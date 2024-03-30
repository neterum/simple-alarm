# Simple Alarm

This project encapsulates all my efforts into detecting simple RF door sensors.  All code runs on a Rasbperry Pi 3. An RTL-SDR USB module and RTL_433 software captures the RF from the door sensors and sends the information to an MQTT server.  This Python code subscribes to the MQTT server and displays the captured message.  Supervisord starts the RTL_433 on boot of the Raspberry Pi.  pyttsx3 library will "speak" a user assigned name door sensor if ~/.config/simple-alarm/devices.json exists.

~/.config/simple-alarm/devices.json format:

```
{
        "id": "a8abe5",
        "device": "Garage Door",
        "voice": "Garage Door"
}
```

### RTL SDR Setup

https://cromwell-intl.com/open-source/raspberry-pi/sdr-getting-started.html
Plug in device
* ```dmesg``` to detect usb
* ```lsusb``` to see if device was detected as "DVB-t" device (this bad)
If device detected as "DVB-T"
* ```lsmod | egrep 'sdr|dvb'``` to detect which DVB-T which module was loaded
* ```sudo vim /etc/modprobe.d/blacklist-dvb.conf```
  * 2023-03-19: Bob added this so RTL-SDR devices are detected as SDR, not DVB
  * ```blacklist dvb_usb_rtl28xxu``` add to blacklist-dvb.conf
* Remove device and unload drivers
  * ```sudo rmmod rtl2832_sdr dvb_usb_rtl28xxu dvb_usb_v2 rtl2832 dvb_core```
  * ```lsmod | egrep 'sdr|dvb'``` (no output is good)
* Plug device back in, run ```dmesg``` to make sure DVB-T driver was not loaded
```
sudo apt install rtl-sdr
sudo vim /etc/udev/rules.d/rtl-sdr.rules
```
* Add all text at https://raw.githubusercontent.com/osmocom/rtl-sdr/master/rtl-sdr.rules into vim file

```
sudo /etc/init.d/udev restart
rtl_test
sudo apt install rtl-433
rtl_433 -f 319500000 -R 100 -F json
rtl_433 -f 319500000 -R 100 -F "mqtt://127.0.0.1:1883,events=door
```
* Note: My door sensors run at 319.5 Mhz.  Yours may vary.

### MQTT Setup

```
sudo apt install mosquitto
systemctl status mosquitto" and "netstat –antp | grep 1883
```

Python library: ```pip3 install paho-mqtt```

### Supervisord Setup

https://hagensieker.com/2019/03/06/how-to-keep-rtl_433-alive-for-your-home-automation-using-supervisor/

```
sudo apt install supervisor
systemctl status supervisor
sudo vim /etc/supervisor/conf.d/rtl_433.conf
```
* Note: default is "/etc/supoervisor/supervisord.conf"

* Paste the below ing the rtl_433.conf file
```
[program:rtl_433]
command=rtl_433 -f 319500000 -R 100 -F "mqtt://127.0.0.1:1883,events=door" 
autostart=true
autorestart=true
stderr_logfile=/var/log/rtl_433.err.log
stdout_logfile=/var/log/rtl_433.out.log
startretries=100
user=pi
```

```cat /var/log/supervisor/supervisord.log``` for any required troubleshooting

### To run this application:

```
git clone https://github.com/neterum/simple-alarm
cd simple-alarm
source venv/bin/activate
pip3 install -r requirements.txt
python simple-alarm/alarm.py
```