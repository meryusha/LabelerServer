class Category(object):
    #when new class is created - has no color
    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError("Not a String")
        self._name = name.lower()
        self._color = None
    
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Not a String")
        self._name = value.lower()

    @property
    def color(self):
        return self._color 
    
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise ValueError("Not a String")
        self._color = value.lower()

    def __eq__(self, other):
        if not isinstance(other, Category):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.name == other.name
    