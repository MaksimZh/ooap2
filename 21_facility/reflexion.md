# Специфика наследования реализаций

Добавилось ещё два типа наследования.
Они отличаются от предыдущих тем, что они ближе к уровню реализации,
чем остальные, которые относятся больше к уровню логики.
Даже название - "наследование реализаций" - указывает на это.

В первом примере вся реализация дерева выделяется в отдельную абстракцию.
Эта сущность, вероятно, будет общей для разных древовидных структур,
включая диаграмму классов.

В предметной области абстрактного дерева, скорее всего, нет.
Это особенность реализации.

В третьем примере два вида существ в предметной области не связаны отношением
"является".
Наследование здесь - снова детали реализации.

Аналогичное решение мы видим для http-ответов и для концовок игры.
И то и другое скорее значения, чем типы.
Просто их удобно представить в виде классов-потомков.

В моём решении это относится и к токенам.
Их удобно сделать отдельными классами, чем складывать всё в один тип.

Аналогично, иерархия лексических нализаторов - это способ избежать большого
количества условных операторов.