from enum import Enum


class ModelName(Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


fake_items_db = [
    {'item_name': 'Foo'},
    {'item_name': 'Bar'},
    {'item_name': 'Baz'}
]

items_dict = {'items': [{'item_id': 'Foo'}, {'item_id': 'Bar'}]}
