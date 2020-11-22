import random
import game_logic as logic


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
    monster = logic.Entity("Monster")
    monster_ai = logic.AIController(monster)

    player = logic.Player("Player")
    player_controller = logic.PlayerController(player, user_choice)

    logic.begin_game(player, monster)
