# RPi-Router
## Using a Raspberry Pi's WiFi Connection to Provide Internet to Devices via Ethernet

###### During periods away from home I spend significant time in accommodation that has public wifi that requires a user to login on a splash page with no direct access to a router. I wanted to be able to use some IoT devices, mainly wifi enabled power outlets, to control things like light and heating. Initially it was just so I could turn on the heat on my way there rather than arrive to a cold room.

###### I had a spare RPi so figured I could use that to connect to the wifi, then share that connection with the ethernet port and plug in an old Sky router I had in the garage, giving me a network in front of the network, so to speak.

## First Step - What You'll Need and Configuring the Pi

###### Because of the connection process I could not do this headless, so I'm not going to go through the process of setting up the Pi that way. I always need access to the GUI to log in to the wifi network via the splash page.

### What You Need
###### 1. A Raspberry Pi (One with an ethernet port, obvs) with a power lead and relevant HDMI cable
###### 2. A micro SD card
###### 3. A monitor
###### 4. A USB mouse and keyboard
###### 5. A router and an ethernet cable

###### To prepare the SD card, you'll need to download a [Raspbian image](https://www.raspberrypi.org/downloads/raspbian/) (lite is fine) and flash the image onto the SD card using [Balena Etcher](https://www.balena.io/etcher).

###### Pop the SD card into the Pi and power it up.
