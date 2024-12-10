# FIR filter aplication using RPi 5 with DAC PCM5102

![rpi5 and dac](https://github.com/user-attachments/assets/55c003f5-7e87-428f-b4b3-eaf175b9dd2c)

Figure 1 by Himbeer

## DAC 	          /        RPi 5
## VIN	                 /         Pin 2 (5V)
## GND	                 /         Pin 6 (GND)
## LCK	                 /         Pin 35
## DIN	                 /         Pin 40
## BCK	                 /         Pin 12
## SCK	                 /         GND


The PCM5102 will generate SCK by itself, but it needs to know that it should do that, this is done by connecting SCK to GND. Otherwise your audio output will sound like a distorted, bass-boosted remix (one could, of course say, that this is a nice feature :D).
Refer to pinout.xyz if you aren’t sure about the Pi’s pin numbering.

## Software setup
This guide explains it quite well, but I will summarise it here, in case something ever happens to that link.
Editing boot.txt

## Run this command to open the file in a text editor:
sudo nano /boot/config.txt

## You will need to change the following things:
## Uncomment (remove the # before the line):
dtparam=i2s=on
## Comment (add a # before the line):
#dtparam=audio=on
## Append this to the end of the file:
dtoverlay=hifiberry-dac

## Creating asound.conf
## Run this command to open the file in a text editor:
sudo nano /etc/asound.conf
## And paste the following:
pcm.!default  {
 type hw card 0
}
ctl.!default {
 type hw card 0
}

## Now reboot your Raspberry Pi
sudo reboot

Credits to:  Himbeer for picture and set up steps

DAC PCM5102

![ZBK8Q](https://github.com/user-attachments/assets/60383264-e44c-41a9-9537-8bbbf705d85c)
