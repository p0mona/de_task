from src.helpers import arg_parse
import pytest


@pytest.mark.parametrize(
    "argv, locations, devices, events, format",
    [
        (
            [
                "main.py",
                "--locations",
                "data/locations.py",
                "--devices",
                "data/devices.py",
                "--events",
                "data/events.py",
                "--format",
                "json",
            ],
            "data/locations.py",
            "data/devices.py",
            "data/events.py",
            "json",
        ),
        (
            [
                "main.py",
                "--locations",
                "data/locations.py",
                "--devices",
                "data/devices.py",
                "--events",
                "data/events.py",
                "--format",
                "xml",
            ],
            "data/locations.py",
            "data/devices.py",
            "data/events.py",
            "xml",
        ),
    ],
)
def test_arg_parse(mocker, argv, locations, devices, events, format):
    mocker.patch("sys.argv", argv)

    args = arg_parse()
    assert args.locations == locations
    assert args.devices == devices
    assert args.events == events
    assert args.format == format
