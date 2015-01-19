#-*- coding: utf-8 -*-

# External imports
import logging

# Internal imports (if any)
import pykopyko.game
import pykopyko.player


class SimpleBot(pykopyko.player.Player):

    name = 'SimpleBot'
    __logger = logging.getLogger('pykopyko.bots.SimpleBot')
    __dice_threshold = 3

    def __init__(self, name, board_view):
        pykopyko.player.Player.__init__(self, name, board_view)
        self.__end_turn()

    def process_roll(self, dices, separated_dices):
        """
        Process a roll and returns the dices you want to keep.

        :param dices: the list of dice's symbols.
        :param separated_dices: the list of dice's symbols separated so far.
        :return: a tuple with the number you want to keep and a boolean if you want to roll again.
        """
        self.__speak('I got {} from the dices'.format(', '.join(dices)))
        worm_symbol = pykopyko.game.Game.worm_symbol
        candidate_symbols = [d for d in dices if d not in separated_dices]
        if worm_symbol in candidate_symbols:
            self.__speak('I got some worms, I think I will get that')
            selected_symbol = worm_symbol
            new_points = 5 * dices.count(selected_symbol)
        else:
            counted_symbols = [(5 if s is worm_symbol else int(s) * candidate_symbols.count(s), s)
                               for s in candidate_symbols]
            counted_symbols.sort(reverse=True)
            self.__speak('I get {} points from symbol {}, I think it\'s OK'.format(*counted_symbols[0]))
            new_points, selected_symbol = counted_symbols[0]
        if worm_symbol not in separated_dices and selected_symbol is not worm_symbol:
            self.__speak('I don\'t have any worm, so I\'ll keep rolling')
            roll_again = True
        elif min((ration.cost for location, ration in self._board_view.available_rations if location is not self)) \
                > (pykopyko.game.Game.valuation(separated_dices) + new_points):
            self.__speak('I don\'t have enough points for any ration, so I\'ll keep rolling')
            roll_again = True
        else:
            self.__speak('I don\'t want to risk my actual points, I think I will get that')
            roll_again = sum((1 for s in dices if s != selected_symbol)) > SimpleBot.__dice_threshold
        return selected_symbol, roll_again

    def process_score(self, score):
        """
        Process an score, returning the ration from the board_view you want to get.

        :param score: the amount of points obtained from your last rolls. None if your rolls were invalid.
        :return: the ration instance you want if your score is not None.
        """
        self.__end_turn()
        if score is None:
            return
        candidates = []
        for location, ration in self._board_view.available_rations:
            if location is None and ration.cost > score:
                continue
            if location is self:
                continue
            if location is not None and ration.cost != score:
                continue
            candidates.append((ration, location))
        if candidates:
            candidates.sort(reverse=True)
            selected_ration, location = candidates[0]
            self.__speak('I select ration {!s} from {!s}'.format(selected_ration, location or 'the grill'))
            return selected_ration

    def roll(self, player, dices):
        """
        Informs you of a player's roll.

        :param player: the player instance that make the roll.
        :param dices: the list of dice's scores.
        """
        pass

    def ration_movement(self, movement_src, movement_dst, ration):
        """
        Informs you of a ration movement.

        :param movement_src: source of the movement. None if it's the grill.
        :param movement_dst: destination of the movement. None if it's the grill.
        :param ration: the ration being moved.
        """
        pass

    def ration_discard(self, ration):
        """
        Informs you of a ration discarded from the grill.

        :param ration: the ration discarded.
        """
        pass
    
    def __end_turn(self):
        self.__selected_symbols = set()
        self.__dices_count = 8
        
    def __speak(self, message):
        SimpleBot.__logger.info('[{}] {}'.format(self._name, message))


player_class = SimpleBot
