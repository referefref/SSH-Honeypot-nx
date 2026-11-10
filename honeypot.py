#!/usr/bin/env python3
import os, socket, sys, threading
import paramiko

#generate keys with 'ssh-keygen -t rsa -f server.key'
#Optional environment variables (the defaults are the original settings):
#SSH_HONEYPOT_KEY, SSH_HONEYPOT_PORT, SSH_HONEYPOT_LOGFILE, SSH_HONEYPOT_PARAMIKO_LOG
HOST_KEY = paramiko.RSAKey(filename=os.environ.get('SSH_HONEYPOT_KEY', 'server.key'))
SSH_PORT = int(os.environ.get('SSH_HONEYPOT_PORT', 2222))
LOGFILE = os.environ.get('SSH_HONEYPOT_LOGFILE', 'logins.txt') #File to log the user:password combinations to
PARAMIKO_LOG = os.environ.get('SSH_HONEYPOT_PARAMIKO_LOG', 'paramiko.log')
LOGFILE_LOCK = threading.Lock()

class SSHServerHandler (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            logfile_handle = open(LOGFILE,"a", encoding="utf-8", errors="backslashreplace")
            print("New login: " + username + ":" + password, flush=True)
            logfile_handle.write(username + ":" + password + "\n")
            logfile_handle.close()
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED


    def get_allowed_auths(self, username):
        return 'password'

def handleConnection(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)

    server_handler = SSHServerHandler()

    transport.start_server(server=server_handler)

    channel = transport.accept(1)
    if not channel is None:
        channel.close()

def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', SSH_PORT))
        server_socket.listen(100)

        paramiko.util.log_to_file (PARAMIKO_LOG) 

        while(True):
            try:
                client_socket, client_addr = server_socket.accept()
                threading.Thread(target=handleConnection, args=(client_socket,), daemon=True).start()
            except Exception as e:
                print("ERROR: Client handling")
                print(e)

    except Exception as e:
        print("ERROR: Failed to create socket")
        print(e)
        sys.exit(1)

main()