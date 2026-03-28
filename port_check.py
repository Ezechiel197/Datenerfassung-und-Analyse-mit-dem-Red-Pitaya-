import socket

ip = '169.254.2.247'
port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    result = s.connect_ex((ip, port))
    if result == 0:
        print("Port ist offen")
    else:
        print("Port ist geschlossen oder der SCPI-Server läuft nicht.")
