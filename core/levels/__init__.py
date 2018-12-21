import json

from ..base import Base
from ..entities import Entity, Hero, Enemy, Blob
from ..exceptions import NoMovementException
from ..items import Item, Potion


class Wall(Base):

    symbol = '#'


class Coffer(Base):

    symbol = 'M'
    items = []

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', 'Unknown Coffer')
        self.items = kwargs.pop('items', [Potion()])

    def show_items(self, entity):
        if self.items:
            for i, item in enumerate(self.items):
                print '{0})'.format(i), item
            choose = raw_input('Choose one or All object...')
            try:
                ch = int(choose)
                item = self.items.pop(ch)
                print 'You got one {0} !'.format(item)
                entity.items.append(item)
            except ValueError:
                if choose == 'All':
                    entity.items.extend(self.items)
                    self.items = []
        else:
            print 'Empty!'
            _ = raw_input('Press any key...')

    def auto_fill(self):
        pass


class Level(Base):

    x = 20
    y = 20
    coordinates = {}
    level_map = []
    enemies = []

    action = {
        'up': ('x', -1),
        'down': ('x', 1),
        'right': ('y', 1),
        'left': ('y', -1),
    }

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', 'Unknown level')
        self.x = kwargs.pop('x', self.x)
        self.y = kwargs.pop('y', self.y)
        self.generate_map()

    def generate_map(self):
        self.level_map = [[None] * self.y for i in range(self.x)]

    def load_map(self, path=None):
        if path:
            with open(path) as data_file:
                data = json.load(data_file)
                self.name = data['name']
                self.x = len(data['map'])
                self.y = len(data['map'][0])
                self.generate_map()
                for i, row in enumerate(data['map']):
                    for j, column in enumerate(row):
                        if data['map'][i][j] == '#':
                            self.level_map[i][j] = Wall()
                        elif data['map'][i][j] == '.':
                            self.level_map[i][j] = None
                        elif data['map'][i][j] == 'M':
                            self.level_map[i][j] = Coffer()
                        elif data['map'][i][j] == 'O':
                            enemy = Blob()
                            self.level_map[i][j] = enemy
                            enemy.register(self)
                            self.coordinates[enemy] = {
                                'x': i,
                                'y': j
                            }
                            self.enemies.append(self.level_map[i][j])

    def draw(self):
        print ' '
        print ' '
        for i, row in enumerate(self.level_map):
            print ' ',
            print ' ',
            row_list = []
            for j, column in enumerate(row):
                if not self.level_map[i][j]:
                    row_list.append('.')
                else:
                    row_list.append(self.level_map[i][j].symbol)
            print ' '.join(row_list)
        print ' '
        print ' '

    def update(self, *args, **kwargs):
        entity = kwargs.pop('entity', None)
        action = kwargs.pop('action', None)
        axis, mul = self.action.get(action[0])
        offset = entity.movement * mul
        move_to = self.coordinates.get(entity)[axis] + offset
        old_x = self.coordinates.get(entity)['x']
        old_y = self.coordinates.get(entity)['y']
        if axis == 'x':
            y = old_y
            x = move_to
        elif axis == 'y':
            x = old_x
            y = move_to
        try:
            target = self.level_map[x][y]
            if not isinstance(target, Wall):
                if isinstance(target, Entity):
                    if isinstance(entity, Hero) or isinstance(target, Hero):
                        self.battle(entity, target)
                # elif isinstance(target, Item) and isinstance(entity, Hero):
                #     entity.items.append(target)
                #     del self.coordinates[target]
                elif isinstance(target, Coffer):
                    if isinstance(entity, Hero):
                        target.show_items(entity)
                    raise NoMovementException
                else:
                    self.level_map[x][y] = entity
                    self.coordinates[entity]['x'] = x
                    self.coordinates[entity]['y'] = y
                    self.level_map[old_x][old_y] = None
        except NoMovementException as e:
            print e

    def battle(self, entity_a, entity_b):
        turn = 0
        end = False
        while not end:
            if turn == 0:
                entity_b.hp = entity_b.hp - entity_a.attack
                if entity_b.hp <= 0:
                    end = True
                turn = 1
            else:
                entity_a.hp = entity_a.hp - entity_b.attack
                if entity_a.hp <= 0:
                    end = True
                turn = 0

    def put(self, entity, x, y):
        self.coordinates[entity] = {
            'x': x,
            'y': y,
        }
        self.level_map[x][y] = entity

    def move_enemies(self):
        for enemy in self.enemies:
            if enemy.is_dead:
                x = self.coordinates[enemy]['x']
                y = self.coordinates[enemy]['y']
                self.level_map[x][y] = None
                del self.coordinates[enemy]
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
        for enemy in self.enemies:
            enemy.move()