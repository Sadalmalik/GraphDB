# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
Итак.
Я хочу замутить себе простенькую графовую базу данных.

Два основных типа сущностей:
  Ноды - они же узлы или вершины графа
  Связи - они же рёбра

Сначала я думал писать типа файл ноды и связи ноды в самом файле.
Типа:

{
    "id": Индекс_Узла,
    "data": { /* уникальные данные */ },
    "relations":
        [
            {
                "id": Индекс_Связи,
                "type": Индекс_Узла,
                "from": Индекс_Узла,
                "into": Индекс_Узла
            },
            {...},
            {...},
            {...}
        ]
}

Но связи неудобно хранить так, потому как связь привязана к двум нодам, а не к одному.
Значит в виде отдельных файликов.

И тут я вспоминаю свою идею что бы связь была таким же нодом.
Это пожалуй крутая тема, но тогда разу может возникнуть мысль что у нодов должны быть типы...
Хотя можно и без них.

Если сделать максимально прозрачную систему адресации...
Впринципе мне сейчас не нужна скорость.

Так что сделаю так:
идентификатор узла это имя вида
папка.подпапка.имя
и расположенны файлы сохранений соответственно по пути
папка/подпапка/имя.node

Каждый узел является и узлом и связью (как я и придумывал)
И имеет вид:

{
    "id": "полное имя/путь",
    "name": "собственное имя",
    "data": { }, # если понадобиться

    "type": "id узла",
    "from": "id узла",
    "into": "id узла",

    "relations": # Список узлов, ссылающихся на данный узер в одном из трёх вышеназначенных полей
    [
        "id узла",
        "id узла",
        "id узла",
        ...
    ]
}

Информация вроде как _избыточна_ но её как раз хватит что бы попасть куда угодно по графу.

Надеюсь норм.
Ну и на питоне прототипировать в целом легко.



Значит какие базовые операции?
Создание объекта узла
Получение объекта узла
Удаление узла (сложна!)
  можно удалять...
  можно помечать на удаление...

А дальше из узла можно получать все его связи



Заюзать проперти
https://www.python-course.eu/python3_properties.php



"""

import json
from os import path


class Node:
    def __init__(self, id, data=None, _type=None, _from=None, _into=None, _relations=None):
        self.__content = {
            'id': id,
            'name': id.split('.')[-1],
            'type': _type,
            'from': _from,
            'into': _into,
            'relations': _relations,
        }
        self.__changed = False


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return obj.__content
        return json.JSONEncoder.default(self, obj)


class GraphDB:
    def __init__(self, root_directory):
        self.__root = root_directory
        self.__index = {}

    def __NodeToPath(self, node):
        return path.join(self.__root, *node.split('.'))

    def CreateNode(self, node):
        _path = self.__NodeToPath(node)
        if path.isfile(_path):
            # Узел есть - откроем его
            pass
        else:
            # Узла нет - создадим
            pass


def main():
    n = Node('test.Node0')
    print(n)
    print(json.dumps(n, cls=NodeEncoder))


if __name__ == '__main__':
    main()
