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

import pathlib
from os import path

from GraphDB import GraphDB


def main():
    direct = pathlib.Path(__file__).parent.absolute()
    p = path.join(direct, 'test_database')
    db = GraphDB(p)
    relation = db.CreateNode('relations.relation')
    isa = db.CreateNode('relations.isa')
    aka = db.CreateNode('relations.aka')

    atom = db.CreateNode('types.atom')
    symbol = db.CreateNode('types.symbol', atom)

    db.CreateLink(isa, isa, relation)
    db.CreateLink(aka, isa, relation)
    db.CreateLink(symbol, isa, atom)

    db.SaveAllChanges()

    category = db.CreateNode('category')

    _obj_ = db.CreateNode('category.object')
    _sub_ = db.CreateNode('category.subject')
    _bei_ = db.CreateNode('category.being')
    _cre_ = db.CreateNode('category.creature')
    _animal_ = db.CreateNode('category.animal')
    _mammal_ = db.CreateNode('category.mammal')
    _human_ = db.CreateNode('category.human')

    db.CreateLink(_human_, isa, _mammal_)
    db.CreateLink(_mammal_, isa, _animal_)
    db.CreateLink(_animal_, isa, _cre_)
    db.CreateLink(_cre_, isa, _bei_)
    db.CreateLink(_bei_, isa, _sub_)
    db.CreateLink(_sub_, isa, _obj_)

    db.CreateLink(_human_, aka, category)
    db.CreateLink(_mammal_, isa, category)
    db.CreateLink(_animal_, isa, category)
    db.CreateLink(_cre_, isa, category)
    db.CreateLink(_bei_, isa, category)
    db.CreateLink(_sub_, isa, category)

    db.SaveAllChanges()


if __name__ == '__main__':
    main()
