import math





class Joint:
    def __init__(self, name, x, y):
        assert type(x) == float or type(x) == int , "x coordinate has to be a float"
        assert type(y) == float or type(x) == int, "y coordinate has to be a float"
        self.x = x
        self.y = y
        self.name = name
    
    def __str__(self):
        return self.name


class Member:
    def __init__(self, joint1, joint2):
        assert type(joint1) == Joint and type(joint2) == Joint , "You have to give to Joints"
        self.joint1 = joint1 
        self.joint2 = joint2
       
 
    def isconnected(self, joint):
        assert type(joint) == Joint ,'the tested join has to be type Joint'
        if self.joint1 == joint:
            self.otherjoint = self.joint2
            return True
        elif self.joint2 == joint:
            self.otherjoint = self.joint1
            return True
        else: return False
   

    def angle(self, joint):
        assert type(joint) == Joint , "joint has to be type Joint"
        anglevar = math.atan2(self.otherjoint.y - joint.y, self.otherjoint.x - joint.x)
        return anglevar
    
    def giveload(self, load):
        self.load = load

    def reset(self):
        self.load = None
        self.otherjoint = None



class Load:
    def __init__(self, joint, value, angle):
        assert type(joint) == Joint ,'first argument has to be a joint'
        self.joint = joint
        self.value = value
        self.angle = angle
        self.xcoef = None
        self.ycoef = None


    def getxcoef(self):
        assert self.value != None ,"the value of the support has to ve found in order to calculate the coeficients"
        if self.xcoef == None:
            self.xcoef =(self.value * math.cos(math.radians(self.angle)))
            return self.xcoef
        else: return self.xcoef

    
    def getycoef(self):
        assert self.value != None ,"the value of the support has to ve found in order to calculate the coeficients"
        if self.ycoef == None:
            self.ycoef = (self.value * math.sin(math.radians(self.angle)))
            return self.ycoef
        else: return self.ycoef


class RollerSupport:
    def __init__(self, joint, angle):
        assert type(joint) == Joint, 'first argument has to be a joint'
        self.joint = joint
        self.angle = angle
        self.id = 1
        self.value = None
        self.xcoef = None
        self.ycoef = None


    def givevalue(self, value):
        self.value = value

    
    def isconnected(self, joint):
        if self.joint == joint:
            return True
        else: return False

    
    def getxcoef(self):
        assert self.value != None ,"the value of the support has to ve found in order to calculate the coeficients"
        if self.xcoef == None:
            self.xcoef =(self.value * math.cos(math.radians(self.angle)))
            return self.xcoef
        else: return self.xcoef

    
    def getycoef(self):
        assert self.value != None ,"the value of the support has to ve found in order to calculate the coeficients"
        if self.ycoef == None:
            self.ycoef = self.value * math.sin(math.radians(self.angle))
            return self.ycoef
        else: return self.ycoef

    
    def reset(self):
        self.value = None
        self.xcoef = None
        self.ycoef = None



class PinnedSuppport(RollerSupport):
    def __init__(self, joint):
        assert type(joint) == Joint ,'first argument has to be a joint'
        self.joint = joint
        self.id = 2
        self.angle = None
        self.value = None
        self.xcoef = None
        self.ycoef = None
    

    def givexcoef(self, value):
        self.xcoef = value

    
    def giveycoef(self, value):
        self.ycoef = value


    def getangle(self):
        assert self.xcoef != None and self.ycoef != None , "both coeficients need to be defined in order to calculate angle"
        if self.angle != None:
            self.angle = math.arctan2(self.ycoef, self.xcoef)
            return self.angle
        else: return self.angle
    

    def reset(self):
        self.value = None
        self.xcoef = None
        self.ycoef = None
        self.angle = None
