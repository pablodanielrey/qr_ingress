#!/bin/bash
rm -R /home/qr/.config/google-chrome
rm -R /home/qr/.cache/google-chrome
mkdir -p /home/qr/.config/google-chrome
touch /home/qr/.config/google-chrome/First\ Run
READY=`curl -sL -w "%{http_code}" "http://10.107.73.172/" -o /dev/null`
while [ "$READY" != "200" ];
do
	sleep 10s;
	READY=`curl -sL -w "%{http_code}" "http://10.107.73.172/" -o /dev/null`
done
/usr/bin/i3
