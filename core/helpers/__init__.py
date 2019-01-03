EMPTY = '.'
SPACE = ' '

def get_entity_instance(symbol):
   from ..entities import Hero, Blob
   from ..levels import Coffer, Wall
   tiles = {
      Wall.symbol: Wall,
      Hero.symbol: Hero,
      Blob.symbol: Blob,
      Coffer.symbol: Coffer,
      EMPTY: None,
   }
   _class = tiles.get(symbol)
   return _class() if _class else None


def getchar():
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch
