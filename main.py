
__author__ = "Brett Duncan"
__copyright__ = "Copyright 2019"
__credits__ = []
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"
__status__ = "Development"


import sys

from tictactoe import tictactoe
from connectfour import connectfour


def main():

    # needs at least game type and
    assert len(sys.argv) > 2, 'required parameters missing'

    # choose the game to play
    if sys.argv[1] == 'tictactoe':
        play = tictactoe.play
    elif sys.argv[1] == 'connectfour':
        play = connectfour.play
    else:
        raise ValueError('invalid game selected')

    player1 = sys.argv[2]

    if len(sys.argv) == 3:
        player2 = player1
    else:
        player2 = sys.argv[3]

    # play the game
    play(player1, player2)


if __name__ == '__main__':
    main()