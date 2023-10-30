from game import MiffyGame
from player import MiffyPlayer
from enums import Icon
import pandas as pd


def main():
    miffy = MiffyPlayer(Icon.miffy)
    dog = MiffyPlayer(Icon.snuffy)

    game = MiffyGame([miffy, dog])
    print(game.board_status)

    winners = []
    for _ in range(1000):
        winners.append(game.simulate().icon.name)

    # print(winners)
    df = pd.DataFrame(winners, columns=["winners"])
    print(df.winners.value_counts())
    pass


if __name__ == "__main__":
    main()
