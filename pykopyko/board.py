#-*- coding: utf-8 -*-

# External imports
import functools

# Internal imports (if any)


@functools.total_ordering
class Ration:

    def __init__(self, cost, worms):
        self.__cost = cost
        self.__worms = worms

    @property
    def cost(self):
        return self.__cost

    @property
    def worms(self):
        return self.__worms

    def __eq__(self, other):
        return self.__cost == other.__cost

    def __lt__(self, other):
        return self.__cost < other.__cost

    def __str__(self):
        return '[{} | {}]'.format(self.__cost, self.__worms)


class Board:

    def __init__(self):
        self.__grill = []
        self.__trash_bin = []
        self.__stacks = {}
        self.__available_rations = None

    @property
    def grill(self):
        return self.__grill

    @property
    def stacks(self):
        return self.__stacks

    @property
    def available_rations(self):
        if self.__available_rations is None:
            self.__available_rations = [(None, r) for r in self.__grill] + \
                                       [(p, s[-1]) for p, s in self.__stacks.items() if s]
        return self.__available_rations

    def __str__(self):
        scores = [(p, sum((r.worms for r in s))) for p, s in self.__stacks.items()]
        scores.sort(key=lambda x: x[1], reverse=True)
        return '\n'.join(['', '*** SCORECARD ***'] +
                         ['Player {!s}: {} worms'.format(p, s) for p, s in scores] +
                         ['', 'Trash bin: {}'.format(', '.join(map(str, self.__trash_bin)))])

    def reset(self, players):
        self.__grill = [Ration(x, (x - 17) // 4) for x in range(21, 37)]
        self.__trash_bin = []
        self.__stacks = {p: [] for p in players}
        self.__available_rations = None

    def move_ration(self, ration, player):
        """
        Moves the given ration to the given player.

        :param ration: ration to be moved.
        :param player: destination player.
        :return: the source of the movement. None if it's the grill.
        :raise: ValueError if the ration is not found in the grill nor in the player stacks.
        """
        self.__available_rations = None
        player_stack = self.__stacks[player]
        if ration in self.__grill:
            self.__grill.remove(ration)
            player_stack.append(ration)
            return
        for p, stack in self.__stacks.items():
            if p is player:
                continue
            if stack and ration == stack[-1]:
                player_stack.append(stack.pop())
                return p
        raise ValueError('Ration {!s} can be found on the board'.format(ration))

    def lose_ration(self, player):
        """
        The topmost ration from player is moved to the grill.

        :param player: player losing a ration.
        :return: the ration lost.
        """
        self.__available_rations = None
        player_stack = self.__stacks[player]
        if player_stack:
            ration_lost = player_stack.pop()
            self.__grill.append(ration_lost)
            return ration_lost

    def discard_ration(self):
        """
        Discard a ration from the grill.

        :return: the ration discarded.
        """
        self.__grill.sort()
        ration_discarded = self.__grill.pop()
        self.__trash_bin.append(ration_discarded)
        return ration_discarded


class BoardView:

    def __init__(self, board):
        self.__board = board

    @property
    def grill(self):
        return self.__board.grill[:]

    @property
    def stacks(self):
        return {p: s for p, s in self.__board.stacks}

    @property
    def available_rations(self):
        return self.__board.available_rations[:]
