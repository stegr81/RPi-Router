# RPi-Router
## Using a Raspberry Pi's WiFi Connection to Provide Internet to Devices via Ethernet

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

`sudo apt-get update`

###### Once it's done it's thing, go again with...

`sudo apt-get upgrade`

## Install the DHCP Software

###### A Dynamic Host Control Protocol server is responsible for assigning addresses to computers and devices on an access point. We're going to use isc-dhcp-server.

`sudo apt-get install isc-dhcp-server`

###### We need to define the network and associated addresses that the DHCP server will be serving. To do that we need to modify the configuration file. I had a few issues with this initially, but there aren't really too many things to consider.
###### To edit files I use Nano, but feel free to use whichever text editor you prefer...
`sudo nano /etc/dhcp/dhcpd.conf`
###### You'll find that everything is hashed out. Find the line that says 'authoritative' and unhash it.
###### At the end of the file enter the following:
```
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
`sudo nano /etc/default/isc-dhcp-server`
###### Find the line that says INTERFACES and edit it to say the following...
`INTERFACES="eth0"`
###### Exit and save the file.





