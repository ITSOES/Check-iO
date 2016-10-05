class Building:
    def __init__(self, south, west, width_WE, width_NS, height=10):
        self.south, self.west = south, west
        self.width_WE, self.width_NS = width_WE, width_NS
        self.height = height

    def corners(self):
        return {'north-east': [self.south + self.width_NS, self.west + self.width_WE], 
        'south-east': [self.south, self.west + self.width_WE],
        'south-west': [self.south, self.west], 
        'north-west': [self.south + self.width_NS, self.west]}

    def area(self):
        return self.width_WE * self.width_NS

    def volume(self):
        return self.area() * self.height

    def __repr__(self):
        return "Building({south}, {west}, {width_WE}, {width_NS}, {height})".format(**{
            'south': self.south,
            'west': self.west,
            'width_WE': self.width_WE,
            'width_NS': self.width_NS,
            'height': self.height})