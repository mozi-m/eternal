import threading
import sys
import os
import time
import paramiko

import channel
import database
import broadcast

server_addr = "0.0.0.0"

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} [port]")
    exit()
try:
    HOST_KEY = paramiko.RSAKey(filename="private.key")
except Exception as e:
    print(e)
    print("Could not find RSA key!")
    exit()

def live_title():
    while 1:
        try:
            sys.stdout.write(f"\x1b]2;Eternal | Vtubers: {len(broadcast.addr_clients)} | Dup Vtubers {len(broadcast.dup_clients)} | PID: {str(os.getpid())}\x07")
            sys.stdout.flush()
            time.sleep(0.5)
        except:
            pass

def main():
    try:
        port = int(sys.argv[1])
    except:
        print("Port must be an integer")
        exit()
    
    print(f"[main] Initialized - PID {str(os.getpid())}")
    threading.Thread(target=live_title).start()
    threading.Thread(target=database.db_init).start()
    threading.Thread(target=channel.start_ssh,args=(server_addr, port), daemon=True).start()
    threading.Thread(target=broadcast.brd_init, daemon=True).start()

if __name__ == "__main__":
    main()
