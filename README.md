speedtest
=========

An ambient device that displays the current network quality

A python script regularly runs "speedtest-cli --simple" and keeps a running average of the results. The awesome speedtest-cli tool I'm using is from here: https://github.com/sivel/speedtest-cli

An LED strip will show a color on the red-to-green spectrum; the color will be porportional to the most recent DL speed

The ping time will be mapped to the angle of the LED bar

The UL speed might get mapped to a subtle pulsing effect on the LED strip, but I'm not sure pleasant that will be to live with...

Heavily uses the awesome speedtest-cli tool (thanks!)

To run on BBB:
 * install Adafruit_BBIO (http://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black?view=all)
 * set up github ssh keys (I use ssh-keygen on a non-BBB machine and then transfer the id_rsa over to the BBB, it's much quicker than messing with Dropbear. However, this is the best/most helpful SSH thread: https://groups.google.com/forum/?fromgroups#!searchin/beagleboard/github/beagleboard/h6XiKjT9-ZI/xgA0kIGViKgJ)
 * clone speedtest-cli from here: https://github.com/sivel/speedtest-cli
 * make sure the speedtest-cli file itself is copied over to /usr/bin, so it's available in your PATH
 * ?
 * Profit!