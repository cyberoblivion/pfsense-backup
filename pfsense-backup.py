__author__ = 'cstein'
import requests
from lxml import html
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
parser.add_argument("-s", "--https", action="store_true", help="use https instead of http")
parser.add_argument("-o", "--output_file", help="specifies the Output File")
parser.add_argument("host", type=str, help="the host IP Address or Domain Name of the Firewall")
parser.add_argument("-username", "-u", type=str, help="the Username which should be used for authentication")
parser.add_argument("-password", "-p", type=str, help="the Password which should be used for authentication")
args = parser.parse_args()

if args.https:
    host = "https://%s/" % args.host
else:
    host = "http://%s/" % args.host

verify = False
# todo: The Tool should warn the User if the Certificate could not be verified!
# Just setting Verify to False is a Dirty Workaround, this way every SSL Certificate will be accepted.
# The User should be able to use a Commandline Argument to choose if he wants to ignore unverified Certificates.

s = requests.session()

# Get the Magic CSRF Token
if args.verbose:
    print('retrieving the "magic" CSRF Token.')
r = s.get("%sindex.php" % host, verify=verify)
try:
    magic_csrf_token = html.fromstring(r.text).xpath('/html/body/div/form/input/@value')[0]
except:
    magic_csrf_token = ""
if args.verbose:
    print('Token: %s' % magic_csrf_token)

# Login into Firewall Webinterface
if args.verbose:
    print('Logging in, into %s' % host)
r = s.post("%sindex.php" % host,
           data={
               "__csrf_magic": magic_csrf_token,
               "usernamefld": args.username,
               "passwordfld": args.password,
                "login": "Login"
           },
           verify=verify)
if html.fromstring(r.text).xpath('//title/text()')[0].startswith("Login"):
    exit("Login was not Successful!")

# download configuration
if args.verbose:
    print('retrieving the Configuration File')
r = s.post("%sdiag_backup.php" % host, data={"Submit": "Download configuration", "donotbackuprrd": "on"}, verify=verify)
if html.fromstring(r.text).xpath('count(//pfsense)') != 1.0:
    exit("Something went wrong! the returned Content was not a PfSense Configuration File!")

# safe or output the Configuration
if args.output_file:
    if args.verbose:
        print('Safing the Configuration to: %s' % args.output_file)
    with open(args.output_file, "w") as f:
        f.write(r.text)
else:
    print(r.text)