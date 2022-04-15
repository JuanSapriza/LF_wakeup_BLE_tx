from adafruit_ble import BLERadio

ble = BLERadio()
print("scanning")
found = set()
scan_responses = set()
for advertisement in ble.start_scan():
    if advertisement.complete_name:
        if advertisement.complete_name not in found:
            found.add(advertisement.complete_name)
            print("ID: "+advertisement.complete_name+" | "+str(advertisement.rssi)+"dBi")
            print(found)
