# Наследование подтипов, с ограничением и с расширением

## Работа над ошибками
Ну как можно было забыть сделать задание для подтипов!?

Сделаю сейчас не подглядывая в ответ.

### Стена, пустая клетка, ловушка - подтипы клетки лабиринта
Каждый тип клетки независим.
Хотя у них общий интерфейс, связанный с логикой движения в лабиринте,
реализации разные.

### "Решатель" дифуров, "диагонализатор" матриц - подтипы абстрактной процедуры
У всех процедур есть абстрактный интерфейс:
запись аргументов, выполнение и чтение результата.
При этом набор аргументов и алгоритм выполнения разные.


## Рефлексия
Сложнее всего мне далось понимание различий между наследованием подтипов
и наследованием с ограничением.
Как я понял, нужно смотреть на интерфейсы АТД и сценарии использования.

### Наследование подтипов
Интерфейс не меняется.

Доступные сценарии использования остаются теми же, что и у родительского класса.
Поведение в этих сценариях может существенно отличаться.

### Наследование с ограничениями
Интерфейс АТД может расширяться.

Множество сценариев использования родительского АТД делится между АТД-потомками.

LSP не нарушается, т.к. подмножество допустимых сценариев использования
родительского АТД доступно всем потомкам.
Просто при разделе сфер ответственности это общее подмножество сужается.

## Наследование с расширением
Интерфейс АТД расширяется.

Добавляются новые сценарии использования, недоступные родительскому АТД.