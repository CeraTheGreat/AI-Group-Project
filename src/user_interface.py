import random
import game_logic as logic

monster = logic.Entity("Monster")
monster_ai = logic.Brain(monster)

player = logic.Player("Player")

while not monster.is_dead() and not player.is_dead():
    # Player turn
    name,move = random.choice(list(player.moveset.items()))
    action_type, power = move

    # Player does these to monster
    if action_type == logic.MoveType.ATTACK: 
        result = logic.do_action(player, monster, move)
    if action_type == logic.MoveType.INTIMIDATE: 
        result = logic.do_action(player, monster, move)

    # Player does these to self
    if action_type == logic.MoveType.HEAL: 
        result = logic.do_action(player, player, move)
    if action_type == logic.MoveType.DEFEND: 
        result = logic.do_action(player, player, move)

    # Print outcome of action
    print(player.name,"preformed",name,"for",result)

    # Monster turn
    name,move = monster_ai.take_turn(player)
    action_type, power = move

    # Player does these to monster
    if action_type == logic.MoveType.ATTACK: 
        result = logic.do_action(monster, player, move)
    if action_type == logic.MoveType.INTIMIDATE: 
        result = logic.do_action(monster, player, move)

    # Player does these to self
    if action_type == logic.MoveType.HEAL: 
        result = logic.do_action(monster, monster, move)
    if action_type == logic.MoveType.DEFEND: 
        result = logic.do_action(monster, monster, move)

    # Print outcome of action
    print(monster.name,"preformed",name,"for",result)

    print(player)
    print(monster)

    input("press 'enter'")

print(monster.name,"has died") if monster.is_dead() else print(player.name,"has died")

