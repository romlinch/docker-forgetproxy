#!/usr/bin/env python

# Copyright (c) 2014, Tully Foote

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os
import subprocess
import socket
import sys
import time

redirect_cmd_return_1 = "iptables -t nat -A PREROUTING -i docker0 -d 10.0.0.0/8 -j RETURN"
redirect_cmd_return_2 = "iptables -t nat -A PREROUTING -i docker0 -d 127.0.0.0/8 -j RETURN"
redirect_cmd_return_3 = "iptables -t nat -A PREROUTING -i docker0 -d 169.254.0.0/16 -j RETURN"
redirect_cmd_return_4 = "iptables -t nat -A PREROUTING -i docker0 -d 172.16.0.0/12 -j RETURN"
redirect_cmd_return_5 = "iptables -t nat -A PREROUTING -i docker0 -d 192.168.0.0/16 -j RETURN"
redirect_cmd_return_6 = "iptables -t nat -A PREROUTING -i docker0 -d 224.0.0.0/4 -j RETURN"
redirect_cmd_return_7 = "iptables -t nat -A PREROUTING -i docker0 -d 240.0.0.0/4 -j RETURN"
redirect_cmd_http_1 = "iptables -t nat -A PREROUTING -p tcp" \
               " --dport 80 -i docker0 -j REDIRECT --to 12345"
redirect_cmd_http_2 = "iptables -t nat -A PREROUTING -p tcp" \
               " --dport 8080 -i docker0 -j REDIRECT --to 12345"
redirect_cmd_all_1 = "iptables -t nat -A PREROUTING -p tcp" \
               " -i docker0 -j REDIRECT --to 12346"

remove_redirect_cmd_return_1 = redirect_cmd_return_1.replace(' -A ', ' -D ')
remove_redirect_cmd_return_2 = redirect_cmd_return_2.replace(' -A ', ' -D ')
remove_redirect_cmd_return_3 = redirect_cmd_return_3.replace(' -A ', ' -D ')
remove_redirect_cmd_return_4 = redirect_cmd_return_4.replace(' -A ', ' -D ')
remove_redirect_cmd_return_5 = redirect_cmd_return_5.replace(' -A ', ' -D ')
remove_redirect_cmd_return_6 = redirect_cmd_return_6.replace(' -A ', ' -D ')
remove_redirect_cmd_return_7 = redirect_cmd_return_7.replace(' -A ', ' -D ')

remove_redirect_cmd_http_1 = redirect_cmd_http_1.replace(' -A ', ' -D ')
remove_redirect_cmd_http_2 = redirect_cmd_http_2.replace(' -A ', ' -D ')
remove_redirect_cmd_all_1 = redirect_cmd_all_1.replace(' -A ', ' -D ')

LOCAL_PORT = 12345




def is_port_open(port_num):
    """ Detect if a port is open on localhost"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(('127.0.0.1', port_num)) == 0


class RedirectContext:
    """ A context to make sure that the iptables rules are removed
    after they are inserted."""
    def __enter__(self):
        print("Enabling IPtables forwarding")
        try:
            subprocess.check_call(redirect_cmd_return_1.split())
            subprocess.check_call(redirect_cmd_return_2.split())
            subprocess.check_call(redirect_cmd_return_3.split())
            subprocess.check_call(redirect_cmd_return_4.split())
            subprocess.check_call(redirect_cmd_return_5.split())
            subprocess.check_call(redirect_cmd_return_6.split())
            subprocess.check_call(redirect_cmd_return_7.split())

            subprocess.check_call(redirect_cmd_http_1.split())
            subprocess.check_call(redirect_cmd_http_2.split())
            subprocess.check_call(redirect_cmd_all_1.split())

            self.setup = True
        except:
            print("Failed to setup IPTABLES. Did you use --privileged"
                  " if not you need to run")
            self.setup = False
        return self

    def __exit__(self, type, value, traceback):
        if self.setup:
            print("Disabling IPtables forwarding")
            subprocess.check_call(remove_redirect_cmd_return_1.split())
            subprocess.check_call(remove_redirect_cmd_return_2.split())
            subprocess.check_call(remove_redirect_cmd_return_3.split())
            subprocess.check_call(remove_redirect_cmd_return_4.split())
            subprocess.check_call(remove_redirect_cmd_return_5.split())
            subprocess.check_call(remove_redirect_cmd_return_6.split())
            subprocess.check_call(remove_redirect_cmd_return_7.split())

            subprocess.check_call(remove_redirect_cmd_http_1.split())
            subprocess.check_call(remove_redirect_cmd_http_2.split())
            subprocess.check_call(remove_redirect_cmd_all_1.split())


def main():
    if os.geteuid() != 0:
        print("This must be run as root, aborting")
        return -1

    # While the process is running wait for squid to be running
    while not is_port_open(LOCAL_PORT):
        print("Waiting for port %s to open" % LOCAL_PORT)
        time.sleep(1)

    if is_port_open(LOCAL_PORT):
        print("Port %s detected open setting up IPTables redirection" %
              LOCAL_PORT)
        with RedirectContext():
            # Wait for the squid instance to end or a ctrl-c
            try:
                while is_port_open(LOCAL_PORT):
                    time.sleep(1)
            except KeyboardInterrupt as ex:
                # Catch Ctrl-C and pass it into the squid instance
                print("CTRL-C caught, shutting down.")
            except Exception as ex:
                print("Caught exception, %s, shutting down" % ex)

    else:
        print("Port %s never opened, squid instance"
              " must have terminated prematurely" % LOCAL_PORT)

    return 0

if __name__ == '__main__':
    sys.exit(main())
