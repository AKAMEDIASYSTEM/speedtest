#! /bin/bash
echo 'installing speedtest-barnacle now'
cp speedtest-poller.service speedtest-resonator.service speedtest-blinker.service speedtest-server.service /etc/systemd/system
cp avahi-resonator.service /etc/avahi/services/
systemctl enable speedtest-poller.service speedtest-resonator.service speedtest-blinker.service speedtest-server.service
systemctl start speedtest-poller.service speedtest-resonator.service speedtest-blinker.service speedtest-server.service
systemctl | grep AKA
