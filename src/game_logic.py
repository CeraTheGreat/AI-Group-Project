# AI group project
# Jenny Rotelli & Matthew McKnight
# 
# Game logic - entity interactions and AI implimentation

import enum


# (max_health, max_intimidation, max_defense)
DEFAULT_MAX_STATS = (100, 4, 4)

class MoveType(enum.Enum):
    ATTACK = 0
    HEAL = 1
    DEFEND = 2
    INTIMIDATE = 3

MOVES = {
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


class Brain:
    def __init__(self, entity):
        self.entity= entity

    def take_turn(opponents):
        # AI should go here
        pass


# A player has no "Brain" in the code since it is controlled by a user
class Player(Entity):
    def __init__(self, name="Player", max_stats=None):
        if max_stats is None:
            max_stats = Stats(*DEFAULT_MAX_STATS)
        super().__init__(name, max_stats)


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
     
