import csv
from dataclasses import dataclass
from pathlib import Path
from BaseClasses import ItemClassification


@dataclass
class TunicItemTemplate:
    name: str
    item_classification: ItemClassification
    num_checks: int


item_templates = []
item_template_by_name = {}

with open(Path(__file__).parent / "data" / "items.csv") as items_csv_file:
    csv_reader = csv.reader(items_csv_file)
    next(csv_reader)  # skip header
    for entry in csv_reader:
        item_template = TunicItemTemplate(
            name=entry[0],
            item_classification=getattr(ItemClassification, entry[1]),
            num_checks=int(entry[5])
        )
        item_templates.append(item_template)
        item_template_by_name[item_template.name] = item_template
