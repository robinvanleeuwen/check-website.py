#!/usr/bin/python3

from time import sleep
from time import strftime
from docopt import docopt

import urllib3
import requests
import configparser
import sys

arguments = """Usage: check-website.py [-c <configfile>] | -u <url> [ -i <interval>] | [-h] [-v]

Options:
    -h --help       Show this
    -v --version    Show version
    -c <configfile> Use this as configuration file
    -u <url>        Use this url to check
    -i <interval>   Check interval in seconds, default 5 second 

"""

_VERSION_ = "0.1"


class WebsiteChecker():

    doc = None
    websites = dict()
    interval = 0
    slack_url = None
    identifier = ""

    def __init__(self):
        self.doc = docopt(arguments)

    def run(self):
        self.parse_arguments()
        self.check_websites()

    def parse_arguments(self):

        if self.doc["--version"]:
            print(_VERSION_)
            sys.exit()

        if self.doc["-c"]:
            self.read_config()
            
        if self.doc["-u"]:
            self.websites[self.doc["-u"]] = "UP"
            self.interval = self.doc["-i"] or 10

    def check_websites(self):

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if len(self.websites) == 0:

            sys.exit()

        print("Checking sites:\n")

        for site in self.websites:
            print(site)

        print("\nWith an interval of {0} seconds.".format(self.interval))

        while True:

            for site in self.websites:

                print(".", end="")
                sys.stdout.flush()

                timestamp = strftime("%Y-%m-%d %H:%M:%S")

                try:
                    requests.head(site, timeout=10, verify=False)

                    if self.websites[site] == "DOWN":
                        print("Yey! {0} is up again! {1}".format(site, timestamp), end="")
                        sys.stdout.flush()
                        self.sendslack(site, state="up", timestamp=timestamp)
                        self.websites[site] = "UP"
                        continue

                except Exception as e:

                    print("X", end="")
                    sys.stdout.flush()

                    if self.websites[site] == "UP":
                        self.websites[site] = "DOWN"
                        print("{0} IS DOWN! {1}".format(site, timestamp), end="")
                        sys.stdout.flush()
                        self.sendslack(site, state="down", timestamp=timestamp)
                        continue

            print(".", end="")
            sleep(int(self.interval))

    def read_config(self):

        config = configparser.ConfigParser()
        config.read(self.doc["-c"])

        self.interval = config.get("settings", "interval")
        self.identifier = config.get("settings", "identifier")
        self.slack_url = config.get("settings", "slack_url")

        for site in config.get("settings", "sites").split(" "):

            if site.find("http") == 0:

                self.websites[site] = "UP"

    def sendslack(self, site, state, timestamp=None):

        if not self.slack_url:
            return

        print(self.slack_url)

        if state == "up":

            payload = {
                "text": "{0}: Yey! :+1: :+1: :+1: *{1}* is up again! ({2})".format(self.identifier, site, timestamp)
            }

        elif state == "down":

            payload = {
                "text": "{0}: *{1}* is DOWN :sob: ({2})".format(self.identifier, site, timestamp)
            }

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(self.slack_url, json=payload, headers=headers)
        except Exception as e:
            print(e)


if __name__ == "__main__":

    c = WebsiteChecker()
    c.run()
