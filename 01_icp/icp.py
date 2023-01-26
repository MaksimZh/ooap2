from abc import ABC, abstractmethod

# Базовый класс оружия
class Weapon(ABC):

    # Частичная реализация, общая для всех видов оружия:
    # учёт веса оружия

    __weight: int

    def __init__(self, weight: int) -> None:
        self.__weight = weight

    def get_weight(self) -> int:
        return self.__weight

    # Расчёт урона зависит от вида оружия и должен быть реализован потомками
    @abstractmethod
    def calc_damage(self, strength: int, agility: int) -> int:
        pass


# Игровой персонаж
class Character:

    __strength: int
    __agility: int
    
    # КОМПОЗИЦИЯ: character has a weapon
    __weapon: Weapon

    def __init__(self, strength: int, agility: int) -> None:
        self.__strength = strength
        self.__agility = agility
        self.__weapon = Hands()

    def set_weapon(self, weapon: Weapon) -> None:
        self.__weapon = weapon
    
    def get_damage(self) -> int:
        # ПОЛИМОРФИЗМ: 
        return self.__weapon.calc_damage(self.__strength, self.__agility)


# НАСЛЕДОВАНИЕ: hands is a weapon
class Hands(Weapon):

    def __init__(self) -> None:
        super().__init__(0)

    def calc_damage(self, strength: int, agility: int) -> int:
        return 2 * strength + agility


# НАСЛЕДОВАНИЕ: sword is a weapon
class Sword(Weapon):

    def __init__(self) -> None:
        super().__init__(50)

    def calc_damage(self, strength: int, agility: int) -> int:
        return 20 * strength + agility


# НАСЛЕДОВАНИЕ: bow is a weapon
class Bow(Weapon):

    def __init__(self) -> None:
        super().__init__(10)

    def calc_damage(self, strength: int, agility: int) -> int:
        return strength + 15 * agility


swordsman = Character(strength=20, agility=10)
marksman = Character(strength=5, agility=20)
sword = Sword()
bow = Bow()

print(swordsman.get_damage(), marksman.get_damage()) # 50 30
swordsman.set_weapon(bow)
marksman.set_weapon(sword)
print(swordsman.get_damage(), marksman.get_damage()) # 170 120
swordsman.set_weapon(sword)
marksman.set_weapon(bow)
print(swordsman.get_damage(), marksman.get_damage()) # 410 305
