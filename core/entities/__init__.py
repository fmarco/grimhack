# -*- coding: utf-8 -*-

import random

from ..base import Base

class Entity(Base):
    hp = 0
    attack = 0
    movement = 1
    level = None
    max_hp = 0

    def __init__(self, *args, **kwargs):
        self.abilities = {}
        self.actions = {}
        self.items = []
        self.name = kwargs.pop('name', 'Unknown')

    @property
    def is_dead(self):
        return self.hp <= 0

    def register(self, level):
        self.level = level

    def unregister(self, level):
        self.level = None

    def update_level(self, *args, **kwargs):
        action = kwargs.pop('action', {})
        self.level.update(**{'entity': self, 'action': action})

    def up(self):
        self.update_level(**{'action': ['up', self.movement]})

    def down(self):
        self.update_level(**{'action': ['down', self.movement]})

    def right(self):
        self.update_level(**{'action': ['right', self.movement]})

    def left(self):
        self.update_level(**{'action': ['left', self.movement]})


class Enemy(Entity):

    movements = {
        0: 'up',
        1: 'down',
        2: 'right',
        3: 'left'
    }

    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)

    def move(self):
        raise NotImplementedError


class Blob(Enemy):
    symbol = 'O'
    hp = 1
    attack = 2
    max_hp = 1
    rand_limit = 5

    def __init__(self, *args, **kwargs):
        super(Blob, self).__init__(*args, **{'name': 'Blob'})

    def move(self):
        index = random.randint(0, self.rand_limit)
        movement = self.movements.get(index, None)
        if movement:
            getattr(self, movement, None)()


class Hero(Entity):

    symbol = '@'
    hp = 10
    max_hp = 10
    attack = 5

    def __init__(self, *args, **kwargs):
        initial_attrs = kwargs.pop('hero_attrs', {})
        super(Hero, self).__init__(*args, **initial_attrs)

    def show_stats(self):
        print '    '
        print '    Name:   ', self.name
        print '    Hp:     ', self.hp
        print '    Attack: ', self.attack

    def show_inventory(self):
        print 'Inventory'
        if self.items:
            for i, item in enumerate(self.items):
                print '{0})'.format(i), item
            self.use_item()
        else:
            print 'Empty!'
        _ = raw_input('Press any key...')

    def use_item(self):
        choose = raw_input('Choose one item to use')
        try:
            ch = int(choose)
            item = self.items.pop(ch)
            print 'You used one {0} !'.format(item)
            item.use(self)
        except ValueError:
            pass
