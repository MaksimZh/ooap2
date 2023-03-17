from abc import ABC, abstractmethod

class Player:

    def heal(self, hit_points: int) -> None:
        ...

    def hurt(self, hit_points: int) -> None:
        ...


# Абстрактная ячейка на карте
# Можно проверить может ли игрок наступить на неё
# Может взаимодействовать с игроком произвольным образом
class Cell(ABC):

    @abstractmethod
    def can_pass(self) -> bool:
        assert False
    
    @abstractmethod
    def interact(self, player: Player) -> None:
        assert False


# Через стену нельзя пройти
class Wall(Cell):

    def can_pass(self) -> bool:
        return False
    
    def interact(self, player: Player) -> None:
        pass


# Можно наступить на ловушку
# Ловушка наносит урон
class Trap(Cell):

    def can_pass(self) -> bool:
        return True
    
    def interact(self, player: Player) -> None:
        player.hurt(10)


# Можно наступить на святое место
# Святое место лечит игрока
class HolyPlace(Cell):

    def can_pass(self) -> bool:
        return True
    
    def interact(self, player: Player) -> None:
        player.heal(10)

...

# Полиморфный вызов
def new_logic(player: Player, cell: Cell):
    if not cell.can_pass():
        return
    move_player(...)
    cell.interact(player)


# Что было бы с аттрибутами
def old_logic(player: Player, cell: Cell):
    if cell.get_type() == WALL:
        return
    move_player(...)
    if cell.get_type() == TRAP:
        player.hurt(10)
        return
    if cell.get_type() == HOLY:
        player.heal(10)
        return
    ...
