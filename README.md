![Logo](assets/logo.png)
# MultiBind 
🚧 Under Constructions 🚧

## About
A bind shell is a type of network shell that listens for incoming connections on a specific network port. When a connection is established, the shell "binds" to the incoming network connection, essentially opening up a command line interface on the target system. This allows an attacker to remotely execute commands and interact with the target machine as if they were physically present and typing commands directly.

MultiBind is inspired by one of the projects on the TCM (Python 201 for Hacker) Course, I have added and will continue to add multiple functionalities such as:
- [X] Client Side
- [X] Server Side
- [X] Data Gathering (OS, IP, PWD)
- [ ] Port Change (argument)
- [ ] Encryption (AES)
- [ ] OS Detection
- [ ] PowerShell Support


## How to Use
MultiBind uses argparse to dictate whether it is in "client mode" (Sending Connections) or "server mode"(Receiving Connections).

In a Penetration testing scenario "Client Mode" will run on your attacking machine to send and establish a terminal connection to your victim machine, to start client mode run the following command: 
```python
python3 bind.py -c <VICTIM-MACHINE-IP>
```

On the hand "Server Mode" will run on your victim machine to open up a port and listen on all interfaces(0.0.0.0), currently the default port is "5757", to start server mode run the following command: 
```python
python3 bind.py -l
```
