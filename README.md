# check-website

This is a utility to periodically check if websites are online.
It sends a message to a slack.com webhook channel, when a website
is up or down. 

## Setup

You can run this utility on the terminal directly or integrate it
in a systemd service and run it in a screen:

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


