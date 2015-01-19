#-*- coding: utf-8 -*-

# External imports
import itertools
import logging
import random

# Internal imports (if any)
import pykopyko.board


class Game:

    symbols = ['1', '2', '3', '4', '5', 'W']
    worm_symbol = symbols[-1]
    __logger = logging.getLogger('pykopyko.game')

    def __init__(self):
        self.__players = []
        self.__board = pykopyko.board.Board()

    @property
    def board(self):
        return self.__board

    def add_player(self, player):
        self.__players.append(player)

    def run(self):
        players_number = len(self.__players)
        if not (2 <= players_number <= 7):
            raise ValueError('Invalid number of players ({}) to play the game'.format(players_number))
        self.__board.reset(self.__players)
        players_iter = itertools.cycle(self.__players)
        while len(self.__board.grill):
            next_player = next(players_iter)
            Game.__logger.info('Turn of player {!s}'.format(next_player))
            self.__turn(next_player)
        Game.__logger.info('Game finished\n{!s}'.format(self.__board))

    @staticmethod
    def valuation(dices):
        return sum((5 if s == Game.worm_symbol else int(s) for s in dices))

    def __turn(self, player):
        player_dices = []
        dices = [None] * 8
        while dices:
            dices = [random.choice(Game.symbols) for _ in range(len(dices))]
            self.__roll(player, dices)
            if not (set(dices) - set(player_dices)):
                Game.__logger.info('No symbols can be selected from last roll of player {!s}'.format(player))
                player_dices = []
                break
            selected_symbol, roll_again = player.process_roll(dices, player_dices[:])
            Game.__logger.info('Player {!s} selects symbol {}'.format(player, selected_symbol))
            if selected_symbol not in dices:
                Game.__logger.error('Invalid selected symbol {} from player {!s}'.format(selected_symbol, player))
                player_dices = []
                break
            if selected_symbol in player_dices:
                Game.__logger.error('Invalid already selected symbol {} from player {!s}'.format(
                    selected_symbol, player))
                player_dices = []
                break
            player_dices += [d for d in dices if d == selected_symbol]
            dices = [d for d in dices if d != selected_symbol]
            if not roll_again:
                Game.__logger.info('Player {!s} ends turn'.format(player))
                break
        score = Game.valuation(player_dices) if Game.worm_symbol in player_dices else None
        if score is None:
            self.__failed_turn(player, 'there are no worms')
            return
        else:
            Game.__logger.info('Player {!s} scores {} points'.format(player, score))
        selected_ration = player.process_score(score)
        if selected_ration:
            Game.__logger.info('Player {!s} selects ration {!s}'.format(player, selected_ration))
        else:
            self.__failed_turn(player, 'no ration were selected')
            return
        location = ration = None
        if selected_ration.cost > score:
            Game.__logger.error('Player {!s} selects ration {!s} with a cost higher than score ({})'.format(
                player, selected_ration, score))
            selected_ration = None
        else:
            for location, ration in self.__board.available_rations:
                if ration is selected_ration:
                    if location is player:
                        Game.__logger.error('Player {!s} selects ration {!s}, but already owns it'.format(
                            player, selected_ration))
                        selected_ration = None
                    elif location is not None and ration.cost != score:
                        Game.__logger.error(
                            'Player {!s} selects ration {!s} from player {!s} with a cost different than score ({})'
                            .format(player, selected_ration, location, score))
                        selected_ration = None
                    break
            else:
                Game.__logger.error('Player {!s} selects not available ration {!s}'.format(player, selected_ration))
                selected_ration = None
        if selected_ration is None:
            self.__failed_turn(player, 'an invalid ration was selected')
        else:
            self.__board.move_ration(selected_ration, player)
            self.__ration_movement(location, player, ration)

    def __failed_turn(self, player, reason=None):
        Game.__logger.info('Failed turn from player {!s}{}'.format(player,
                                                                   ' because {}'.format(reason) if reason else ''))
        player.process_score(None)
        lost_ration = self.__board.lose_ration(player)
        if lost_ration:
            self.__ration_movement(player, None, lost_ration)
        discarded_ration = self.__board.discard_ration()
        self.__ration_discarded(discarded_ration)

    def __notify(self, player, method_name, args):
        for p in self.__players:
            if p is player:
                continue
            getattr(p, method_name)(*args)

    def __roll(self, player, dices):
        Game.__logger.info('Player {!s} rolls {}'.format(player, ', '.join(dices)))
        self.__notify(player, 'roll', (player, dices))

    def __ration_movement(self, movement_src, movement_dst, ration):
        Game.__logger.info('Ration {!s} moved from {} to {}'.format(ration,
                                                                    movement_src or 'the grill',
                                                                    movement_dst or 'the grill'))
        self.__notify(None, 'ration_movement', (movement_src, movement_dst, ration))

    def __ration_discarded(self, ration):
        Game.__logger.info('Ration {!s} discarded'.format(ration))
        self.__notify(None, 'ration_discard', (ration, ))
