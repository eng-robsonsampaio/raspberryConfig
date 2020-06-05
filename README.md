# raspberryConfig
Simple script to set some configurations such as static ip and wireless network in raspberry. I am using console-menu to open a interactive menu in the rasp console.

## Usage

```
from consolemenu import *
from consolemenu.items import *

```
You will have to have admin privilagies in order to change wpa_supplicant.conf and dhcpcd.conf
```
sudo python config_network

```
