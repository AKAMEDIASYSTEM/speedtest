#! /bin/bash
echo 'installing speedtest-barnacle now'
chmod +x expire.sh
cp speedtest-poller.service speedtest-avahi.service speedtest-resonator.service speedtest-blinker.service speedtest-server.service /etc/systemd/system
cp avahi-resonator.service /etc/avahi/services/
systemctl enable speedtest-poller.service speedtest-avahi.service speedtest-resonator.service speedtest-blinker.service speedtest-server.service
systemctl start speedtest-poller.service speedtest-avahi.service speedtest-resonator.service speedtest-blinker.service speedtest-server.service
systemctl | grep AKA
