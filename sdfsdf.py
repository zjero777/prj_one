from storage import *
from factory import *
from data import *

items = [
    {'id':1, 'count':3}
]

in_storage = [
    {'id':1, 'count':0, 'allow_count':50},
    {'id':2, 'count':0, 'allow_count':50},
    {'id':3, 'count':30, 'allow_count':50}
]

recipe = [
    {'id':3, 'count':1},
    {'id':5, 'count':2},
    {'id':1, 'count':1}
]

data = data()
bp = data.get_fdata('name', 'brickyard')

factory = factory(0,data,bp,0,0)
factory.update()
factory.update()
factory.update()
factory.update()
factory.update()
factory.update()
factory.in_storage.add_items(items)
print('******IN_STORAGE***********************')
print(factory.in_storage.cells)
print('******PROD***********************')
print(factory.in_storage.inspect_resources(factory.incom_recipe))
factory.update()
factory.update()
factory.update()
print('******IN_STORAGE***********************')
print(factory.in_storage.cells)

   





