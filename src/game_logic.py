# AI group project
# Jenny Rotelli & Matthew McKnight
# 
# Game logic - entity interactions and AI implimentation

import enum
import random
import itertools
import copy
from operator import itemgetter


# (max_health, max_intimidation, max_defense)
DEFAULT_MAX_STATS = (100, 8, 8)
BUFF_COOLDOWN = 5

class MoveType(enum.Enum):
    ATTACK = 0
    HEAL = 1
    DEFEND = 2
    INTIMIDATE = 3


class State(enum.Enum):
    AGGRESSIVE = 0
    DEFENSIVE = 1
    BALANCED = 2


MOVES = {
        # name : (type, power)
        "slash":(MoveType.ATTACK, 10),
        "potion":(MoveType.HEAL, 9),
        "sheild":(MoveType.DEFEND, 4),
        "scare":(MoveType.INTIMIDATE, 3) }


class Stats:
    def __init__(self, health, intimidation, defense):
        self.health = health
        self.intimidation = intimidation
        self.defense = defense

class Entity:
    def __init__(self, name, max_stats=None):
        self.name = name 
        if max_stats is None:
            max_stats = Stats(*DEFAULT_MAX_STATS)
        self.max_stats = max_stats
        self.health = self.max_stats.health

        self._intimidation = [0] * BUFF_COOLDOWN
        self._defense = [0] * BUFF_COOLDOWN
        
        self.moveset = MOVES

        # we start without a controller, add one later
        self.controller = None

    @property
    def intimidation(self):
        return sum(self._intimidation)

    @property
    def defense(self):
        return sum(self._defense)

    def __repr__(self):
        return '{}:\n\tHealth: {}/{}\n\tIntimidation: {}/{}\n\tDefense: {}/{}\n'.format(
                self.name,
                self.health,
                self.max_stats.health,
                self.intimidation,
                self.max_stats.intimidation,
                self.defense,
                self.max_stats.defense)

    def be_hit(self, strength):
        damage = max(strength - self.defense, 0)
        self.health = self.health - damage
        return damage

    def be_healed(self, strength):
        heal_amt = _cap(self.health, strength, self.max_stats.health, 0)
        self.health = self.health + heal_amt
        return heal_amt

    def be_defended(self, strength):
        defense_amt = _cap(self.defense, strength, self.max_stats.defense, 0)
        self._defense[0] = defense_amt
        return defense_amt

    def be_intimidated(self, strength):
        intimidate_amt = _cap(self.intimidation, strength, self.max_stats.intimidation, 0)
        self._intimidation[0] = intimidate_amt
        return intimidate_amt

    def is_dead(self):
        return self.health <= 0


class AIController():
    def __init__(self, entity):
        random.seed()
        self.state = State.DEFENSIVE
        self.entity = entity
        self.entity.controller = self
        self.state_edge = 7

    def state_check(self, opponent):
        health_diff = opponent.health - self.entity.health

        if health_diff <= -self.state_edge:
            return State.AGGRESSIVE
        if -self.state_edge < health_diff < self.state_edge:
            return State.BALANCED
        if health_diff >= self.state_edge:
            return State.DEFENSIVE

    def state_decide(self, opponent):

        if self.state == State.AGGRESSIVE:
            # keep rolling until we pick a valid option
            while True:
                roll = random.randint(1,100)

                # 60% chance attack
                if 0 < roll <= 60:
                    # entity attack moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.ATTACK]
                    return random.choice(list(moves))
                
                # 20% chance intimidate
                if 60 < roll <= 80:
                    # entity intimidate moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.INTIMIDATE]
                    choice = random.choice(list(moves))

                    # check if move does anything
                    intimidate_amt = _cap(opponent.intimidation, choice[1][1], opponent.max_stats.intimidation, 0)
                    # if valid, return choice
                    if intimidate_amt > 0:
                        return choice
                    else:
                    # if not, reroll
                        continue

                # 10% chance heal
                if 80 < roll <= 90:
                    # entity heal moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.HEAL]
                    choice = random.choice(list(moves))

                    #check if move does anything
                    heal_amt = _cap(self.entity.health, choice[1][1], self.entity.max_stats.health, 0)

                    # if valid, return choice
                    if heal_amt > 0:
                        return choice
                    # if not, reroll
                    else:
                        continue

                # 10% chance defend
                if 90 < roll <= 100:
                    # entity defend moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.DEFEND]
                    choice = random.choice(list(moves))

                    #check if move does anything
                    defense_amt = _cap(self.entity.defense, choice[1][1], self.entity.max_stats.defense, 0)

                    if defense_amt > 0:
                        return choice
                    else:
                        continue


        if self.state == State.DEFENSIVE:
            while True:
                roll = random.randint(1,100)

                # 40% chance attack
                if 0 < roll <= 40:
                    # entity attack moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.ATTACK]
                    return random.choice(list(moves))
                
                # 10% chance intimidate
                if 40 < roll <= 50:
                    # entity intimidate moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.INTIMIDATE]
                    choice = random.choice(list(moves))

                    # check if move does anything
                    intimidate_amt = _cap(opponent.intimidation, choice[1][1], opponent.max_stats.intimidation, 0)
                    # if valid, return choice
                    if intimidate_amt > 0:
                        return choice
                    else:
                    # if not, reroll
                        continue

                # 40% chance heal
                if 50 < roll <= 90:
                    # entity heal moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.HEAL]
                    choice = random.choice(list(moves))

                    #check if move does anything
                    heal_amt = _cap(self.entity.health, choice[1][1], self.entity.max_stats.health, 0)

                    # if valid, return choice
                    if heal_amt > 0:
                        return choice
                    # if not, reroll
                    else:
                        continue

                # 10% chance defend
                if 90 < roll <= 100:
                    # entity defend moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.DEFEND]
                    choice = random.choice(list(moves))

                    #check if move does anything
                    defense_amt = _cap(self.entity.defense, choice[1][1], self.entity.max_stats.defense, 0)

                    if defense_amt > 0:
                        return choice
                    else:
                        continue


        if self.state == State.BALANCED:
            while True:
                roll = random.randint(1,100)

                # 30% chance attack
                if 0 < roll <= 30:
                    # entity attack moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.ATTACK]
                    return random.choice(list(moves))
                
                # 20% chance intimidate
                if 30 < roll <= 50:
                    # entity intimidate moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.INTIMIDATE]
                    choice = random.choice(list(moves))

                    # check if move does anything
                    intimidate_amt = _cap(opponent.intimidation, choice[1][1], opponent.max_stats.intimidation, 0)
                    # if valid, return choice
                    if intimidate_amt > 0:
                        return choice
                    else:
                    # if not, reroll
                        continue

                # 30% chance heal
                if 50 < roll <= 80:
                    # entity heal moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.HEAL]
                    choice = random.choice(list(moves))

                    #check if move does anything
                    heal_amt = _cap(self.entity.health, choice[1][1], self.entity.max_stats.health, 0)

                    # if valid, return choice
                    if heal_amt > 0:
                        return choice
                    # if not, reroll
                    else:
                        continue

                # 20% chance defend
                if 80 < roll <= 100:
                    # entity defend moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.DEFEND]
                    choice = random.choice(list(moves))

                    #check if move does anything
                    defense_amt = _cap(self.entity.defense, choice[1][1], self.entity.max_stats.defense, 0)

                    if defense_amt > 0:
                        return choice
                    else:
                        continue

    def take_turn(self, opponent):
        # check action state transition
        self.state = self.state_check(opponent)

        # what move should the player take based on the current state
        return (opponent, *self.state_decide(opponent))

class PlayerController():
    def __init__(self, entity, controller_method):
        self.entity = entity
        self.entity.controller = self
        self.control = controller_method

    def take_turn(self, opponent):
        return (opponent, *self.control(self.entity))
    

class Player(Entity):
    def __init__(self, name="Player", max_stats=None):
        if max_stats is None:
            max_stats = Stats(*DEFAULT_MAX_STATS)
        super().__init__(name, max_stats)


class DumbController():
    def __init__(self, entity):
        self.entity = entity
        self.entity.controller = self

    def take_turn(self, opponent):
        return (opponent, *random.choice(list([(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.ATTACK])))


class SearchController():
    def __init__(self, entity, path_iter):
        self.entity = entity
        self.entity.controller = self
        self.path_iter = path_iter

    def take_turn(self, opponent):
        return (opponent, *next(self.path_iter, (None,None)))


class PathController():
    def __init__(self, entity, path_iter=[]):
        self.entity = entity
        self.entity.controller = self
        self.path_iter = iter(path_iter)

    def take_turn(self, opponent):
        next_move = next(self.path_iter, None)
        if next_move is None:
            self.path_iter = iter(search_optimum(self.entity, opponent))
            next_move = next(self.path_iter, None)
        return (opponent, *next_move)

def eval_path(path, searcher, opponent):
    s = copy.deepcopy(searcher)
    search_ai = SearchController(s, iter(path))

    o = copy.deepcopy(opponent)
    dumb_ai = DumbController(o)

    entities = [s,o]

    for node in path:
        # simulate round
        for entity in entities:
            # shift entity buffs each round
            entity._defense = [0] + entity._defense[0:-1]
            entity._intimidation = [0] + entity._intimidation[0:-1]

            # use all other entities as possible targets
            target, name, move = entity.controller.take_turn(*[e for e in entities if e is not entity])
            action_type, power = move

            # entity does these to target
            if action_type == MoveType.ATTACK: 
                result = do_action(entity, target, move)
            if action_type == MoveType.INTIMIDATE: 
                result = do_action(entity, target, move)

            # entity does these to self
            if action_type == MoveType.HEAL: 
                result = do_action(entity, entity, move)
            if action_type == MoveType.DEFEND: 
                result = do_action(entity, entity, move)

    # evaluate result
    # if we killed the player, DO THAT
    if o.health <= 0:
        return 10000
    # else, return mathematical fitness
    else:
        # check final health results
        health_fitness = s.health - o.health

        # check change in health through game
        o_health_diff = opponent.health - o.health
        s_health_diff = s.health - searcher.health

        # combine values with weights
        return health_fitness + (0.5 * o_health_diff) + (0.5 * s_health_diff)


def search_optimum(searcher, opponent, depth=4):
    # permute all possible paths
    paths = [p for p in itertools.product(searcher.moveset.items(), repeat=4)]

    # search all permutations
    path_fitness = [(eval_path(p,searcher, opponent),p) for p in paths]

    # return best path
    return max(path_fitness,key=itemgetter(0))[1]


def begin_game(*entities):
    # while challengers are alive
    while not [entity for entity in entities if entity.is_dead()]:
        for entity in entities:
            # shift entity buffs each round
            entity._defense = [0] + entity._defense[0:-1]
            entity._intimidation = [0] + entity._intimidation[0:-1]

            # use all other entities as possible targets
            target, name, move = entity.controller.take_turn(*[e for e in entities if e is not entity])
            action_type, power = move

            # entity does these to target
            if action_type == MoveType.ATTACK: 
                result = do_action(entity, target, move)
            if action_type == MoveType.INTIMIDATE: 
                result = do_action(entity, target, move)

            # entity does these to self
            if action_type == MoveType.HEAL: 
                result = do_action(entity, entity, move)
            if action_type == MoveType.DEFEND: 
                result = do_action(entity, entity, move)

            print(entity.name,"preformed",name,"for",result)

        print()
        print(*entities, sep="\n")
        
    print(*[f"{entity.name} has died" for entity in entities if entity.is_dead()], sep=", and ")


def do_action(actor, recipient, action):
        action_type, power = action
        if action_type == MoveType.ATTACK: return recipient.be_hit(power - actor.intimidation)
        if action_type == MoveType.HEAL: return recipient.be_healed(power)
        if action_type == MoveType.DEFEND: return recipient.be_defended(power)
        if action_type == MoveType.INTIMIDATE: return recipient.be_intimidated(power)
    

def _cap(base, num, max_cap, min_cap):
    if num < 0:
        return num if num >= min_cap - base else min_cap - base
    elif num > 0:
        return num if num <= max_cap - base else max_cap - base
    else:
        return num
     
