from storage import *
from factory import *
from data import *

items = [
    {'id':3, 'count':10},
    {'id':1, 'count':100},
    {'id':3, 'count':100},
    {'id':1, 'count':10},
    {'id':3, 'count':100},
    {'id':1, 'count':100},
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
factory = factory(0,0,bp,0,0)

in_storage = storage(None, None, len(recipe))
in_storage.append_recipe_cells(recipe)
in_storage.sort_by_recipe(recipe)



   





