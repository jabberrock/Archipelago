from BaseClasses import Item, Region, Location, Entrance, Tutorial
from ..AutoWorld import World, WebWorld
from .ItemTemplates import item_template_by_name
from .Locations import location_by_unique_name


class TunicWebWorld(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Tunic Setup Guide",
            description="A guide to connect Tunic to Archipelago",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Jabberrock"]
        )
    ]


class TunicWorld(World):
    game = "Tunic"
    topology_present = True
    data_version = 0
    web = TunicWebWorld()

    item_name_to_id = {}
    start_id = 1000
    for item_name in item_template_by_name:
        item_name_to_id[item_name] = start_id
        start_id += 1

    location_name_to_id = {}
    start_id = 2000
    for location_name in location_by_unique_name:
        location_name_to_id[location_name] = start_id
        start_id += 1

    def create_item(self, name: str) -> Item:
        return TunicItem(
            name,
            item_template_by_name[name].item_classification,
            self.item_name_to_id[name],
            self.player
        )

    def create_items(self) -> None:
        item_pool = []
        for item_name in item_template_by_name:
            item_template = item_template_by_name[item_name]
            for i in range(item_template.num_checks):
                item_pool.append(self.create_item(item_template.name))

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
