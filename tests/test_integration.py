import json
from helpers import arg_parse
import os

class TestIntegration():
    def test(self, tmp_path, mocker):
        locations_data = [
            {"location_id": 1, "location_name": "Headquarters", "parent_location_id": None},
            {"location_id": 2, "location_name": "Branch Office", "parent_location_id": 1},
            {"location_id": 3, "location_name": "Remote Site", "parent_location_id": 2}
        ]
        
        devices_data = [
            {"device_id": 1, "device_name": "Main Server", "location_id": 1, "status": "active"},
            {"device_id": 2, "device_name": "Backup Server", "location_id": 1, "status": "active"},
            {"device_id": 3, "device_name": "Workstation", "location_id": 2, "status": "inactive"}
        ]
        
        events_data = [
            {"event_id": 1, "device_id": 1, "event_type": "startup", "timestamp": "2023-01-01"},
            {"event_id": 2, "device_id": 2, "space_occupied": 'false', "timestamp": "2023-01-02"},
            {"event_id": 3, "device_id": 3, "motion_detected": 'true', "timestamp": "2023-01-03"}
        ]
        
        locations_file = tmp_path / "test_locations.json"
        devices_file = tmp_path / "test_devices.json"
        events_file = tmp_path / "test_events.json"

        for path, data in [
            (locations_file, locations_data),
            (devices_file, devices_data),
            (events_file, events_data)
        ]:
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        
        mocker.patch('sys.argv', [
            'src/main.py',
            '--locations', str(locations_file),
            '--devices', str(devices_file),
            '--events', str(events_file),
            '--format', 'json'
        ])

        args = arg_parse()

        assert args.locations == str(locations_file)
        assert args.devices == str(devices_file)
        assert args.events == str(events_file)
        assert args.format == 'json'

        assert os.path.exists(args.locations)
        assert os.path.exists(args.devices)
        assert os.path.exists(args.events)

        for path in [args.locations, args.devices, args.events]:
            with open(path, 'r') as f:
                content = json.load(f)
                assert isinstance(content, list)