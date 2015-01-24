"""
This is the main point of entry.  It does some really ugly things to provide
end users with the most convenience.  It sets a global `SETTINGS` constant
so that users don't need to remember to pass settings or configuration when
creating new connections to new devices.
"""
from __future__ import print_function
import lib.router as router
import argparse
import yaml
import code
from lxml import etree


def parse_arguments():
    """
    Returns parsed CLI arguments.
    """
    arg_parser = argparse.ArgumentParser(description="Router Power Shell")
    arg_parser.add_argument("-d", "--device", help="Router hostname")
    return arg_parser.parse_args()

def parse_config():
    """
    Return the settings specified in `settings_file`.

    """
    settings_file = 'etc/settings.yml'
    with open(settings_file) as fname:
        return yaml.load(fname)

def connect(host):
    """
    Returns a router object, which should also connect the user to the router.
    """
    return router.Router(host=host,
                         user=SETTINGS['credentials']['username'],
                         password=SETTINGS['credentials']['password'])

def main():
    """
    Main point of entry for the script.  Parses arguments, creates
    connections, and creates an interactive Python interpreter.
    """
    args = parse_arguments()
    print("Krait Power Shell for Junos")
    print("Author: Tyler Christiansen <code@tylerc.me>")
    if args.device is not None:
        device = connect(host=args.device)
        print(etree.tostring(device.get_header()))

    # Start an interactive shell for end users to abuse junos-eznc! :)
    var = globals()
    var.update(locals())
    shell = code.InteractiveConsole(var)
    shell.interact()

# Ugly globalness to allow users to call connect more effortlessly from
# the shell
SETTINGS = parse_config()
main()
