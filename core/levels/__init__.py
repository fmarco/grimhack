import json

from ..base import Base
from ..entities import Entity, Hero, Enemy, Blob
from ..exceptions import NoMovementException, BattleFinishedException
from ..helpers import get_entity_instance, EMPTY, SPACE
from ..items import Item, Potion


class Wall(Base):
    symbol = '#'


class Coffer(Base):

    symbol = 'M'

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

    action = {
        'up': ('x', -1),
        'down': ('x', 1),
        'right': ('y', 1),
        'left': ('y', -1),
    }

    def __init__(self, *args, **kwargs):
        self.coordinates = {}
        self.level_map = []
        self.enemies = []
        self.name = kwargs.pop('name', 'Unknown level')
        self.x = kwargs.pop('x', self.x)
        self.y = kwargs.pop('y', self.y)

    def initialize_map(self):
        self.level_map = [[None] * self.y for i in range(self.x)]

    def load_map(self, path=None):
        if path:
            with open(path) as data_file:
                data = json.load(data_file)
                self.name = data['name']
                self.x = len(data['map'])
                self.y = len(data['map'][0])
                self.initialize_map()
                for i, row in enumerate(data['map']):
                    for j, column in enumerate(row):
                        symbol = data['map'][i][j]
                        instance = get_entity_instance(symbol)
                        self.level_map[i][j] = instance
                        if isinstance(instance, Enemy):
                            instance.register(self)
                            self.coordinates[instance] = {
                                'x': i,
                                'y': j
                            }
                            self.enemies.append(self.level_map[i][j])

    def draw(self):
        print SPACE
        print SPACE
        for i, row in enumerate(self.level_map):
            print SPACE,
            print SPACE,
            row_list = []
            for j, column in enumerate(row):
                if not self.level_map[i][j]:
                    row_list.append(EMPTY)
                else:
                    row_list.append(self.level_map[i][j].symbol)
            print SPACE.join(row_list)
        print SPACE
        print SPACE

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
                        self.fight(
                            attacker=entity,
                            defender=target
                        )
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
        except BattleFinishedException as e:
            print e

    def fight(self, attacker, defender):
        while True:
            defender.hp = defender.hp - attacker.attack
            if defender.is_dead:
                if isinstance(defender, Enemy):
                    x = self.coordinates[defender]['x']
                    y = self.coordinates[defender]['y']
                    self.level_map[x][y] = None
                    del self.coordinates[defender]
                    self.enemies.remove(defender)
                    self.draw()
                raise BattleFinishedException
            attacker, defender = defender, attacker


    def add_entity_at_coordinates(self, entity, x, y):
        self.coordinates[entity] = {
            'x': x,
            'y': y,
        }
        self.level_map[x][y] = entity

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()
