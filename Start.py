from pypresence import Presence
import time
import psutil
import threading
import json
from datetime import datetime
import os
from colorama import init, Fore, Style

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    print(Fore.CYAN + """
$$$$$$$\\  $$\\                                               $$\\       $$$$$$$\\  $$$$$$$\\   $$$$$$\\  
$$  __$$\\ \\__|                                              $$ |      $$  __$$\\ $$  __$$\\ $$  __$$\\ 
$$ |  $$ |$$\\  $$$$$$$\\  $$$$$$$\\  $$$$$$\\   $$$$$$\\   $$$$$$$ |      $$ |  $$ |$$ |  $$ |$$ /  \\__|
$$ |  $$ |$$ |$$  _____|$$  _____|$$  __$$\\ $$  __$$\\ $$  __$$ |      $$$$$$$  |$$$$$$$  |$$ |      
$$ |  $$ |$$ |\\$$$$$$\\  $$ /      $$ /  $$ |$$ |  \\__|$$ /  $$ |      $$  __$$< $$  ____/ $$ |      
$$ |  $$ |$$ | \\____$$\\ $$ |      $$ |  $$ |$$ |      $$ |  $$ |      $$ |  $$ |$$ |      $$ |  $$\\ 
$$$$$$$  |$$ |$$$$$$$  |\\$$$$$$$\\ \\$$$$$$  |$$ |      \\$$$$$$$ |      $$ |  $$ |$$ |      \\$$$$$$  |
\\_______/ \\__|\\_______/  \\_______| \\______/ \\__|       \\_______|      \\__|  \\__|\\__|       \\______/ 
    """ + Style.RESET_ALL)

def find_config_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    max_depth = 3
    
    for i in range(max_depth):
        config_path = os.path.join(current_dir, 'config.json')
        if os.path.exists(config_path):
            return config_path
        current_dir = os.path.dirname(current_dir)
    
    return None

def load_config():
    try:
        config_path = find_config_file()
        if config_path is None:
            print(Fore.RED + "Error: config.json not found in current or parent directories" + Style.RESET_ALL)
            return None
            
        print(Fore.GREEN + f"Found config at: {config_path}" + Style.RESET_ALL)
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(Fore.RED + f"Error loading config: {e}" + Style.RESET_ALL)
        return None

def get_system_info():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    current_time = datetime.now()
    uptime_seconds = time.time() - psutil.boot_time()
    
    import platform
    import socket
    import getpass

    return {
        "cpu": cpu,
        "cores": psutil.cpu_count(),
        "ram": memory.percent,
        "ram_total": round(memory.total / (1024**3), 2),
        "ram_used": round(memory.used / (1024**3), 2),
        "ram_free": round(memory.free / (1024**3), 2),
        "disk": disk.percent,
        "disk_total": round(disk.total / (1024**3), 2),
        "disk_used": round(disk.used / (1024**3), 2),
        "disk_free": round(disk.free / (1024**3), 2),
        
        "time": current_time.strftime("%H:%M:%S"),
        "date": current_time.strftime("%Y-%m-%d"),
        "uptime": time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)),
        "hour": current_time.strftime("%H"),
        "minute": current_time.strftime("%M"),
        "second": current_time.strftime("%S"),
        "day": current_time.strftime("%d"),
        "month": current_time.strftime("%m"),
        "year": current_time.strftime("%Y"),
        "weekday": current_time.strftime("%A"),
        
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "ip": socket.gethostbyname(socket.gethostname())
    }

def update_rpc(rpc, config):
    update_count = 0
    while True:
        try:
            system_info = get_system_info()
            details = config['details']
            state = config['state']
            
            # Replace all variables
            for key, value in system_info.items():
                details = details.replace(f"%{key}%", str(value))
                state = state.replace(f"%{key}%", str(value))
            
            rpc.update(
                details=details,
                state=state,
                start=int(time.time()),
                large_image=config['large_image'],
                large_text=config['large_text'],
                small_image=config['small_image'],
                small_text=config['small_text']
            )
            
            update_count += 1
            clear_console()
            print_logo()
            print(Fore.GREEN + "✓ Discord RPC Active" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Updates: {update_count}" + Style.RESET_ALL)
            print(Fore.CYAN + "\nCurrent Status:" + Style.RESET_ALL)
            print(f"Details: {details}")
            print(f"State: {state}")
            print(Fore.CYAN + "\nSystem Info:" + Style.RESET_ALL)
            print(f"CPU: {system_info['cpu']}% | RAM: {system_info['ram']}% | Disk: {system_info['disk']}%")
            print(f"Time: {system_info['time']} | Date: {system_info['date']}")
            print(f"Uptime: {system_info['uptime']}")
            print(Fore.MAGENTA + "\nPress Ctrl+C to exit" + Style.RESET_ALL)
            
            time.sleep(15)
        except Exception as e:
            print(Fore.RED + f"\nError: {e}" + Style.RESET_ALL)
            break

def main():
    clear_console()
    print_logo()
    
    config = load_config()
    if not config:
        input(Fore.RED + "Press Enter to exit..." + Style.RESET_ALL)
        return
        
    client_id = config['client_id']
    if client_id == "YOUR_DISCORD_APP_CLIENT_ID":
        print(Fore.RED + "Error: Please set your Discord Application ID in config.json" + Style.RESET_ALL)
        input("Press Enter to exit...")
        return

    try:
        print(Fore.YELLOW + "Connecting to Discord..." + Style.RESET_ALL)
        rpc = Presence(client_id)
        rpc.connect()
        print(Fore.GREEN + "Connected to Discord RPC!" + Style.RESET_ALL)
        time.sleep(1)
        
        rpc_thread = threading.Thread(target=update_rpc, args=(rpc, config), daemon=True)
        rpc_thread.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nShutting down Discord RPC..." + Style.RESET_ALL)
        if rpc:
            rpc.close()
    except Exception as e:
        print(Fore.RED + f"\nError: {e}" + Style.RESET_ALL)
        if rpc:
            rpc.close()

if __name__ == "__main__":
    main()