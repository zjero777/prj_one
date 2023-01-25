from storage import *

items = [
    {'id':3, 'count':10},
    {'id':1, 'count':100},
    {'id':3, 'count':100},
    {'id':1, 'count':10},
    {'id':3, 'count':100},
    {'id':1, 'count':100},
]

list_allow = [
    {'id':1, 'count':50},
    {'id':3, 'count':30},
    {'id':6, 'count':80},
]

in_storage = [
    {'id':3, 'count':0},
    {'id':1, 'count':30}
]

in_storage_allows = [
    {'id':3, 'count':50},
    {'id':1, 'count':50}
]
recipe = [
    {'id':1, 'count':1},
    {'id':2, 'count':2},
    {'id':3, 'count':1}
]

def sort_by_recipe(in_storage, recipe):
    sorted_storage = sorted(in_storage, key=lambda x: recipe.index(next(filter(lambda y: y['id'] == x['id'], recipe))))
    return sorted_storage   


def check_recipe_and_storage(storage: storage, recipe):
    if storage.cells is None: return False
    for s in storage.cells:
        if s['count']==0: continue # можно использовать ячейку любого вила если в ней нет ничего
        for r in recipe:
            if s['id'] == r['id']: break
        else:
            return False
    else:
        return True
                        
        
    #         find_cell, allowcount = storage.is_allow_item(r)
    #         if find_cell == -1:
    #             return(False)
        
    #     else: 
    #         storage.cells.append({'id':-1,'count':0})
    #         storage.allows.append({'id':-1,'count':200})
    #     if len(storage.cells)>len(recipe):
    #         return(False)
    #     else:
    #         return True
    # return True

def sort_by_recipe(storage, recipe):
    sorted_storage = sorted(storage, key=lambda x: recipe.index(next((y for y in recipe if y.get('id') == x.get('id')), None)) if next((y for y in recipe if y.get('id') == x.get('id')), None) else -1)
    return sorted_storage

in_storage = storage(None, None, list_items=in_storage, list_allows=in_storage_allows)

print(f'\033[95min_storage: {in_storage.cells}\033[0m')
print(f'\033[94mrecipe: {recipe}\033[0m')
if check_recipe_and_storage(in_storage, recipe):
    print('Ok - Items do not need to be thrown away')
    cells = sort_by_recipe(in_storage.cells, recipe)

    print(f'\033[95min_storage: {cells}\033[0m')
    print(f'\033[94mrecipe: {recipe}\033[0m')
   
else:
    print('Error - Items need to be thrown away! Purge enable')






