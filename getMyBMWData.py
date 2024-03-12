
import asyncio
import sys
import os
import json
from bimmer_connected.account import MyBMWAccount
from bimmer_connected.api.regions import Regions
from bimmer_connected.vehicle.vehicle import VehicleViewDirection
from bimmer_connected.vehicle.doors_windows import LockState

async def main(email, password, vin, region):
    if (region == 'cn'):
        region = Regions.CHINA
    elif (region == 'us'):
        region = Regions.NORTH_AMERICA
    else:
        region = Regions.REST_OF_WORLD

    account = MyBMWAccount(email, password, region)
    await account.get_vehicles()
    vehicle = account.get_vehicle(vin)

    filename = 'modules/MMM-MyBMW/car-' + vin + '.png'
    if (not os.path.isfile(filename)):
        image_data = await vehicle.get_vehicle_image(VehicleViewDirection.FRONTSIDE)
        with open(filename, 'wb') as file:
            file.write(image_data)
            file.close()

    data = {
        'updateTime': vehicle.vehicle_location.vehicle_update_timestamp.isoformat(),
        'mileage': vehicle.mileage.value,
        'doorLock': (vehicle.doors_and_windows.door_lock_state == LockState.LOCKED) or (vehicle.doors_and_windows.door_lock_state == LockState.SECURED),
        'fuelRange': vehicle.fuel_and_battery.remaining_range_fuel.value,
        'electricRange': vehicle.fuel_and_battery.remaining_range_electric.value,
        'chargingLevelHv': vehicle.fuel_and_battery.remaining_battery_percent,
        'connectorStatus': vehicle.fuel_and_battery.is_charger_connected,
        'vin': vehicle.vin,
        'imageUrl': filename
    }

    print(json.dumps(data))
    sys.stdout.flush()

region = 'rest'
if (len(sys.argv) > 4):
    region = sys.argv[4]
if (len(sys.argv) < 4):
    print('Usage: python getMyBMWData.py <email> <password> <vin> <region:us|cn|rest>')
else:
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3], region))