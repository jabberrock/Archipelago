import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class TunicLocation:
    scene_name: str
    check_type: str
    game_object_name: str
    position: str
    is_position_accurate: bool
    chest_id: Optional[int]
    unique_name: str


locations = []
location_by_unique_name = {}

with open(Path(__file__).parent / "data" / "locations.csv") as locations_csv_file:
    csv_reader = csv.reader(locations_csv_file)
    next(csv_reader)  # skip header
    for entry in csv_reader:
        location = TunicLocation(
            scene_name=entry[0],
            check_type=entry[1],
            game_object_name=entry[2],
            position=entry[3],
            is_position_accurate=(entry[4] == "1"),
            chest_id=int(entry[5]) if not entry[5].isspace else None,
            unique_name=entry[6]
        )
        locations.append(location)
        location_by_unique_name[location.unique_name] = location

# Add Well locations which activate when enough Coins are dropped into the well
for i in range(4):
    location = TunicLocation(
        scene_name="Well",
        check_type=f"Well Redeem #{i + 1}",
        game_object_name="Well",
        position="(0.0, 0.0, 0.0)",
        is_position_accurate=False,
        chest_id=None,
        unique_name=f"Well Redeem #{i + 1}"
    )
    locations.append(location)
    location_by_unique_name[location.unique_name] = location
