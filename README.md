# pfsense-backup

## Summary

This Tool can be used to Backup the Configuration of a PfSense, version 2.x.x

## Requierements

- Python 2.7
- lxml
- requests

## Usage

    usage: pfsense-backup.py [-h] [-v] [-s] [-o OUTPUT_FILE] [-username USERNAME]
                             [-password PASSWORD]
                             host

    positional arguments:
      host                  The host IP Address or Domain Name of the Firewall

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -s, --https           use https instead of http
      -o OUTPUT_FILE, --output_file OUTPUT_FILE
                            Specifies the Output File
      -username USERNAME, -u USERNAME
                            The Username which should be used for authentication
      -password PASSWORD, -p PASSWORD
                            The Password which should be used for authentication


## Usage Examples

### Safe the Configuration of the Firewall "https://192.168.0.1" int the file "backup.xml"

It is a good Idea to use a dedicated Backup User on your PfSense, for creating Backups, you should also, via a Group, limit the Access of the Backup user so that he can only access the "Backup and Restore" Configuration Panel of the PfSense Webinterface.

This Example uses the user "backup" with the password "secure_much_very_wow" and stores the retrieved Configuration File inside the file "backup.xml"

    python pfsense-backup.py -v -o backup.xml -u backup -p secure_much_very_wow -https 192.168.0.1

### Output the Configuration file of the Firewall "http://192.168.0.1" to the Shell

    python pfsense-backup.py -u backup -p secure_much_very_wow 192.168.0.1
