speedtest
=========

An ambient device that displays the current network quality

A python script regularly runs "speedtest-cli --simple" and keeps a running average of the results. The awesome speedtest-cli tool I'm using is from here: https://github.com/sivel/speedtest-cli

An LED strip will show a color on the red-to-green spectrum; the color will be porportional to the most recent DL speed

The ping time will be mapped to the angle of the LED bar

The UL speed might get mapped to a subtle pulsing effect on teh LDE strip, but I'm not sure pleasant that will be to live with...

Heavily uses the awesome speedtest-cli tool (thanks!)
Will also use the BBB-GPIO library that Adafruit points to

