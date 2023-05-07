import csv
from pathlib import Path
from BaseClasses import Item, Region, Location, Entrance, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld
from dataclasses import dataclass

class TunicWebWorld(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Tunic',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Jabberrock']
        )
    ]


@dataclass
class TunicItemTemplate:
    name: str
    item_classification: ItemClassification
    num_checks: int
    

class TunicWorld(World):
    game = "Tunic"
    topology_present = True
    data_version = 0
    web = TunicWebWorld()

    # Load items from data file
    item_list = {}
    with open(Path(__file__).parent / "data" / "items.csv") as items_csv_file:
        csv_reader = csv.reader(items_csv_file)
        next(csv_reader)  # skip header
        for entry in csv_reader:
            item_name = entry[0]
            item_classification = getattr(ItemClassification, entry[1])
            num_checks = int(entry[5])
            item_list[item_name] = TunicItemTemplate(item_name, item_classification, int(num_checks))

    # Create item to ID mapping
    item_name_to_id = {}
    start_id = 1000
    for item_name in item_list:
        item_name_to_id[item_name] = start_id
        start_id += 1

    # Load locations from data file and create location to ID mapping
    location_name_to_id = {}
    start_id = 2000
    with open(Path(__file__).parent / "data" / "locations.csv") as locations_csv_file:
        csv_reader = csv.reader(locations_csv_file)
        next(csv_reader)  # skip header
        for entry in csv_reader:
            is_valid = entry[3] == "1"
            if is_valid:
                location_name = entry[4]
                location_name_to_id[location_name] = start_id
                start_id += 1

    # Add Well locations which activate when enough Coins are dropped in
    for i in range(4):
        location_name_to_id[f"Well - Redeem #{i + 1}"] = start_id
        start_id += 1

    def create_item(self, name: str) -> Item:
        tunic_item = TunicItem(
            name,
            self.item_list[name].item_classification,
            self.item_name_to_id[name],
            self.player
        )
        return tunic_item

    def create_items(self):
        item_pool = []
        for item_name in self.item_list:
            item = self.item_list[item_name]
            for i in range(item.num_checks):
                tunic_item = TunicItem(
                    item.name,
                    item.item_classification,
                    self.item_name_to_id[item.name],
                    self.player
                )
                item_pool.append(tunic_item)

        self.multiworld.random.shuffle(item_pool)
        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        return 'Some Money'

    def create_regions(self):
        menu_region = Region('Menu', self.player, self.multiworld)
        menu_to_tunic_entrance = Entrance(self.player, 'Tunic', menu_region)
        menu_region.exits.append(menu_to_tunic_entrance)

        tunic_region = Region('Tunic', self.player, self.multiworld)
        for location_name in self.location_name_to_id:
            location = TunicLocation(self.player, location_name, self.location_name_to_id[location_name], tunic_region)
            tunic_region.locations.append(location)

        menu_to_tunic_entrance.connect(tunic_region)

        self.multiworld.regions += [
            menu_region,
            tunic_region
        ]


class TunicItem(Item):
    game = "Tunic"


class TunicLocation(Location):
    game = "Tunic"
