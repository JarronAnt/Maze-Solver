
#class to repersent a single point
class Point(object):

    #constructor 
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    #overload add function so that it adds the individual 
    #components of the point
    def __add__(self,o):
        return Point(self.x + o.x, self.y+o.y)

    #overload equal operation
    #make sure the individual compnonets are equal
    def __eq__(self,o):
        return ((self.x == o.x) and (self.y == o.y))

