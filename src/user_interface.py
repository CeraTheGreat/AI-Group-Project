import random
import game_logic

monster = game_logic.Entity("Monster")
player = game_logic.Player("Player")

while not monster.is_dead() and not player.is_dead():
    # Player turn
    name,move = random.choice(list(player.moveset.items()))
    action_type, power = move

    # Player does these to monster
    if action_type == game_logic.MoveType.ATTACK: 
        result = game_logic.do_action(player, monster, move)
    if action_type == game_logic.MoveType.INTIMIDATE: 
        result = game_logic.do_action(player, monster, move)

    # Player does these to self
    if action_type == game_logic.MoveType.HEAL: 
        result = game_logic.do_action(player, player, move)
    if action_type == game_logic.MoveType.DEFEND: 
        result = game_logic.do_action(player, player, move)

    # Print outcome of action
    print(player.name,"preformed",name,"for",result)

    #monster turn
    name,move = random.choice(list(monster.moveset.items()))
    action_type, power = move

    # Player does these to monster
    if action_type == game_logic.MoveType.ATTACK: 
        result = game_logic.do_action(monster, player, move)
    if action_type == game_logic.MoveType.INTIMIDATE: 
        result = game_logic.do_action(monster, player, move)

    # Player does these to self
    if action_type == game_logic.MoveType.HEAL: 
        result = game_logic.do_action(monster, monster, move)
    if action_type == game_logic.MoveType.DEFEND: 
        result = game_logic.do_action(monster, monster, move)

    # Print outcome of action
    print(monster.name,"preformed",name,"for",result)

    print(player)
    print(monster)

    input("press 'enter'")

print(monster.name,"has died") if monster.is_dead() else print(player.name,"has died")

