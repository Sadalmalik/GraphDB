# !/usr/bin/python
# -*- coding: utf-8 -*-

import json
import pathlib


def LoadJson(file):
    with open(file, encoding='utf8') as f:
        return json.load(f)


def SaveJson(file, value):
    _path = pathlib.Path(file).parent
    _path.mkdir(parents=True, exist_ok=True)
    with open(file, 'w', encoding='utf8') as f:
        json.dump(value, f, indent=2)


def GetCrossPath(a, b):
    a = a.split('.')
    b = b.split('.')
    result = []
    for x, y in zip(a, b):
        if x != y:
            break
        result.append(x)
    result = '.'.join(result)
    print('Cross path:\n{}\n{}\n{}'.format(a, b, result))
    return result