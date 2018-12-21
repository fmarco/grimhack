# -*- coding: utf-8 -*-

class Base(object):

    name = ''
    symbol = ''

    def __str__(self):
        return self.name if self.name else 'Unknown'

    @property
    def symbol(self):
        return self.symbol