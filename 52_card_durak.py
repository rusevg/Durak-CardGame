import os
import pygame
import random
from time import sleep
from intro import intro

intro()

# Playing music
file = r'mysound.mp3'
pygame.mixer.init()
track = pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)
os.system('cls||clear')

# Screen size
os.system("mode con cols=100 lines=15")

# Staff for creating cards
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
          '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
          'A': 14}
suits = ("\u2665", "\u2666", "\u2660", "\u2663")

ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10',
         'J', 'Q', 'K', 'A')


def list_for_attack_and_defence(hand):
    # Making a comfortable list for using in defending and attack funktion.
    # [[value,quantity,suits], [value,quantity,suits]...] and so on.
    global paired_cards
    paired_cards = []
    for i in hand.all_cards:
        if len(paired_cards) == 0:
            paired_cards.append([i.value, 1, [i.suit]])
        elif i.value == paired_cards[-1][0]:
            paired_cards[-1][1] += 1
            paired_cards[-1][2].append(i.suit)
        else:
            paired_cards.append([i.value, 1, [i.suit]])


def fit_multipairs(paired_cards, trump_card, suit='',
                   card_range=[2, 8, 1], defending='off'):
    # Looking for good pairs to beat or attack
    global appropriate_pair
    so_so_cards = []
    appropriate_pair = 0
    if defending == 'off':
        for i in range(card_range[0], card_range[1], card_range[2]):
            for j in paired_cards:
                if i == j[0] and j[1] == 4:
                    appropriate_pair = j[0]
                    return appropriate_pair
                elif i == j[0] and j[1] == 3:
                    appropriate_pair = j[0]
                    return appropriate_pair
                elif i == j[0] and j[1] > 1 and trump_card.suit not in j[2]:
                    appropriate_pair = j[0]
                    return appropriate_pair
    else:
        appropriate_pair = []
        for i in range(card_range[0], card_range[1], card_range[2]):
            for j in paired_cards:
                if i == j[0] and j[1] == 4:
                    appropriate_pair.append(j)
                    return appropriate_pair
                elif i == j[0] and j[1] == 3 and suit in j[2]:
                    appropriate_pair.append(j)
                    return appropriate_pair
                elif i == j[0] and j[1] == 2 and suit in j[2]:
                    so_so_cards.append(j)
        if len(so_so_cards) > 0:
            appropriate_pair.append(so_so_cards[0])
            return appropriate_pair
    return appropriate_pair


def count_scores(i, occurrences, trump_card,
                 trump_corrector, simple_corrector):
    # Count main scores of hand
    global total_hand_value
    global values_of_cards
    if total_hand_value is None:
        values_of_cards = []
        total_hand_value = 0
    if i.value in values_of_cards:
        while i.value in values_of_cards:
            occurrences += 1
            values_of_cards.remove(i.value)
        for j in range(occurrences):
            values_of_cards.append(i.value)
        if occurrences == 1:
            if i.suit == trump_card.suit:
                total_hand_value += trump_corrector[1]
            total_hand_value += simple_corrector[1]
            values_of_cards.append(i.value)
        elif occurrences == 2:
            if i.suit == trump_card.suit:
                total_hand_value += trump_corrector[2]
            total_hand_value += simple_corrector[2]
            values_of_cards.append(i.value)
        elif occurrences == 3:
            if i.suit == trump_card.suit:
                total_hand_value += trump_corrector[3]
            total_hand_value += simple_corrector[3]
            values_of_cards.append(i.value)
    else:
        if i.suit == trump_card.suit:
            total_hand_value += trump_corrector[0]
        total_hand_value += simple_corrector[0]
        values_of_cards.append(i.value)
    return total_hand_value, values_of_cards


def hand_analise(suits, player, trump_card):
    # Function which return value of hand, ordered hand
    global total_hand_value
    total_hand_value = None
    bot_sorted = []
    suits_list = []
    a_suit, b_suit, c_suit = [], [], []
    for i in list(suits):
        if i != trump_card.suit:
            suits_list.append(i)
    # Main scores for every card
    for i in player.all_cards:
        occurrences = 0
        if i.value < 8:
            count_scores(i, occurrences, trump_card,
                         (14, 14, 14, 14), (-2, 1, 4, 8))
        elif i.value <= 10:
            count_scores(i, occurrences, trump_card,
                         (12, 12, 12, 12), (1, 3, 8, 12))
        else:
            count_scores(i, occurrences, trump_card,
                         (9, 9, 9, 9), (8, 12, 17, 23))
        if i.suit == suits_list[0]:
            a_suit.append(i)
        elif i.suit == suits_list[1]:
            b_suit.append(i)
        else:
            c_suit.append(i)
        # Making ordered hand
        if len(bot_sorted) == 0:
            bot_sorted.append(i)
        else:
            if i.value < bot_sorted[0].value:
                bot_sorted.insert(0, i)
            elif i.value >= bot_sorted[(len(bot_sorted) - 1)].value:
                bot_sorted.insert((len(bot_sorted)), i)
            else:
                for j in bot_sorted:
                    if (i.value >= j.value and i.value <=
                            bot_sorted[(bot_sorted.index(j) + 1)].value):
                        bot_sorted.insert((bot_sorted.index(j) + 1), i)
                        break
    # Counting taxes for more than 1 card with one suit
    monosuit_tax = 0
    for i in a_suit, b_suit, c_suit:
        if len(i) == 2:
            for j in i:
                if j.value >= 10:
                    monosuit_tax += 0
                else:
                    monosuit_tax += -3
        elif len(i) == 3:
            for j in i:
                if j.value > 10:
                    monosuit_tax += -2
                else:
                    monosuit_tax += -6
        elif len(i) >= 4:
            for j in i:
                if j.value > 10:
                    monosuit_tax += -3
                else:
                    monosuit_tax += -8
    if total_hand_value is None:
        total_hand_value = 0
    # Correcting scores according to amount of cards bot has
    num_factor = len(bot_sorted) / 6
    total_hand_value = (total_hand_value + monosuit_tax) / num_factor
    list_for_attack_and_defence(player)
    player.replace_hand(bot_sorted)
    list_for_attack_and_defence(player)
    return total_hand_value, player


class Card:
    # Main card class
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + "" + self.suit

    def display_card(self):
        return self.rank + "" + self.suit


class Deck:
    # Main deck class
    def __init__(self):
        self.all_cards = []
        self.shown_cards = []
        for suit in suits:
            for rank in ranks:
                # Create the Card Object
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def kozyr(self):
        c = self.all_cards.pop()
        self.all_cards.insert(0, c)
        return c

    def deck_num(self):
        return len(self.all_cards)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Player():
    # Main player class
    def __init__(self, name):
        self.name = name
        self.all_cards = []
        self.status = ''
        self.finish_status = False

    def lowest_card(self, trump):
        lowest = 15
        for i in self.all_cards:
            if i.suit == trump.suit:
                if i.value < lowest:
                    lowest = i.value
        return lowest

    def cards_num(self):
        x = len(self.all_cards)
        return x

    def remove_one(self, index):
        return self.all_cards.pop(index)

    def add_cards(self, new_cards):
        if isinstance(new_cards, type([])):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

    def discover_hand(self):
        phc = 'You have next cards: '
        count_dh = 0
        for i in self.all_cards:
            count_dh += 1
            phc += ('{}({}) '.format(count_dh, i))
        print(phc)

    def replace_hand(self, r_list):
        self.all_cards.clear()
        self.all_cards = r_list


def going_through_round(ordered_list, game, new_deck, players_without_cards):
    # Function that include main round logic, correct order of player's and decide who is who.
    # Turn defender correction
    if ordered_list[1] not in game.zero_list:
        defender = ordered_list.pop(1)
    elif ordered_list[2] not in game.zero_list:
        defender = ordered_list.pop(2)
    else:
        defender = ordered_list.pop(3)
    # Main round loop
    while True:
        for i in ordered_list:
            while True:
                if len(game.attack_cards) < (
                        len(defender.all_cards) + len(game.beaten_cards)):
                    ttemp = len(game.attack_cards)
                    os.system('cls||clear')
                    display_info(i, defender)
                    if i != human_player or (
                            i == human_player and i not in game.zero_list):
                        whose_turn(i, defender)
                    else:
                        human_player.finish_status = True
                    if (ttemp != len(game.attack_cards)
                            and defender.finish_status is not None):
                        os.system('cls||clear')
                        display_info(i, defender)
                        whose_turn(defender, defender)
                        if defender.finish_status is not None:
                            round_finish_status_nulled(list_of_players)
                            if human_player in game.zero_list:
                                human_player.finish_status = True
                    elif ttemp == len(game.attack_cards):
                        break
                else:
                    print('Defender cant take more!')
                    for i in ordered_list:
                        i.finish_status = True
                    break
        c_trues = 0
        for i in list_of_players:
            if i.finish_status is True:
                c_trues += 1
        if c_trues == (3 - players_without_cards):
            if defender.finish_status is None:
                defender.add_cards(game.attack_cards)
                defender.add_cards(game.beaten_cards)
            game.clear_attack_cards()
            game.clear_beaten_cards()
            break
    for i in ordered_list:
        if i.cards_num() < 6:
            fill_hands(new_deck, i)
    if defender.finish_status is not None and defender.cards_num() < 6:
        fill_hands(new_deck, defender)
    ordered_list.insert(1, defender)
    # Sorting player's list
    if new_deck.deck_num() == 0:
        for i in ordered_list:
            if i.cards_num() == 0:
                if i not in game.zero_list:
                    game.list_of_players_zero_cards_add(i)
    if len(game.zero_list) <= 1:
        if ordered_list[2] not in game.zero_list:
            next_after_defender = ordered_list[2]
        else:
            next_after_defender = ordered_list[3]
    else:
        if (((ordered_list[0] in game.zero_list) and (defender in game.zero_list)) or
            ((ordered_list[0] in game.zero_list) and (ordered_list[3] in game.zero_list)) or
                ((ordered_list[1] in game.zero_list) and (ordered_list[3] in game.zero_list))):
            next_after_defender = ordered_list[2]
        elif (((defender in game.zero_list) and (ordered_list[2] in game.zero_list)) or
              ((ordered_list[0] in game.zero_list) and (ordered_list[2] in game.zero_list))):
            next_after_defender = ordered_list[3]
        elif ((ordered_list[2] in game.zero_list) and (ordered_list[3] in game.zero_list)):
            next_after_defender = ordered_list[0]

    if defender.finish_status is None or defender in game.zero_list:
        rotation(ordered_list, next_after_defender)
    elif defender not in game.zero_list:
        rotation(ordered_list, defender)

    round_finish_status_nulled(list_of_players)
    player_status(list_of_players)
    return ordered_list


def display_info(attacker, defender):
    # Display all necessary information for game
    string1 = 'Players: '
    for i in list_of_players:
        string1 += (i.name + '({})'.format(i.cards_num()) + ' ')
    string1 += ('||| Trump card is: ' + trump_card.display_card()
                + '  ||| Cards left: ' + str(new_deck.deck_num()))
    print(string1)
    print('{} ||| {} is attacking'.format(
            game.print_attack_cards(), attacker.name))
    print('{} ||| {} is defending'.format(
        game.print_beaten_cards(), defender.name))
    human_player.discover_hand()
    print('--------------------------------------------------------------------')


class Game_round:
    # Main game class
    def __init__(self):
        self.status_list = [player_one.finish_status, player_two.finish_status,
                            player_three.finish_status, human_player.finish_status]
        self.attack_cards = []
        self.beaten_cards = []
        self.zero_list = []

    def change_status(self, status, index):
        self.status_list[index] = status

    def clear_attack_cards(self):
        self.attack_cards = []

    def clear_beaten_cards(self):
        self.beaten_cards = []

    def add_attack_card(self, card):
        self.attack_cards.append(card)

    def add_beaten_cards(self, card):
        self.beaten_cards.append(card)

    def list_of_players_zero_cards_add(self, player):
        self.zero_list.append(player)

    def print_beaten_cards(self):
        if len(self.beaten_cards) > 0:
            pbc = 'There are beaten cards on the table: '
            for i in self.beaten_cards:
                pbc += (i.display_card() + ' ')
            return pbc
        else:
            return 'There are no beaten cards'

    def print_attack_cards(self):
        if len(self.attack_cards) > 0:
            pac = 'There are attack cards on the table: '
            for i in self.attack_cards:
                pac += (i.display_card() + ' ')
            return pac
        else:
            return 'There are no attack cards'


def player_status(list_of_players):
    human_player.status = ''
    player_one.status = ''
    player_two.status = ''
    player_three.status = ''
    return list_of_players


def round_finish_status_nulled(list_of_players):
    player_one.finish_status = False
    player_two.finish_status = False
    player_three.finish_status = False
    human_player.finish_status = False
    return list_of_players


def first_move(first, second, third, fourth):
    # Searching for player with the lowest trump card for first move
    global lwst_player
    print('first_move')
    lwst = 15
    for i in [first, second, third, fourth]:
        if i.lowest_card(trump_card) < lwst:
            lwst = i.lowest_card(trump_card)
            lwst_player = i
    return lwst_player


def rotation(list_for_rotation, n_s_e):
    # Rotation of player's list(for correct turn)
    global ordered_list
    index = list_for_rotation.index(n_s_e)
    ordered_list = list_for_rotation[index:] + list_for_rotation[:index]


def fill_hands(deck, player):
    # Taking cards from deck and put it into player's hands
    if deck.deck_num() >= (6 - player.cards_num()):
        for x in range(6 - player.cards_num()):
            player.add_cards(deck.deal_one())
        return player, deck
    elif deck.deck_num() >= 1:
        for x in range(deck.deck_num()):
            player.add_cards(deck.deal_one())
        return player, deck
    else:
        pass


def human_move(human_player, game, trump, suits):
    # Main function for human player
    # Human's move, if it's his turn, start round
    if len(game.attack_cards) == 0:
        print('Its your turn to attack! Choice cards.')
        while True:
            num = input('Enter a number of Card you would like to use: ')
            if num.isdigit():
                if int(num) in range(human_player.cards_num() + 1):
                    break
        human_player.status = 'attacking'
        human_player.finish_status = True
        rtx = int(num) - 1
        game.add_attack_card(human_player.remove_one(rtx))

    # Adding cards on the table, continue round
    elif (human_player.status == 'attacking' or
          ('defending' in [player_one.status, player_two.status, player_three.status])):
        while True:
            temporary_value = False
            num = (input("Enter a namber of the card you'd like to use to make him "
                         "suffer, or put 'N' here if you have nothing to add: "))
            if num.isdigit():
                if int(num) in range(1, (human_player.cards_num() + 1)):
                    for i in (game.attack_cards + game.beaten_cards):
                        if i.value == human_player.all_cards[(int(num) - 1)].value:
                            temporary_value = True
                            human_player.finish_status = True
                            game.add_attack_card(human_player.remove_one((int(num) - 1)))
                            break
                    if temporary_value is False:
                        print('You should use another one!')
            if num.capitalize() == 'N':
                human_player.finish_status = True
                break
            if temporary_value:
                break
    # Defence
    elif len(game.beaten_cards) == 0 or human_player.status == 'defending':
        human_player.status = 'defending'
        while True:
            num = input(
                'Enter a number of Card you would like to use or "take" if you cant: ')
            if num == 'take':
                human_player.finish_status = None
                break
            elif num.isdigit():
                if int(num) in range(1, human_player.cards_num() + 1):
                    # Suit match check
                    if (game.attack_cards[(len(game.attack_cards) - 1)].suit
                            == human_player.all_cards[(int(num) - 1)].suit):
                        # Checking is this card value greater
                        if (game.attack_cards[(len(game.attack_cards) - 1)].value
                                < human_player.all_cards[(int(num) - 1)].value):
                            game.add_beaten_cards(
                                human_player.remove_one((int(num) - 1)))
                            break
                    # Checking the possibility of beating a regular card with a trump card
                    elif (game.attack_cards[(len(game.attack_cards) - 1)].suit
                          != trump.suit):
                        if human_player.all_cards[(
                                int(num) - 1)].suit == trump.suit:
                            game.add_beaten_cards(
                                human_player.remove_one((int(num) - 1)))
                            break
                    else:
                        print('You cant beat this way')


def bot_move(turn, ordered_list, new_deck, game, trump_card, defender, suits):
    # Bot logic is here
    # Check if there is defender
    turn_index = list_of_players.index(turn)
    list_of_players.pop(turn_index)
    some_defender = False
    for i in list_of_players:
        if i.status == 'defending':
            some_defender = True
    list_of_players.insert(turn_index, turn)
    # Bot attack, there are no cards on the table
    if len(turn.all_cards) == 0:
        turn.finish_status = True
        return turn
    hand_analise(suits, turn, trump_card)
    if len(game.attack_cards) == 0:
        # Looking for pairs up to 7
        fit_multipairs(paired_cards, trump_card)
        if appropriate_pair > 0:
            for i in turn.all_cards:
                if i.value == appropriate_pair and i.suit != trump_card.suit:
                    turn.status = 'attacking'
                    turn.finish_status = True
                    game.add_attack_card(turn.remove_one(
                        turn.all_cards.index(i)))
                    return game
        # If bot has too bad or too well cards he use pairs from 8 to 10
        if total_hand_value > 50 or total_hand_value < 25:
            fit_multipairs(paired_cards, trump_card, suit='',
                           card_range=[8, 11, 1], defending='off')
            if appropriate_pair > 0:
                for i in turn.all_cards:
                    if i.value == appropriate_pair and i.suit != trump_card.suit:
                        turn.status = 'attacking'
                        turn.finish_status = True
                        game.add_attack_card(turn.remove_one(
                            turn.all_cards.index(i)))
                        return game
        # If previous statements does not survive bot uses the worst card to attack
        min_el = 15
        for i in turn.all_cards:
            if min_el == 15:
                if i.value < min_el and i.suit != trump_card.suit:
                    min_el = i
            elif i.value < min_el.value and i.suit != trump_card.suit:
                min_el = i
        if min_el == 15:
            min_el = turn.all_cards[0]
        turn.status = 'attacking'
        turn.finish_status = True
        game.add_attack_card(turn.remove_one(turn.all_cards.index(min_el)))

    # Bot is adding attack cards
    elif some_defender is True or turn.status == 'attacking':
        # Looking for players to destroy
        bot_index = ordered_list.index(turn)
        # There are 4 players
        agression = None
        if len(game.zero_list) == 0:
            if bot_index <= 1:
                agression = True
            else:
                agression = False
        # There are 3 players
        elif len(game.zero_list) == 1:
            if bot_index == 0:
                agression = False
            else:
                agression = True
        # There are only 2 players
        else:
            agression = True
        # Loking for minimal simple and trump card to add
        min_add_simple_card = None
        min_add_trump_card = None
        for i in game.attack_cards + game.beaten_cards:
            for j in turn.all_cards:
                if i.value == j.value:
                    if j.suit != trump_card.suit:
                        if min_add_simple_card is None:
                            min_add_simple_card = j
                        elif j.value < min_add_simple_card.value:
                            min_add_simple_card = j
                    else:
                        if min_add_trump_card is None:
                            min_add_trump_card = j
                        elif j.value < min_add_trump_card.value:
                            min_add_trump_card = j
        # How many players says that they have nothing to add
        counter_finishes = 0
        for i in ordered_list:
            if i.finish_status is True:
                counter_finishes += 1
        # If it is necessary to destroy opponent and he is not going to
        # surrender yet
        if agression is True and defender.finish_status is not None:
            if min_add_simple_card is not None:
                game.add_attack_card(turn.remove_one(
                    turn.all_cards.index(min_add_simple_card)))
                turn.finish_status = True
            elif min_add_trump_card is not None:
                if len(game.zero_list) == 0:
                    if counter_finishes == 2:
                        game.add_attack_card(
                            turn.remove_one(turn.all_cards.index(
                                min_add_trump_card)))
                        turn.finish_status = True
                    else:
                        turn.finish_status = True
                else:
                    game.add_attack_card(turn.remove_one(
                        turn.all_cards.index(min_add_trump_card)))
                    turn.finish_status = True
            else:
                turn.finish_status = True
        # If defender is not going to surrender or it is not necessary to
        # destroy him but he surrender
        elif (defender.finish_status is None and
              agression is True) or (agression is False and
                                     defender.finish_status is None):
            if min_add_simple_card is not None:
                if min_add_simple_card.value < 11:
                    game.add_attack_card(turn.remove_one(
                        turn.all_cards.index(min_add_simple_card)))
                    turn.finish_status = True
                    return turn.finish_status
                elif (min_add_simple_card.value <= 13 and
                      total_hand_value > 50 and new_deck.deck_num() == 0):
                    game.add_attack_card(turn.remove_one(
                        turn.all_cards.index(min_add_simple_card)))
                    turn.finish_status = True
                    return turn.finish_status
                else:
                    turn.finish_status = True
            else:
                turn.finish_status = True
        elif agression is False and defender.finish_status is not None:
            turn.finish_status = True

    # Bot in defence
    elif len(game.beaten_cards) == 0 or turn.status == 'defending':
        turn.status = 'defending'
        # Searching for minimal simple and trump card for defence
        if turn.finish_status is not None:
            min_beat_card = game.attack_cards[-1]
            for i in turn.all_cards:
                if i.suit == game.attack_cards[-1].suit:
                    if i.value > game.attack_cards[-1].value:
                        if min_beat_card == game.attack_cards[-1]:
                            min_beat_card = i
                        elif i.value < min_beat_card.value:
                            min_beat_card = i
            if min_beat_card == game.attack_cards[-1]:
                min_beat_card = None
                for i in turn.all_cards:
                    if i.suit == trump_card.suit:
                        if min_beat_card is None:
                            if game.attack_cards[-1].suit == trump_card.suit:
                                if i.value > game.attack_cards[-1].value:
                                    min_beat_card = i
                            else:
                                min_beat_card = i
                        else:
                            if (i.value < min_beat_card.value and
                                    game.attack_cards[-1].suit != trump_card.suit):
                                min_beat_card = i
                            elif (game.attack_cards[-1].suit == trump_card.suit
                                  and i.value > game.attack_cards[-1].value and
                                  i.value < min_beat_card.value):
                                min_beat_card = i
            # If there is nothing to use
            if min_beat_card is None:
                turn.finish_status = None
            else:
                # Looking for pairs which would be useful for defence, case
                # when there are no beaten cards
                if len(game.beaten_cards) == 0:
                    if min_beat_card.suit == trump_card.suit:
                        game.add_beaten_cards(turn.remove_one(
                            turn.all_cards.index(min_beat_card)))
                    else:
                        smart_defend(min_beat_card, game)
                        if def_value == 0:
                            game.add_beaten_cards(turn.remove_one(
                                turn.all_cards.index(min_beat_card)))
                        else:
                            for i in turn.all_cards:
                                if i.value == def_value and i.suit == game.attack_cards[-1].suit:
                                    game.add_beaten_cards(
                                        turn.remove_one(turn.all_cards.index(i)))
                else:
                    # Case when there are beaten cards, bot is trying to beat
                    # using card values which already on the table
                    temp_table_values = []
                    temp_trump = None
                    for i in game.attack_cards + game.beaten_cards:
                        temp_table_values.append(i.value)
                    for i in turn.all_cards:
                        if i.value in temp_table_values:
                            if (i.suit == game.attack_cards[-1].suit and i.value > game.attack_cards[-1].value):
                                game.add_beaten_cards(turn.remove_one(turn.all_cards.index(i)))
                                return game
                            elif (game.attack_cards[-1].suit != trump_card.suit
                                  and i.suit == trump_card.suit and temp_trump is None):
                                temp_trump = i
                            elif (game.attack_cards[-1].suit == trump_card.suit and
                                  game.attack_cards[-1].value < i.value and i.suit == trump_card.suit):
                                game.add_beaten_cards(
                                    turn.remove_one(turn.all_cards.index(i)))
                                return game
                    # If there is only trump card he uses it
                    if temp_trump is not None:
                        game.add_beaten_cards(turn.remove_one(
                            turn.all_cards.index(temp_trump)))
                        return game
                    # If there are no tricky ways to beat he uses what he can
                    else:
                        game.add_beaten_cards(turn.remove_one(
                            turn.all_cards.index(min_beat_card)))


def smart_defend(min_beat_card, game):
    # Looking for good ways to use paired cards for defence
    global def_value
    def_value = 0
    fit_multipairs(paired_cards, trump_card, game.attack_cards[-1].suit,
                   card_range=[(game.attack_cards[-1].value + 1), 14, 1], defending='on')
    if len(appropriate_pair) > 0:
        if appropriate_pair[0][0] == min_beat_card.value:
            return min_beat_card
        elif (game.attack_cards[-1].value < 9 and appropriate_pair[0][0]
              in range(game.attack_cards[-1].value, 10)):
            def_value = appropriate_pair[0][0]
            return def_value
        elif appropriate_pair[0][0] in range(game.attack_cards[-1].value,
                                             (game.attack_cards[-1].value + 3)):
            def_value = appropriate_pair[0][0]
            return def_value
        else:
            return min_beat_card


def loose_check(deck, players_list):
    # Looking for players who finished game, and check is game finished
    c = 0
    if deck.deck_num() == 0:
        for player in players_list:
            if player.cards_num() == 0:
                c += 1
    if c >= 3:
        return False
    else:
        return True


def who_start(trump_card, list_of_players):
    # Decide who will go first
    global min_player
    min_trump = trump_card
    min_player = None
    for i in list_of_players:
        for j in i.all_cards:
            if min_trump == trump_card:
                if j.suit == min_trump.suit:
                    min_trump = j
                    min_player = i
            else:
                if j.suit == min_trump.suit:
                    if j.value < min_trump.value:
                        min_trump = j
                        min_player = i
    return min_player, min_trump


def whose_turn(player, defender):
    # Function which defines is it bot or human
    if player in [player_one, player_two, player_three]:
        return bot_move(player, ordered_list, new_deck,
                        game, trump_card, defender, suits)
    else:
        return human_move(human_player, game, trump_card, suits)


def game_start_setap():
    # Setup new game
    global player_one
    global player_two
    global player_three
    global human_player
    global list_of_players
    global new_deck
    global round_num
    global players_without_cards
    player_one = Player('HuAnan')
    player_two = Player('Atermiter')
    player_three = Player('Machinist')
    print('\n\n\n\n\n')
    player_name = input('\t\t\t\t  Enter your name dude ')
    human_player = Player(player_name)
    list_of_players = [player_one, player_two, player_three, human_player]
    players_without_cards = 0
    round_num = 1
    new_deck = Deck()
    new_deck.shuffle()
    new_deck.shuffle()
    new_deck.shuffle()
    round_finish_status_nulled(list_of_players)
    player_status(list_of_players)


# Main game loop
game_on = True
while game_on:
    os.system('cls||clear')
    game_start_setap()
    # Taking cards / trump card
    if round_num == 1:
        for i in list_of_players:
            fill_hands(new_deck, i)
        trump_card = new_deck.kozyr()
    game = Game_round()
    who_start(trump_card, list_of_players)
    ordered_list = list_of_players.copy()
    rotation(list_of_players, min_player)

    while loose_check(new_deck, ordered_list):
        going_through_round(ordered_list, game, new_deck,
                            players_without_cards)
    game_dro = True
    for i in ordered_list:
        if i.cards_num() > 0:
            os.system('cls||clear')
            print('{} has lost!'.format(i.name))
            game_dro = False
    if game_dro:
        os.system('cls||clear')
        print('Looks like game dro!')
    while True:
        inpt = input('Would you like to try again? Y/N ')
        if inpt.capitalize() == 'Y':
            break
        elif inpt.capitalize() == 'N':
            game_on = False
            break


print('See You =)')
sleep(3)
