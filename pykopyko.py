#-*- coding: utf-8 -*-

# External imports
import importlib
import logging
import optparse
import sys

# Internal imports (if any)
import pykopyko.board
import pykopyko.bots
import pykopyko.game


class QBShFormatter(logging.Formatter):

    LEVEL_DICT = {'DEBUG': ' ', 'INFO': '*', 'WARNING': '!', 'ERROR': '!!', 'CRITICAL': '!!!'}

    def format(self, record):
        """
         Responsible for converting a LogRecord to a string.

        :param record: Log record to format.
        :return: a formatted log string.
        """
        return '[{}] {}'.format(QBShFormatter.LEVEL_DICT[record.levelname], record.getMessage())


# Main entry point
if __name__ == '__main__':
    usage = 'Usage: %prog [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-l', '--log-level', dest='log_level', default='INFO',
                      help='log level [INFO]')
    parser.add_option('-b', '--bot', dest='bots', default=[], action='append',
                      help='bot player (can be specified more than one time)')
    # programName, _ = os.path.splitext(sys.argv[0])
    options, args = parser.parse_args()

    logging_format = '%(asctime)s %(levelname)s %(message)s'
    numeric_level = getattr(logging, options.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        print('ERROR: Invalid log level: {}'.format(options.log_level))
        sys.exit(1)

    # Define logging
    logging.basicConfig(format=logging_format, level=numeric_level, filemode='w')

    # Create a game object
    game = pykopyko.game.Game()

    # Create the players
    players = []
    for i, bot in enumerate(options.bots):
        player_class = importlib.import_module('pykopyko.bots.{}'.format(bot)).player_class
        game.add_player(player_class('Player{}'.format(i + 1), pykopyko.board.BoardView(game.board)))

    # Run the game!
    game.run()
