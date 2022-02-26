class waterfalls:
    def __init__(self, app):
        self.app = app
        self.list = []

    def update(self):
        for item in self.list:
            if item.active:
                item.update()

        for item in self.list:
            if not item.active:
                i = self.list.pop(self.list.index(item))
                del i

    def add(self, pos):
        wf = water_fall(self.app, pos)
        self.list.append(wf)


class water_fall:
    def __init__(self, app, pos):
        self.pos = pos
        self.app = app
        self.timer = app.timer
        self.time = self.timer.get_ticks()
        self.active = True

    def update(self):
        if self.timer.get_ticks()-self.time > 5000:
            terra = self.app.terrain
            if terra.field[self.pos] == terra.GetTData('name', 'pit')['id']:
                terra.field[self.pos] = terra.GetTData('name', 'water')['id']
                self.next_water_fall((self.pos[0]-1, self.pos[1]))
                self.next_water_fall((self.pos[0]+1, self.pos[1]))
                self.next_water_fall((self.pos[0], self.pos[1]-1))
                self.next_water_fall((self.pos[0], self.pos[1]+1))

            self.active = False
            del self

    def next_water_fall(self, pos):
        terra = self.app.terrain
        if terra.onMap(pos[0], pos[1]):
            if terra.field[pos] == terra.GetTData('name', 'pit')['id']:
                self.app.water_falls.add(pos)
