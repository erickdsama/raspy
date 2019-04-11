#!/bin/bash

#    GPS script for Waveshare GSM/GPRS/GNSS/Bluetooth for Raspberry Pi hat
#    Copyright (C) 2018  Kari Karvonen
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

tty=/dev/ttyS0

function DecodeLine() {
	#echo ""
	#DESC=(GNSSrunstatus Fixstatus UTCdatetime latitude logitude altitude speedOTG course fixmode Reserved1 HDOP PDOP VDOP Reserverd2 GNSSsatellitesinview GNSSsatellitesused GLONASSsatellitesused Reserved3 cn0max HPA VPA)
	DATA="${1//+CGNSINF: /}"
	IFS=','
	echo $DATA
	#for i in $DATA; do
		#echo -n "  ${DESC[0]}"
	#	DESC=("${DESC[@]:1}")
		#echo -n " "
		#echo "$i"
	#done
}

function SerialWriteAndRead() {
	exec 4<$tty 5>$tty
        stty -F $tty 115200 
	echo "$1" >&5
	while IFS='' read -t 1 -r line || [[ -n "$line"  ]]; do
	    echo "$line"
	    if [[ "$line" == +CGNSINF* ]]; then
	    	DecodeLine "$line">> file.txt

	    fi
	done <&4
	stty stop undef
	
}

case "$1" in
	towertimesync)
		# Use time from cell tower. 
		# You need to physically poweroff and poweron hat after this
		# Without correct time GPS satellites are hard to find
		SerialWriteAndRead "AT+CLTS=1"
		SerialWriteAndRead "AT&W"
		;;
	poweron)
		# Power on GPS 
		SerialWriteAndRead "AT+CGNSPWR=1"
		;;
	poweroff)
		# Power off GPS
	        SerialWriteAndRead "AT+CGNSPWR=0"
	        ;;
	loc)
		# Location / postition
		#SerialWriteAndRead "AT+CGNSSEQ=\"RMC\""
		#SerialWriteAndRead "AT+CGNSURC=1"
		#SerialWriteAndRead "AT+CGNSTST=2"
		#SerialWriteAndRead "AT+CGNSSEQ"
		SerialWriteAndRead "AT+CGNSINF"
                ;;
	loc_service)
		while /bin/true; do
			SerialWriteAndRead "AT+CGNSINF"
			sleep 5
    		done &
		;;
	post)	
                
		SerialWriteAndRead 'AT+SAPBR=3,1,"Contype","GPRS"'
		SerialWriteAndRead 'AT+SAPBR=1,1'
		SerialWriteAndRead 'AT+SAPBR=2,1'
		SerialWriteAndRead 'AT+HTTPINIT '
		SerialWriteAndRead 'AT+HTTPPARA="CID",1'
		SerialWriteAndRead 'AT+HTTPPARA="URL","http://3a205aae.ngrok.io/location"'
		SerialWriteAndRead 'AT+HTTPPARA="CONTENT","application/json"' 
		SerialWriteAndRead 'AT+HTTPDATA=100,10000'
		sleep 10
		SerialWriteAndRead '{"lat":"30.4050", "lng": "-130.42323", "id_code":"Ax34b9"}'
                sleep 10
		SerialWriteAndRead 'AT+HTTPACTION=1'
		#SerialWriteAndRead "AT+CMGF=1"
		#SerialWriteAndRead "AT+CMGS=\"6562724890\""
		#SerialWriteAndRead "Hola mami"
		;;
	time)
		# Time
		SerialWriteAndRead "AT+CCLK?"
		;;
	status)
		# GPS timesync status
		SerialWriteAndRead "AT+CLTS?"
		# Power status
		SerialWriteAndRead "AT+CGNSPWR?"
		# GPS Fix status
		SerialWriteAndRead "AT+CGPSSTATUS?"
		;;
	*)
		echo "Simple GPS-script for Waveshare GSM/GPRS/GNSS/Bluetooth for Raspberry Pi hat"
		echo ""
		echo "$0  {loc|time|status|poweron|poweroff|towertimesync}"
		echo ""
		echo "See more info and AT command: https://www.waveshare.com/wiki/GSM/GPRS/GNSS_HAT"
		exit 1
		;;
esac
exit 0
