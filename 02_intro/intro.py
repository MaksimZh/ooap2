from abc import ABC, abstractmethod


# Базовый класс оружия
class Weapon(ABC):

    # Частичная реализация, общая для всех видов оружия: учёт веса оружия

    __weight: int

    def __init__(self, weight: int) -> None:
        self.__weight = weight

    def get_weight(self) -> int:
        return self.__weight

    # Расчёт урона зависит от вида оружия и должен быть реализован потомками
    @abstractmethod
    def calc_damage(self, strength: int, agility: int) -> int:
        assert False


# Заклинание
class Spell(ABC):
    
    @abstractmethod
    def get_damage(self) -> int:
        assert False

# Пустое заклинание
class NoSpell(Spell):

    def get_damage(self) -> int:
        return 0


# Наследование с расширением класса-родителя
# Магическое оружие - более общий случай,
# так как обычное оружие - это магическое с пустым заклинанием
class MagicWeapon(Weapon):

    __spell: Spell

    def __init__(self, weight: int) -> None:
        super().__init__(weight)
        self.__spell = NoSpell()

    def set_spell(self, spell: Spell) -> None:
        self.__spell = spell
    
    def calc_damage(self, strength: int, agility: int) -> int:
        physical_damage = self.calc_physical_damage(strength, agility)
        spell_damage = self.__spell.get_damage()
        return physical_damage + spell_damage

    @abstractmethod
    def calc_physical_damage(self, strength: int, agility: int) -> int:
        assert False


# Наследование со специализацией класса-родителя
# Молот - частный случай оружия с особой реализацией расчёта урона
class Hummer(Weapon):

    def calc_damage(self, strength: int, agility: int) -> int:
        return self.get_weight() + strength
