from adafruit_ble import BLERadio
from datetime import datetime

ble = BLERadio()
print("scanning")
found = set()


for ad in ble.start_scan():
    #addr = ad.address
    #if ad.scan_response and addr not in scanResponses:
    if ad.complete_name:
        if ad.complete_name not in found:
            found.add(ad.complete_name)
        print(repr(ad))
        print("ID: "+ad.complete_name+" | "+str(ad.rssi)+"dBi | " + datetime.now().strftime("%M:%S.%f") )
    

