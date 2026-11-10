SSH-Honeypot-nx
==============

Adapted from https://github.com/internetwache/SSH-Honeypot by Sebastian Neef (gehaxelt), internetwache.org.

This is a standalone copy of the original project (last upstream commit 3ee0815, March 2021; the code dates from January 2015) with only the changes needed to run it on Python 3. The original imports the Python 2 `thread` module and does not start on Python 3. Behaviour, defaults and log formats are unchanged.

Changes for Python 3:

* `thread.start_new_thread` replaced by a daemon `threading.Thread`; shebang `python3`.
* The credential log is opened as UTF-8 (undecodable characters are written as backslash escapes) and console output is flushed at once, so it reaches the systemd journal.
* Optional environment variables, with the original values as defaults: `SSH_HONEYPOT_PORT` (2222), `SSH_HONEYPOT_LOGFILE` (logins.txt), `SSH_HONEYPOT_KEY` (server.key), `SSH_HONEYPOT_PARAMIKO_LOG` (paramiko.log).
* `requirements.txt` pins paramiko 5.1.0 (tested on Python 3.11).

Install on Python 3: `python3 -m venv venv && venv/bin/pip install -r requirements.txt`, generate the key as below, then `venv/bin/python honeypot.py`.

The original README follows.

SSH-Honeypot
==============

This tool is a simple SSH server in Python which logs all username/password combinations into a logfile.

#Requirements

* ssh-keygen
* python (2.7 or 3.0)
* python-setuptools
* (iptables)

#Installation

* You need to install the ```paramiko``` module. (e.g. ```sudo easy_install paramiko```)
* Clone the repository. ```git clone https://github.com/internetwache/SSH-Honeypot.git``` and switch into the directory ```cd SSH-Honeypot```
* Generate the keypair: ```ssh-keygen -t rsa -f server.key``` and rename the server.key.pub to server.pub (```mv server.key.pub server.pub```)

#Configuration

* To change the ssh port, edit ```SSH_PORT = 2222```
* To change the logfile name, edit ```LOGFILE = 'logins.txt'```

You should use iptables to redirect the SSH traffic from port 22 to 2222 instead of running the script with root privileges. 

```/sbin/iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port 2222```

#License

This piece of software is lincensed under MIT. See LICENSE.md for more information