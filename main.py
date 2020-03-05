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
import os
import pathlib
from os import path

from Node import Node


def LoadJson(file):
    with open(file, encoding='utf8') as f:
        return json.load(f)


def SaveJson(file, value):
    _path = pathlib.Path(file).parent
    _path.mkdir(parents=True, exist_ok=True)
    with open(file, 'w', encoding='utf8') as f:
        json.dump(value, f, indent=2)


class GraphDB:
    def __init__(self, root_directory):
        os.makedirs(root_directory, exist_ok=True)
        self.__root = root_directory
        self.__index = {}
        self.__dirty = []

    def __NodeToPath(self, node):
        return path.join(self.__root, *node.split('.')) + '.json'

    def GetNode(self, node_id):
        if node_id not in self.__index:
            _path = self.__NodeToPath(node_id)
            if path.isfile(_path):
                js = LoadJson(_path)
                self.__index[node_id] = Node(self, js)
            else:
                return None
        return self.__index[node_id]

    def CreateNode(self, node_id):
        _path = self.__NodeToPath(node_id)
        if path.isfile(_path):
            # Узел есть - откроем его
            return self.GetNode(node_id)
        # Узла нет - создадим
        self.__index[node_id] = Node.Create(self, node_id)
        self.__index[node_id].SetDirty()
        return self.__index[node_id]

    def SaveNode(self, node):
        _path = self.__NodeToPath(node.Id)
        SaveJson(_path, node.Content)

    def SetDirty(self, node):
        self.__dirty.append(node)

    def SaveAllChanges(self):
        for node in self.__dirty:
            self.SaveNode(node)
        self.__dirty.clear()


def main():
    direct = pathlib.Path(__file__).parent.absolute()
    p = path.join(direct, 'test_database')
    db = GraphDB(p)
    atom = db.CreateNode('atom')
    symbol = db.CreateNode('symbol')
    symbol.Type = atom
    db.SaveAllChanges()


if __name__ == '__main__':
    main()
