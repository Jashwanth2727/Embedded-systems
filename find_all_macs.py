import asyncio
from bleak import BleakScanner

# Define known naming patterns for your specific hardware
DEVICE_FILTERS = ["BP", "OXY", "THERM"]

async def discover_devices():
    print("--- Starting BLE Scan for Health Kiosk ---")
    print("Ensure devices are in Pairing/Advertising mode...")
    
    devices = await BleakScanner.discover()
    
    found_devices = []
    
    for d in devices:
        # Check if device name matches our sensors
        if d.name and any(f in d.name.upper() for f in DEVICE_FILTERS):
            print(f"MATCH FOUND: {d.name} | MAC: {d.address} | RSSI: {d.rssi}")
            found_devices.append((d.name, d.address))
            
    if not found_devices:
        print("No matching health sensors found. Check device power/advertising.")
    else:
        print(f"\nScan complete. Found {len(found_devices)} devices.")

if __name__ == "__main__":
    try:
        asyncio.run(discover_devices())
    except KeyboardInterrupt:
        pass
