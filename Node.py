# !/usr/bin/python
# -*- coding: utf-8 -*-


class Node:
    def __init__(self, database, content):
        self.__content = content
        self.__database = database
        self.__changed = False

    @staticmethod
    def Create(database, _id, _data=None, _type=None, _from=None, _into=None, _relations=None):
        return Node(database, {
            'id': _id,
            'name': _id.split('.')[-1],
            'data': _data,
            'type': _type,
            'from': _from,
            'into': _into,
            'relations': _relations,
        })

    def SetDirty(self):
        self.__changed = True
        self.__database.SetDirty(self)

    @property
    def IsDirty(self):
        return self.__changed

    @property
    def Content(self):
        return self.__content

    @property
    def Id(self):
        return self.__content['id']

    @Id.setter
    def Id(self, value):
        self.__content['id'] = value
        self.SetDirty()

    @property
    def Name(self):
        return self.__content['name']

    @Name.setter
    def Name(self, value):
        self.__content['name'] = value
        self.SetDirty()

    @property
    def Data(self):
        return self.__content['data']

    @Data.setter
    def Data(self, value):
        self.__content['data'] = value
        self.SetDirty()

    @property
    def Type(self):
        return self.__database.GetNode(self.__content['type'])

    @Type.setter
    def Type(self, value):
        self.__content['type'] = value.Id if value else None
        self.SetDirty()

    @property
    def From(self):
        return self.__database.GetNode(self.__content['from'])

    @From.setter
    def From(self, value):
        self.__content['from'] = value.Id if value else None
        self.SetDirty()

    @property
    def Into(self):
        return self.__database.GetNode(self.__content['into'])

    @Into.setter
    def Into(self, value):
        self.__content['into'] = value.Id if value else None
        self.SetDirty()

    @property
    def Relations(self):
        return self.__content['relations']

    @Relations.setter
    def Relations(self, value):
        self.__content['id'] = value
        self.SetDirty()
