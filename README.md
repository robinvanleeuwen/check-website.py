# check-website 1.0 

This is a utility to periodically check if websites are online.
It prints to the terminal if a website is up or down, and can send a message to a slack.com webhook channel.

## Usage from commandline

You can use this utility from the commandline for a quick check on a single site while working on whatever you
are doing. 

    rvl@banana:~/check-website$ ./check-website.py -h
    Usage: check-website.py [-c <configfile>] | -u <url> [ -i <interval>] | [-h] [-v]

    Options:
        -h --help       Show this
        -v --version    Show version
        -c <configfile> Use this as configuration file
        -u <url>        Use this url to check
        -i <interval>   Check interval in seconds, default 10 seconds

For example:

    rvl@banana:~/check-website$ ./check-website.py -u https://www.google.com -i 10
    Checking sites:

    https://www.google.com

    With an interval of 10 seconds.
    ...........
    
or

    rvl@studio80:~/check-website$ ./check-website.py -u https://www.thissiteisdown.ugh -i 10
    Checking sites:

    https://www.thissiteisdown.ugh

    With an interval of 10 seconds.
    .Xhttps://www.thissiteisdown.ugh IS DOWN! 2018-06-29 10:44:40..X..X..X..X..X

Or you can use a config file with multiple sites and send a message to a slack.com webhook. See websites.conf template for settings

## Setup as service

You can run this utility on the terminal directly or integrate it
in a systemd service and run it in a screen:

    /usr/systemd/system/check-website.service

    
    Desription=Check Websites
    After=network.target
        
    [Service]
    Type=forking
    User=root
    Group=root
    StandardInput=null
    StandardOutput=journal
    StandardError=journal
    Environment=
    WorkingDirectory=/root
    ExecStart=/usr/bin/screen -dmS check-websites /usr/local/bin/check-website.py -c /etc/websites.conf 
    Restart=on-abort
     
    [Install]
    WantedBy=multi-user.target


