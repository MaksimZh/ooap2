from abc import ABC, abstractmethod

# NOTE:
# Здесь циклическая зависимость SpaceShip и StarSystem.
# Сделал так для краткости.


class StarSystem(ABC):
    def get_linked_systems(self) -> "set[StarSystem]":
        ...

    @abstractmethod
    def accept_ship(self, ship: "Spaceship") -> None:
        assert False


def find_path(start: StarSystem, finish: StarSystem) -> list[StarSystem]:
    ...


class Spaceship:
    
    __position: StarSystem

    def travel(self, target: StarSystem) -> None:
        path = find_path(self.__position, target)
        # летим через естественные червоточины
        # в текущей (нулевой) системе уже были, поэтому начинаем с первой
        for system in path[1:]:
            system.accept_ship(self)

    def destroy(self) -> None:
        print("BOOM!!!")


# Наследование вариаций
# переопределяется работа метода `travel`
class HyperspaceShip(Spaceship):

    def travel(self, target: StarSystem) -> None:
        # у нас гиперпространственный корабль
        # открываем свою червоточину и летим сразу к цели
        target.accept_ship(self)

# Наследование с конкретизацией
# реализуется абстрактный метод `accept_ship`
class RegularStarSystem(StarSystem):
    def accept_ship(self, ship: "Spaceship") -> None:
        # ничего необычного не происходит
        pass

# Наследование с конкретизацией
# реализуется абстрактный метод `accept_ship`
class BlackHoleSystem(StarSystem):
    def accept_ship(self, ship: "Spaceship") -> None:
        # не повезло :(
        ship.destroy()


class Weapon:
    ...

class WeaponCarrier:
    def get_weapon(self) -> Weapon:
        ...

# Структурное наследование `WeaponCarrier`
class Battleship(HyperspaceShip, WeaponCarrier):
    ...

# Структурное наследование `WeaponCarrier` принципиально другим классом
class AsteroidTurret(WeaponCarrier):
    ...
