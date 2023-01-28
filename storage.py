class storage:
    def __init__(self, app, owner, count=0, list_items_with_allows=[]):
        '''
        app - game class
        owner - owner class
        count - cell count universal 
        list_items - add items
        where:
            {'id':1, 'count':1}
            id - id item  (-1  cell any items type allow)
            count - item count (0 - empty)
            allow_count - allow item count (-1 any store count)
        '''
        self.app = app
        self.owner = owner
        self.count = count
        if not list_items_with_allows:
            self.cells = [{'id':-1, 'count':0, 'allow_count':-1} for i in range(0, count)]
        else:
            self.cells = list_items_with_allows.copy()
            self.count = len(list_items_with_allows)

        self.ui = storage_ui(app, self)

    def is_allow_item(self, item):
        find_cell = -1
        allow_count = -1
        id = item['id']
        count = item['count']
        for num, cell in enumerate(self.cells):
            if cell==-1: 
                if cell['id']==-1 or cell['id']==id:
                    find_cell = num
                else: 
                    continue
                if cell['allow_count']==-1:
                    allow_count = count
                    break
                else:
                    allow_count = min(cell['allow_count'], count)
                    break
            elif self.cells[num]['id']==id:
                find_cell = num
                if cell['allow_count']==-1 or (cell['id']==id and cell['count']>=count+self.cells[num]['count']):
                    allow_count = count
                    break
                else:
                    allow_count = cell['allow_count']-self.cells[num]['count']
                    break
            else: continue
        return(find_cell, allow_count)
           
    def add_items(self, list_items):
        not_fit = [] #items not fit on storage and return
        for item in list_items:
            find_cell, allow_count = self.is_allow_item(item)
            if find_cell==-1:
                self.add_item(not_fit, item)
            elif allow_count<0:
                self.add_item(not_fit, item)
            elif allow_count<item['count']:
                self.add_item_to_cell(find_cell, {'id':item['id'],'count':allow_count})
                self.add_item(not_fit, {'id':item['id'], 'count':item['count']-allow_count})
            else:
                self.add_item_to_cell(find_cell, {'id':item['id'],'count':allow_count})

        return(not_fit)
         
    def add_item_to_cell(self, num, item):
        self.cells[num] = {'id':item['id'], 'count':item['count']+self.cells[num]['count'], 'allow_count':self.cells['allow_count']}

    def add_item(self, list, new_item):
        for item in list:
            if item['id']==new_item['id']:
                item['count'] += new_item['count']
                return
        list.append(new_item)

    def update(self):
        self.ui.update()
    
    def draw(self):
        self.ui.draw()

    def is_need_purge_by_recipe(self, recipe)->bool:
        if self.cells is None: return False
        for s in self.cells:
            if s['count']==0: continue # можно использовать ячейку любого вила если в ней нет ничего
            for r in recipe:
                if s['id'] == r['id']: break
            else:
                return False
        else:
            return True

    def sort_by_recipe(self, recipe):
        self.cells = sorted(self.cells, key=lambda x: recipe.index(next((y for y in recipe if y.get('id') == x.get('id')), None)) if next((y for y in recipe if y.get('id') == x.get('id')), None) else -1)
        
    def remove_non_recipe_cells(self, recipe):
        self.cells = list(filter(lambda x: any(y['id'] == x['id'] for y in recipe), self.cells))
        
    def append_recipe_cells(self, recipe):
        storage_ids = [x['id'] for x in self.cells]
        for item in recipe:
            if item['id'] not in storage_ids:
                self.cells.append({'id': item['id'], 'count': 0, 'allow_count': item['count']*10})
                
        return storage        

class storage_ui:
    def __init__(self, app, storage):
        self.app = app
        self.storage = storage
        
    def update(self):
        pass
    
    def draw(self):
        pass


