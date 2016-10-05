class Friends:
    def __init__(self, connections):
        self.connections = {frozenset(x) for x in connections}

    def add(self, connection):
        result = not connection in self.connections
        self.connections.add(frozenset(connection))
        return result

    def remove(self, connection):
        result = connection in self.connections
        self.connections.discard(connection)
        return result

    def names(self):
        return {x for y in self.connections for x in y}

    def connected(self, name):
        return {y for x in self.connections if name in x for y in x - {name}}