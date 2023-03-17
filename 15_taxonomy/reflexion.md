# Решение конфликта таксономии

Примеры решений достаточно простые и там всё логично.

У меня же в коде есть недостаток, существенный в контексте данного задания.
Это проверка можно ли пройти через ячейку (запрос `can_pass`),
и соответствующий условный оператор.
Лучше и от неё избавиться, особенно если нужно будет
расширять логику перемещения игрока.

Тут важно как реализована сущность, отвечающая за движение,
а в моём решении она не показана.
В любом случае, не хотелось бы переносить логику движения непосредственно в ячейки.
Мне это кажется контринтуитивным, затрудняющим понимание кода.

Теперь уже пришла идея получше: добавить абстракций логики перемещения
и логики взаимодействия.

## Логика перемещения
```Python
class MotionTarget:
    def move(self, old_position: MotionTarget) -> MotionTarget:
        return self

class Obstacle(MotionTarget):
    def move(self, old_position: MotionTarget) -> MotionTarget:
        return old_position
```

## Логика взаимодействия
```Python
class Area:
    def interact(self, player: Player) -> None:
        pass

class HurtingArea(Area):
    def interact(self, player: Player) -> None:
        player.hurt(...)

class HealingArea(Area):
    def interact(self, player: Player) -> None:
        player.heal(...)
```

## Ячейки
Они собираются как конструктор благодаря множественному наследованию.
```Python
class Empty(MotionTarget, Area):
    pass

class Wall(Obstacle, Area):
    pass

class Trap(MotionTarget, HurtingArea):
    pass

class HolyPlace(MotionTarget, HealingArea):
    pass
```
