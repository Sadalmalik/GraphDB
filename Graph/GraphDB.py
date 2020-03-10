import os
from os import path

from Graph.Functions import *
from Graph.Node import Node


class GraphDB:
    def __init__(self, root_directory):
        os.makedirs(root_directory, exist_ok=True)
        self.__root = root_directory
        self.__index = {}
        self.__dirty = []

    def __NodeToPath(self, node):
        return path.join(self.__root, *node.split('.')) + '.json'

    def GetNode(self, node_id):
        if not node_id:
            return None
        if node_id not in self.__index:
            _path = self.__NodeToPath(node_id)
            if path.isfile(_path):
                js = LoadJson(_path)
                self.__index[node_id] = Node(self, js)
            else:
                return None
        return self.__index[node_id]

    def CreateNode(self, node_id, type_node=None):
        _path = self.__NodeToPath(node_id)
        if path.isfile(_path):
            # Узел есть - откроем его
            return self.GetNode(node_id)
        # Узла нет - создадим
        self.__index[node_id] = Node.Create(self, node_id)
        self.__index[node_id].Type = type_node
        return self.__index[node_id]

    def CreateLink(self, node_from, node_type, node_into):
        name = '{}({}){}'.format(
            node_from.Name,
            node_type.Name,
            node_into.Name)
        cross = GetCrossPath(node_from.Id, node_into.Id)
        node_id = '{}.{}'.format(cross, name)
        node = self.CreateNode(node_id)
        node.From = node_from
        node.Into = node_into
        node.Type = node_type
        return node

    def SaveNode(self, node):
        _path = self.__NodeToPath(node.Id)
        SaveJson(_path, node.Content)

    def SetDirty(self, node):
        self.__dirty.append(node)

    def SaveAllChanges(self):
        for node in self.__dirty:
            self.SaveNode(node)
        self.__dirty.clear()
