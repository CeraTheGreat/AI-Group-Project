# AI group project
# Jenny Rotelli & Matthew McKnight
# 
# Game logic - entity interactions and AI implimentation

import enum
import random


# (max_health, max_intimidation, max_defense)
DEFAULT_MAX_STATS = (100, 4, 4)

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
        "slash":(MoveType.ATTACK, 12),
        "potion":(MoveType.HEAL, 3),
        "sheild":(MoveType.DEFEND, 1),
        "scare":(MoveType.INTIMIDATE, 1) }


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
        self.intimidation = 0
        self.defense = 0

        self.moveset = MOVES

        # we start without a controller, add one later
        self.controller = None

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
        damage = strength - self.defense
        self.health = self.health - damage
        return damage

    def be_healed(self, strength):
        heal_amt = _cap(self.health, strength, self.max_stats.health, 0)
        self.health = self.health + heal_amt
        return heal_amt

    def be_defended(self, strength):
        defense_amt = _cap(self.defense, strength, self.max_stats.defense, 0)
        self.defense = self.defense + defense_amt
        return defense_amt

    def be_intimidated(self, strength):
        intimidate_amt = _cap(self.intimidation, strength, self.max_stats.intimidation, 0)
        self.intimidation = self.intimidation + intimidate_amt
        return intimidate_amt

    def is_dead(self):
        return self.health <= 0


class AIController():
    def __init__(self, entity):
        random.seed()
        self.state = State.DEFENSIVE
        self.entity = entity
        self.entity.controller = self

    def state_check(self, context):
        if self.state == State.AGGRESSIVE:
            # check context for state switches
            # return ongoing state
            return State.AGGRESSIVE

        if self.state == State.DEFENSIVE:
            # check context for state switches
            # return ongoing state
            return State.DEFENSIVE

        if self.state == State.BALANCED:
            # check context for state switches
            # return ongoing state
            return State.BALANCED

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

                # 20% chance attack
                if 0 < roll <= 20:
                    # entity attack moves
                    moves = [(x,y) for x,y in self.entity.moveset.items() if y[0] == MoveType.ATTACK]
                    return random.choice(list(moves))
                
                # 10% chance intimidate
                if 20 < roll <= 30:
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

                # 35% chance heal
                if 30 < roll <= 65:
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

                # 35% chance defend
                if 65 < roll <= 100:
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
        self.state == self.state_check(opponent)

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


def begin_game(*entities):
    # while challengers are alive
    while not [entity for entity in entities if entity.is_dead()]:
        for entity in entities:
            # use all other entities as possible targets
            target, name, move = entity.controller.take_turn(*[e for e in entities if e is not entity])
            action_type, power = move

            # entity does these to target
            if action_type == MoveType.ATTACK: 
                result = do_action(entity, target, move)
            if action_type == MoveType.INTIMIDATE: 
                result = do_action(entity, target, move)

            # Player does these to self
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
     
