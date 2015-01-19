#-*- coding: utf-8 -*-

# External imports

# Internal imports (if any)


class Player:

    def __init__(self, name, board_view):
        self._name = name
        self._board_view = board_view

    def __str__(self):
        return self._name

    def process_roll(self, dices, separated_dices):
        """
        Process a roll and returns the dices you want to keep.

        :param dices: the list of dice's symbols.
        :param separated_dices: the list of dice's symbols separated so far.
        :return: the number you want to keep or None if you want to stop.
        """
        raise NotImplementedError

    def process_score(self, score):
        """
        Process an score, returning the ration from the board_view you want to get.

        :param score: the amount of points obtained from your last rolls. None if your rolls were invalid.
        :return: the ration instance you want if your score is not None.
        """
        raise NotImplementedError

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
