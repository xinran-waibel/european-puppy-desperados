import math

class Vector2:
    ### vector 2 is a basic 2d vector with properties x for the x coordinate and y for the y coordinate

    ### the init function can take in and x, y coordinates, another Vector2, or a tuple (x, y)
    def __init__(self, x, y):
        if y is None:
            if type(x) is Vector2:
                self.x = x.x
                self.y = x.y
            else:
                self.x = x[0]
                self.y = x[1]
        else:
            self.x = x
            self.y = y

    ### zeroes the magnitude of this vector
    def zero(self):
        self.x = 0
        self.y = 0

    ### returns the dot product of this vector and another
    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y
    
    ### sets this vector to be another
    def set(self, vector):
        self.x, self.y = vector.x, vector.y
        return self
    
    ### sets the x and y values of the vector
    def set_values(self, x, y):
        self.x, self.y = x, y
        return self
    
    ### sets the values from a tuple (x, y)
    def set_tuple(self, tuple):
        self.x, self.y = tuple[0], tuple[1]
        return self

    ### returns the tuple (x, y)
    def tuple(self):
        return (self.x, self.y)
    
    ### returns a vector that is this vector added to another
    def plus(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)
    
    ### returns a vector that is this vector subtract another
    def minus(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)
    
    ### returns a vector that is this vector scaled by a given scaler
    def multiply(self, scaler):
        return Vector2(self.x * scaler, self.y * scaler)
    
    ### adds a number to the x component and a number to the y component of the vector
    def add(self, x, y):
        self.x += x
        self.y += y
        return self
    
    ### subtracts a number to the x component and a number to the y component of the vector
    def sub(self, x, y):
        self.x -= x
        self.y -= y
        return self
    
    ### adds a number to the x component of the vector
    def addX(self, x):
        self.x += x
        return self
    
    ### adds a number to the y component of the vector
    def addY(self, y):
        self.y += y
        return self

    ### returns a copy of the vector
    def copy(self):
        return Vector2(self.x, self.y)

    ### scales the vector by a given scaler
    def scale(self, scaler):
        self.x *= scaler
        self.y *= scaler
        return self

    ### flips the vector
    def flip(self):
        return self.scale(-1)
    
    ### returns the length squared of the vector
    def lengthSquared(self):
        return self.x * self.x + self.y * self.y

    ### returns the length of the vector
    def length(self):
        return math.sqrt(self.lengthSquared())

    ### normalizes the vector
    def normalize(self):
        if(self.lengthSquared() == 0.0):
            return self
        else:
            return self.scale(1.0 / self.length())

    ### rotates the vector by an angle in radians
    def rotate(self, angle):
        x = self.x
        y = self.y

        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = x * math.sin(angle) - y * math.cos(angle)

        return self