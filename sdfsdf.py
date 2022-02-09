
class inv:
    def __init__(self):
        self.backpack = []
        self.selected_Item = -1
        self.item = {}
        # for item in range(3):
            # self.add(randrange(0,4))


    def item_exist(self, item):
        use_item = 0
        if self.item: use_item = (self.item['id']==item['id'])*1
        finditem = next((x for x in self.backpack if x['id'] == item['id']), {'id':0,'count':0})
        return(finditem['count']-use_item>item['count']-1)
        
    def exist(self, items):
        for block in items:
            if not self.item_exist(block):
                return(False)
        return(True)

    def add_item(self, block):
        finditem = next((x for x in self.backpack if x['id'] == block['id']), False)
        if finditem:
            finditem['count'] += block['count']
        else:
            self.backpack.append(block)
            

    def delete_item(self, block):
        finditem = next((x for x in self.backpack if x['id'] == block['id']), False)
        if not finditem: return
        if finditem['count']==block['count']: 
            self.backpack.remove(finditem)
        elif finditem['count'] > block['count']:
            finditem['count'] -= block['count']

    def delete(self, items):
        for block in items:
            self.delete_item(block)
            
    def insert(self, items):
        for block in items:
            self.add_item(block)
        
        
inventory = inv()

inventory.backpack = [{"id":1, "count":10}, {"id":2, "count":1}]
inventory.item = {}

need_items2 = [{"id":2, "count":1}] #{"id":1, "count":0}, {"id":2, "count":0}
need_items1 = [{"id":1, "count":2}]


print(inventory.backpack)
inventory.insert(need_items2)
inventory.insert(need_items2)
inventory.insert(need_items2)
inventory.insert(need_items2)
inventory.insert(need_items2)
print(inventory.backpack)