from ..entities import Hero, Enemy
from ..levels import Wall

tiles = {
    '#': Wall,
    '@': Hero,
    'X': Enemy,
    '.': None,
}

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