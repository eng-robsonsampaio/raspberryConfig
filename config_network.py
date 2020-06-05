from consolemenu import *
from consolemenu.items import *

SSID = ''
PSK = ''
IP = ''
MASK = ''
new_wpa_supplicant = []
new_dhcpcd = []

wpa_supplicant_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
dhcpdc_file = "/etc/dhcpcd.conf"

# Create the menu
menu = ConsoleMenu("Raspberry Network Configurations")

def set_wireless_network():
    global SSID, PSK 
    SSID = input("SSID: ")
    PSK = input("PSK: ")
    resp = input("Save changes? (Y/N): ")
    if resp.lower() == 'y':
        save_network_changes()
    else:
        print('\nChanges have been discarded!')
        PSK = ''
        SSID = ''
    input('\n\nType any key to exit')

def set_ip_address():
    global IP, MASK
    IP = input("IP: ")
    MASK = input("Mask: ")
    resp = input("Save changes? (Y/N): ")
    if resp.lower() == 'y':
        save_ip_changes()
    else:
        print('\nChanges have been discarded!')
        IP = ''
        MASK = ''
    input('\n\nType any key to exit')

def show_wireless_network():
    print(f"SSID: {SSID}")
    print(f"PSK: {PSK}")
    input('\n\nType any key to exit')

def show_ip_address():
    print(f"IP: {IP}/{MASK}")
    input('\n\nType any key to exit')

def insert_new_content(line, line_pos, content_file, new_content, separator="="):
    [variable, value] = line.split(separator)
    char = '"'
    content_file[line_pos] = f"{variable}{separator}{char}{new_content}{char}\n"
    return content_file

def read_files():
    with open(dhcpdc_file, "r") as file:
        content = file.readlines()
        print("IP:")
        for i, line in enumerate(content):
            if "interface wlan0" in line:
                if(line[0] == "#"):
                    print(f"{line[1:]}")
                else:
                    print(f"{line}")
                if(content[i + 1][0] == "#"):
                    print(f"{content[i + 1][1:]}")
                else:
                    print(f"{content[i + 1]}")

    with open(wpa_supplicant_file, "r") as file:
        content = file.readlines()
        print("Wireless network:")
        for i, line in enumerate(content):
            if "ssid" in line:
                print(f"{line}")
                print(f"{content[i+1]}")

    input('\n\nType any key to exit')

def save_network_changes():
    with open(wpa_supplicant_file, "r") as file:
        content = file.readlines()
        for i, line in enumerate(content):
            if "ssid" in line:  
                new_wpa_supplicant = insert_new_content(line,line_pos=i,content_file=content, new_content=SSID)
            if "psk" in line:
                new_wpa_supplicant = insert_new_content(line,line_pos=i,content_file=content, new_content=PSK)

    with open(wpa_supplicant_file, "w") as file:
        file.writelines(new_wpa_supplicant)
    print('Changes have been saved')

def save_ip_changes():
    with open(dhcpdc_file, "r") as file:
        content = file.readlines()
    for i, line in enumerate(content):
        if "interface wlan0" in line:
            if(line[0] == "#"):
                content[i] = line[1:]
            [variable, value] = content[i+1].split("=")
            if(variable[0] == "#"):
                content[i+1] = f"{variable[1:]}={IP}/{MASK}\n"
            else:
                content[i+1] = f"{variable}={IP}/{MASK}\n"
    new_content = content

    with open(dhcpdc_file, "w") as file:
        file.writelines(new_content)

wireless_network = FunctionItem("Set wireless network ", set_wireless_network)
ip_address = FunctionItem("Set ip address", set_ip_address)
show_config = FunctionItem("Show wireless network", read_files)

menu.append_item(wireless_network)
menu.append_item(ip_address)
menu.append_item(show_config)
menu.show()