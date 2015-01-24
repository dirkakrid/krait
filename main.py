from __future__ import print_function
import lib.router as router
import argparse
import yaml
import code
from lxml import etree


def parse_arguments():
    arg_parser = argparse.ArgumentParser(description="Router Power Shell")
    arg_parser.add_argument("-d", "--device", help="Router hostname")
    return arg_parser.parse_args()

def parse_config():
    settings = 'etc/settings.yml'
    with open(settings) as f:
        return yaml.load(f)

def connect(host):
    return router.Router(host=host,
                         user=config['credentials']['username'],
                         password=config['credentials']['password'])

def main():
    args = parse_arguments()
    print("Krait Power Shell for Junos")
    print("Author: Tyler Christiansen <code@tylerc.me>")
    if args.device is not None:
        device = connect(host=args.device)

    # Start an interactive shell for end users to abuse junos-eznc! :)
    var = globals()
    var.update(locals())
    shell = code.InteractiveConsole(var)
    shell.interact()

# Ugly globalness to allow users to call connect more effortlessly from
# the shell
config = parse_config()
main()
