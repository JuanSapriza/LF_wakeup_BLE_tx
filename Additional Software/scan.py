from adafruit_ble import BLERadio

ble = BLERadio()
print("scanning")
found = set()
scan_responses = set()
i = 0
while True:
    for advertisement in ble.start_scan(interval=0.05):
        if advertisement.complete_name: 
            if advertisement.complete_name not in found:
                found.add(advertisement.complete_name)
                print(str(i)+" ID: "+advertisement.complete_name+" | "+str(advertisement.rssi)+"dBi")
                ble.stop_scan()
                i = i+1
            else:
                ble.stop_scan()
                i = i+1
                
            
