# Замыкание иерархии

Примера на Python нет, потому что проверка типов в этом языке слабая
(хоть и лучше, чем, например, в JavaScript).
Но при использовании линтера можно отловить много ошибок
ещё на этапе написания кода.

В своём решении я так и поступил: где-то аннотации типов для линтера,
а где-то `assert` для уверенности, что откровенные ошибки будут пойманы
во время выполнения.