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
            self.interval = self.doc["-i"] or 5

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

                try:
                    requests.head(site, timeout=2, verify=False)

                    if self.websites[site] == "DOWN":
                        print("Yey! {0} is up again!".format(site), end="")
                        sys.stdout.flush()
                        self.sendslack(site, state="up")
                        self.websites[site] = "UP"
                        continue

                except Exception as e:

                    print("X", end="")
                    sys.stdout.flush()

                    if self.websites[site] == "UP":
                        self.websites[site] = "DOWN"
                        print("{0} IS DOWN!".format(site), end="")
                        sys.stdout.flush()
                        self.sendslack(site, state="down")
                        continue

            print(".", end="")
            sleep(int(self.interval))

    def read_config(self):

        config = configparser.ConfigParser()
        config.read(self.doc["-c"])

        self.interval = config.get("settings", "interval")

        self.slack_url = config.get("settings", "slack_url")

        for site in config.get("settings", "sites").split(" "):

            if site.find("http") == 0:

                self.websites[site] = "UP"

    def sendslack(self, site, state):

        if not self.slack_url:
            return

        print(self.slack_url)


        timestamp = strftime("%Y-%m-%d %H:%M:%S")

        if state == "up":

            payload = {
                "text": "Rigter Website Monitor: Yey! :+1: :+1: :+1: *{0}* is up again! ({1})".format(site, timestamp)
            }

        elif state == "down":

            payload = {
                "text": "Rigter Website Monitor: *{0}* is DOWN :sob: ({1})".format(site, timestamp)
            }

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(self.slack_url, json=payload, headers=headers)
            print("")
        except Exception as e:
            print(e)


if __name__ == "__main__":

    c = WebsiteChecker()
    c.run()
