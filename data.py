import json

class data:
    def __init__(self) -> None:
        f = open('data/data.json', encoding='utf-8')
        self.data = json.load(f)
        f.close
        
    def get_bdata(self, key, stroke):
        for item in self.data.get('block_type'):
            if item[key] == stroke:
                return(item)

    def get_tdata(self, key, stroke):
        for item in self.data.get('terrain_type'):
            if item[key] == stroke:
                return(item)

    def get_fdata(self, key, stroke):
        for item in self.data.get('factory_type'):
            if item[key] == stroke:
                return(item)
    
