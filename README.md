# RPi-Router
## Using a Raspberry Pi's WiFi Connection to Provide Internet to Devices via Ethernet (or vice-versa)

###### During periods away from home for work, I spend significant time in accommodation that has public wifi that requires the user to login on a splash page with no direct access to a router. I wanted to be able to use some IoT devices in the room, mainly wifi enabled power outlets, to control things like light and heating. Initially it was just so I could turn on the heat on my way there rather than arrive to a cold room.

###### I had a spare RPi so figured I could use that to connect to the wifi, then share that connection with the ethernet port and plug in an old Sky router I had in the garage, giving me a network in front of the network, so to speak.

## First Step - What You'll Need and Configuring the Pi

###### Because of the connection process I could not do this headless, so I'm not going to go through the process of setting up the Pi that way. I always need access to the GUI to log in to the wifi network via the splash page. However, [this is a great guide to doing so](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html), if you'd like to know.

### What You Need
###### 1. A Raspberry Pi (One with an ethernet port, obvs) with a power lead and relevant HDMI cable
###### 2. A micro SD card
###### 3. A monitor
###### 4. A USB mouse and keyboard
###### 5. A router and an ethernet cable

###### To prepare the SD card, you'll need to download a [Raspbian image](https://www.raspberrypi.org/downloads/raspbian/) and flash the image onto the SD card using [Balena Etcher](https://www.balena.io/etcher).

###### Pop the SD card into the Pi, attach the relevant cables and peripherals and power it up.

###### After a few setting you'll be into the GUI. Then connect to your preferred wifi connection.

###### It's always worth running the update/upgrade processes

###### Open up a terminal window and type...

```sudo apt-get update```

###### Once it's done it's thing, go again with...

```sudo apt-get upgrade```

## Install the DHCP Software

###### A Dynamic Host Control Protocol server is responsible for assigning addresses to computers and devices on an access point. We're going to use isc-dhcp-server.

```sudo apt-get install isc-dhcp-server```

## Define the Server Settings
###### We need to define the network and associated addresses that the DHCP server will be serving. To do that we need to modify the configuration file. I had a few issues with this initially, but there aren't really too many things to consider. In the end I got rid of most of what was in there and replaced it with just what I needed.
###### To edit files I use Nano, but feel free to use whichever text editor you prefer...
```sudo nano /etc/dhcp/dhcpd.conf```
###### You can find the lines mentioned below and unhas them where required, adding the subnet settings at the end of the file, or just copy this and replace everything already in the file.
```
ddns-update-sytle none;

default-lease-time 600;
max-lease-time 7200;

authoritative;
subnet 192.168.10.0 netmask 255.255.255.0 {
 range 192.168.10.10 192.168.10.250;
 option broadcast-address 192.168.10.255;
 option routers 192.168.10.1;
 default-lease-time 600;
 max-lease-time 7200;
 option domain-name "local-network";
 option domain-name-servers 8.8.8.8, 8.8.4.4;
}
```
###### You can use whatever range you like, but I've gone with 192.168.10.x range. To exit the file hit ctrl+x, when Nano asks if you'd like to save the file, hit 'y' then enter.
###### Now, using Nano again in the same way as before, edit /etc/default/isc-dhcp-server...
```sudo nano /etc/default/isc-dhcp-server```
###### Find the line that says INTERFACES and edit it to say the following...
```INTERFACES="eth0"```
###### Exit and save the file.

## Setting a static IP

###### We need to set a static address for the eth port. Edit the `/etc/network/interfaces` file to show the following. This will allow the wlan to be handled by the dhcp server, but the eth be static as specified.

```
auto lo

iface lo inet loopback
iface wlan0 inet dhcp

allow-hotplug eth0

iface eth0 inet static
 address 192.168.10.1
 netmask 255.255.255.0
```


## Configure IP Forwarding/NAT

###### We need to configure the translation in order that the network traffic will be correctly routed; from the wlan to the eth and in return from the eth to the wlan.
```
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i eht0 -o wlan0 -j ACCEPT
```

###### We also need to make a slight change to the `/etc/sysctl.conf`file
###### Scroll down to the end of the file and add the line...
```net.ipv4.ip_forward=1```

###### At this point more or less everything required is done, but I found that as soon as I plugged my LAN cable in to the PI, the wifi connection dropped. This is due to the Pi prioritising the eth port, which has no connection to the outside world.

###### We need to prioritise the wlan
```
DEFAULT_IFACE=`route -n | grep -E "^0.0.0.0 .+UG" | awk '{print $8}'`
if [ "$DEFAULT_IFACE" != "wlan0" ]
then
  GW=`route -n | grep -E "^0.0.0.0 .+UG .+wlan0$" | awk '{print $2}'`
  echo Setting default route to wlan0 via $GW
  sudo route del default $DEFAULT_IFACE
  sudo route add default gw $GW wlan0
fi
```

###### At this point we should be done. The whole guide was designed to show how to share the wifi connection of a RPi via it's LAN port, however, as stated in the header, if you want to do the opposite and share a wired connection, turing your Pi into a wireless access point. To do this there's a few extra steps and one piece of extra hardware required.
###### You'll need a USB wifi adaptor, which you can plug into one of the spare ports on the Pi.
###### You'll also need to add some additional software. We'll install hostAPD to handle this part. This software has been made available by Jens Segers. Send some love http://jenssegers.be
```
wget https://github.com/jenssegers/RTL8188-hostapd/archive/v1.1.tar.gz
tar -zxvf v1.1.tar.gz
cd RTL8188-hostapd-1.1/hostapd sudo make sudo make install
```
###### To configure hostAPD run the following...
```sudo nano /etc/hostapd/hostapd.conf```
######  This will create a new wireless network called *wifi* with a default password of *YourPassPhrase*. This can all be changed in the .conf file.
###### Going back slightly; in the section covering NAT, Static IP and port prioritisation, change wlan0 for eth0 and vice-versa. 

###### I'll caveat that I haven't tried it this way around, but you should be good to go. If you have any issues, check out [this guide](https://raspberrypihq.com/how-to-turn-a-raspberry-pi-into-a-wifi-router/)

## Extras
###### I found that, for some so far unknown reason, the connection would drop occasionally, but running the IP Forwarding/NAT configuration sorted it. I created a bash script for ease and as something I could set to run at reboot, mainly in the case of power cuts to ensure reconnection if I wasn't around.

```
echo Starting DHCP server
#starting dhcp server
sudo service isc-dhcp-server start
#ensuring both wlan and eth are active
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo ifup wlan0
sudo ifup eth0
#set NAT
echo Setting NAT routing
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i eht0 -o wlan0 -j ACCEPT
echo NAT routing set
#ensure the wifi is prioritised over the wlan
DEFAULT_IFACE=`route -n | grep -E "^0.0.0.0 .+UG" | awk '{print $8}'`
if [ "$DEFAULT_IFACE" != "wlan0" ]
then
  GW=`route -n | grep -E "^0.0.0.0 .+UG .+wlan0$" | awk '{print $2}'`
  echo Setting default route to wlan0 via $GW
  sudo route del default $DEFAULT_IFACE
  sudo route add default gw $GW wlan0
fi
```

###### Ordinarily I set files to run at boot by editing `/etc/rc.local`, however in this instance, because this will run during boot, rather once boot is complete, I found it didn't work. Instead edit `/etc/bash.bashrc` and add `sudo bash <file path>`.

###### To keep my connection alive I created a Python script that conducts regular GET requests or, if they fail to produce a 200 response, run the bash script to reconnect everthing. This works really well until my connection has been running for 7 days, then my wifi network disconnects me.

###### To get around this is likely personal to you/your situation. To solve this aspect I created an additional function in my Python script that essentially conducts a POST request and logs me back in if the script fails to get a positive status update from the IoT device. This check is conducted each time the GET request runs, so around every 15 minutes. The full script is below, but with identifying aspects removed.

```
import requests,re,os,subprocess,sys
from time import sleep
from datetime import datetime

def login():
        r=requests.get('<splash page for public wifi>')
        p=re.compile(r'("csrfmiddlewaretoken".value="([^"]*))') #The services uses CSRF authentication tokens, so I find this using regex
        csrfmiddlewaretoken=p.search(r.text)[2]
        print(f'Authentication token: {csrfmiddlewaretoken}')
        url='<login in URL for public wifi>'
        payload={
                'csrfmiddlewaretoken':csrfmiddlewaretoken,
                'next':'/',
                'username':'xxxxxxxxxx',
                'password':'xxxxxxxxxxxxx',
                }
        conn=requests.post(url,data=payload)
        print(f'Connection Code: {conn}')
subprocess.run(['<bash script file path>', 'arguments'], shell=True)
sleep(2)
login()
sleep(10)
try:
        import tinytuya as tt # my device is TUYA enabled so all of the tt parts relate to that.
except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tinytuya"])
        import tinytuya as tt

socket=tt.OutletDevice(
        dev_id='xxxxxxxxxxxxxxxxxxxxxxxx',
        address='192.168.xx.xx',
        local_key='xxxxxxxxxxxxxxxxxx',
        dev_type='default',
        version=3.3
        )

while True:
        try:
                resp = requests.get("<a suitable page URL>")
                if resp.status_code == 200:
                        print(f"{str(datetime.now())} - respone:{resp}")
                        sleep(900)
        except:
                subprocess.run(['<bash script file path>', 'arguments'], shell=True)
                sleep(30)
                continue
        status=socket.status()
        if 'dps' not in status.keys():
                login()
                sleep(30)
                continue
```






