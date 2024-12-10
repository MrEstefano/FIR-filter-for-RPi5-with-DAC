# FIR-filter-for-RPi5-with-DAC 



DAC Module	          /        Raspberry Pi 3
VIN	                 /         Pin 2 (5V)
GND	                 /         Pin 6 (GND)
LCK	                 /         Pin 35
DIN	                 /         Pin 40
BCK	                 /         Pin 12
SCK	                 /         GND


The PCM5102 will generate SCK by itself, but it needs to know that it should do that, this is done by connecting SCK to GND. Otherwise your audio output will sound like a distorted, bass-boosted remix (one could, of course say, that this is a nice feature :D).
Refer to pinout.xyz if you aren’t sure about the Pi’s pin numbering.

Software setup
This guide explains it quite well, but I will summarise it here, in case something ever happens to that link.
Editing boot.txt

Run this command to open the file in a text editor:
sudo nano /boot/config.txt

You will need to change the following things:
Uncomment (remove the # before the line):
dtparam=i2s=on
Comment (add a # before the line):
#dtparam=audio=on
Append this to the end of the file:
dtoverlay=hifiberry-dac

Creating asound.conf
Run this command to open the file in a text editor:
sudo nano /etc/asound.conf
And paste the following:
pcm.!default  {
 type hw card 0
}
ctl.!default {
 type hw card 0
}

Now reboot your Raspberry Pi
sudo reboot

