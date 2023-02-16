# Наследование, композиция, полиморфизм - 2

## Расширение и специализация класса-родителя
В примере на Python один и тот же класс потомок и расширяет и специализирует
класс-родитель.

В примере на Java всё ещё интереснее, в двух разных иерархиях классов происходит
ровно одно и то же: потомок добавляет новые методы.
При этом используется одно и тоже объяснение:
"все `потомки` - `родители`, но не все `родители` - `потомки`",
а выводы делаются разные: в первом случае - специализация, во втором - расширение.

Эти два примера наводят на мысль, что формализовать отличия
расширения от специализации очень сложно не только на уровне кода,
но и на уровне логики.
Я всё же попытался эти различия внести.

Я хотел, чтобы класс `MagicWeapon` можно было
при желании использовать вместо `Weapon`, просто не добавляя заклинание.
Наоборот же не получится: в сценариях где нужно именно магическое оружие
обычное не подойдёт.

Получилось не очень удачно, поскольку оба класса абстрактные и потомки
должны реализовать разные методы.
Лучше было бы для расчёта физического урона использовать композицию,
тогда оба класса не были бы абстрактными,
могли бы использоваться непосредственно, и решение было бы более наглядным:
```Python
...

class PhysicalDamageCalculator(ABC):
    @abstractmethod
    def calc(self, strength: int, agility: int) -> int:
        assert False


class Weapon:

    __weight: int
    __damage_calculator: PhysicalDamageCalculator

    def __init__(self, weight: int, damage_calculator: PhysicalDamageCalculator) -> None:
        self.__weight = weight
        self.__damage_calculator = damage_calculator

    ...

    def calc_damage(self, strength: int, agility: int) -> int:
        return self.__damage_calculator.calc(strength, agility)


class MagicWeapon(Weapon):
    ...    
    
    def calc_damage(self, strength: int, agility: int) -> int:
        physical_damage = super().calc_damage(strength, agility)
        spell_damage = self.__spell.get_damage()
        return physical_damage + spell_damage

...
```
Теперь точно `MagicWeapon` можно использовать вместо `Weapon`.

Что касается специализации, то класс `Hammer` (в решении опечатка: `Hummer` :)
реализует расчёт урона определённым образом.
В новом решении он выглядел бы так:
```Python
...

class HammerDamageCalculator(PhysicalDamageCalculator):
    
    __weight: int
    
    def __init__(self, weight: int) -> None:
        self.__weight = weight
    
    def calc(self, strength: int, agility: int) -> int:
        return self.__weight + strength


class Hammer(Weapon):

    def __init__(self, weight: int) -> None:
        super().__init__(weight, HammerDamageCalculator(weight))
```
С весом не очень хорошо получилось -
поле дублируется у оружия и в расчёте урона - есть над чем работать :)

Главное отличие: если нам нужен меч, то вместо `Weapon`
можно использовать `MagicWeapon` (расширение),
но нельзя использовать `Hammer` (специализацию).
