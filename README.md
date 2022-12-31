# udesktop
Javascript/Micro Python Remote Desktop for ESP/RPI microcontrollers
<p>
This is a remote desktop capable of spawning mutiple Terminal shells, File Browser, and Editor.
using an HTML/Javascript front end and a micro python back end server.
The windows support drag and drop, minimize, resize. 
</p>
![udesktop.PNG](https://raw.github.com/elahtrebor/udesktop/main/udesktop.PNG)


<p>

This works by letting Javascript and HTML peform the heavy lifting 
in your web browser while making low levels calls to the python server to
handle the file system manipulation. For instance when a terminal is spawned,
javascript basically clones a DIV with a textarea that has callbacks 
to listen for keypresses. When the enter key is detected it sends the current
line of text to the python script listening on port 80 using ajax.
The python script parses a set of commands and returns results.


Caveats:
 The windows respond to triple click currently.
 Interface is a little jumpy.

Tested on ESP32/ ESP8266 and RPI Pico W.

</p>
<pre>

Installation:
 Ensure your microcontroller already has an IP address to use. 
 Copy udesktop.py to your microcontroller. 
 Then start the script by "import udesktop" or defining as main.py
 Copy the udesktop.html to your computer, launch in web browser 
 Select the settings from the Dropdown Menu and data fill the
  ip address of your microcontroller.
  
  Work in progress but works well in tandem with webrepl.
  
 </pre>
