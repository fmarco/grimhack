from ..base import Base

class Item(Base):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')

    def use(self):
        pass


class Potion(Item):

    heal = 1

    def __init__(self, *args, **kwargs):
        super(Potion, self).__init__(*args, **{'name': 'Potion'})

    def use(self, entity):
        max_heal = entity.max_hp - entity.hp
        if self.heal > max_heal:
            entity.hp = entity.max_hp
        else:
            entity.hp += self.heal