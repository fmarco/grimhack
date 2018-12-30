# -*- coding: utf-8 -*-
import os

from entities import Hero
from levels import Level
from helpers import getchar

class App(object):

    running = False
    hero = None
    levels = {}
    max_levels = 10
    difficulty = 1
    level_ref = None

    def game_loop(self):
        while self.running:
            action = raw_input("Type an action: ")
            try:
                getattr(self.hero, action, None)()
            except TypeError, Exception:
                print 'Not a valid command!'
                _ = raw_input("")
            if self.hero.is_dead:
                print 'You lose'
                self.stop()
            self.refresh()

    def draw(self):
        self.hero.show_stats()
        self.level_ref.draw()

    def refresh(self):
        os.system('clear')
        self.draw()
        self.level_ref.move_enemies()

    def game_prepare(self, *args, **kwargs):
        init_values = {}
        init_values['hero_attrs'] = kwargs.pop('hero_attrs', {})
        self.hero = Hero(**init_values)
        for i in range(self.difficulty):
            self.levels[i] = Level(**{'name': 'level_{0}'.format(i)})
            self.levels[i].load_map('./test_level.json')
        self.level_ref = self.levels[0]
        self.hero.register(self.level_ref)
        self.level_ref.put(self.hero, 1, 1)

    def start(self, *args, **kwargs):
        init_values = {}
        self.running = True
        hero_name = raw_input("Please enter hero's name: ")
        hero_attrs = {'name': hero_name}
        init_values['hero_attrs'] = hero_attrs
        self.game_prepare(**init_values)
        self.draw()
        self.game_loop()

    def stop(self, message=None):
        self.running = False
        if message:
            print message
