from player import MiffyPlayer
from enums import Icon
from dataclasses import dataclass
import random
import itertools


@dataclass
class BoardStep():
    icon: Icon | None
    special: str | None = None
    active_player: MiffyPlayer | None = None

    def put_player(self, player: MiffyPlayer) -> MiffyPlayer | None:
        """put a player on the spot. If a player is already present return that player"""
        prev_player = self.active_player
        self.active_player = player
        return prev_player

    def clear_step(self):
        if not self.special:
            self.active_player = None

    @property
    def has_player(self):
        if self.active_player:
            return True
        return False

    @property
    def name(self):
        if self.special:
            return self.special
        return self.icon.name

    def __str__(self):
        if self.has_player:
            return f"Step({self.name}, player={self.active_player})"
        else:
            return f"Step({self.name})"


def generate_next_player(players: list[MiffyPlayer]):
    """generate next player"""
    for element in itertools.cycle(players):
        yield element


class MiffyGame():
    def __init__(self, players: list[MiffyPlayer]):
        self.players = players
        self.reset()
        assert len(players) == 2, "game logic is only for 2 player for now"

    def reset(self):
        self.game_board = [BoardStep(icon=None, special="start"),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.miffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.melanie),
                           BoardStep(Icon.snuffy),
                           BoardStep(Icon.poppy),
                           BoardStep(Icon.miffy),
                           BoardStep(icon=None, special="end")]
        self.board_status = [0 for _ in range(len(self.players))]
        self.gen_player = generate_next_player(self.players)
        self.active_player = next(self.gen_player)

    def get_player_id(self, player: Icon) -> int:
        for idx, _player in enumerate(self.players):
            if player == _player:
                return idx

    def next_player(self):
        return next(self.gen_player)

    def game_won_by(self) -> MiffyPlayer | None:
        for idx, player in enumerate(self.players):
            if self.board_status[idx] >= len(self.game_board) - 1:
                return player
        return None

    def current_status(self):
        status = "\n"
        for boardstep in self.game_board:
            status += f" {boardstep}\n"
        return status

    def find_prev_step_id(self, player: MiffyPlayer) -> int:
        player_id = self.get_player_id(player)
        current_step_id = self.board_status[player_id]
        # current_boardstep = self.game_board[current_step_id]
        # current_boardstep.clear_step()

        for step_id in range(current_step_id-1, 0, -1):
            if self.game_board[step_id].icon == player.icon:
                return step_id
        return 0

    def step(self, player: MiffyPlayer, action: int):
        player_id = self.get_player_id(player)

        # reset current boardstep (clear player) from the boardstep)
        current_boardstep = self.game_board[self.board_status[player_id]]
        current_boardstep.clear_step()

        # find new boardstep
        self.board_status[player_id] += action
        if self.board_status[player_id] >= len(self.game_board) - 1:
            self.board_status[player_id] = len(self.game_board) - 1

        new_boardstep = self.game_board[self.board_status[player_id]]

        # put player on new boardstep
        if other_player := new_boardstep.put_player(player):
            # TODO make this piece recursive, but dont trigger 'goes again'!
            # player steps on other player -> other goes back to his own Icon step
            other_player_id = self.get_player_id(other_player)

            # reset current step of other player
            other_player_current_boarstep = self.game_board[self.board_status[other_player_id]]
            other_player_current_boarstep.clear_step()

            # set back other player
            backstep_id = self.find_prev_step_id(other_player)
            other_player_new_boardstep = self.game_board[backstep_id]
            other_player_new_boardstep.put_player(other_player)
            self.board_status[other_player_id] = backstep_id
            print(f"##### player: {other_player} goes back")

        # check if player lands on his own Icon -> goes again
        if new_boardstep.icon == player.icon:
            self.active_player = self.next_player()  # TODO only works with 2 players, when 3 or more, this wont work

    def simulate(self):
        MAX = 100
        turn = 0
        while turn <= MAX:
            turn += 1
            action = random.randint(1, 6)  # TODO try a new seed
            print(f"new turn for: {self.active_player}, {action} steps further")
            self.step(self.active_player, action)
            print(self.current_status())
            if winner := self.game_won_by():
                print(f"player: {winner} WON in {turn} tries")
                break
            self.active_player = self.next_player()
        self.reset()
        return winner
