import random
import game_logic as logic
import sys


def user_choice(entity):
    while True:
        for i, move_tuple in enumerate(entity.moveset.items()):
            name, move = move_tuple 
            print(f"{i}: {name:8} | typ:{move[0]:20} - str:{move[1]:3}")

        selection = input("select move: ")
        print()
        try:
            selection = int(selection)
        except ValueError:
            print("Not an int")
            continue
        
        if 0 <= selection < len(entity.moveset):
            return list(entity.moveset.items())[selection]
        else:
            continue


if __name__ == "__main__":
    state = False
    search = False

    if len(sys.argv) == 1:
        state = True
    elif len(sys.argv) > 1:
        if sys.argv[1] == '--state':
            state = True
        elif sys.argv[1] == '--search':
            search = True
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("python user_interface.py [--state | --search | -h/--help]")
            sys.exit(0)

    monster = logic.Entity("Monster")
    if state:
        print("using state control...")
        print()
        monster_ai = logic.AIController(monster)
    elif search:
        print("using search control...")
        print()
        monster_ai = logic.PathController(monster)

    player = logic.Player("Player")
    player_controller = logic.PlayerController(player, user_choice)

    logic.begin_game(player, monster)
