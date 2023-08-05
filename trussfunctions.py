from trusselements import *
from math import *
import numpy as np


def calculateinternalforces(joints, members, loads, supports):
    internal_forces = list()
    external_forces = list()
    for joint in joints:
        internal_forces_temp_H = []
        internal_forces_temp_V = []
        external_forces_temp_H = []
        external_forces_temp_V = []
        for member in members:
            if member.isconnected(joint):
                angle_radians = member.angle(joint)
                internal_forces_temp_H.append(cos(angle_radians))
                internal_forces_temp_V.append(sin(angle_radians))
            else: 
                internal_forces_temp_H.append(0.0)
                internal_forces_temp_V.append(0.0)
        for support in supports:
            if support.isconnected(joint):
                if support.id == 1:
                    internal_forces_temp_H.append(math.cos(math.radians(support.angle)))
                    internal_forces_temp_V.append(math.sin(math.radians(support.angle)))
                elif support.id == 2:
                    internal_forces_temp_H.append(1.0)
                    internal_forces_temp_V.append(0.0)
                    internal_forces_temp_H.append(0.0)
                    internal_forces_temp_V.append(1.0)
            else:
                if support.id == 1:
                    internal_forces_temp_H.append(0.0)
                    internal_forces_temp_V.append(0.0)
                if support.id == 2:
                    internal_forces_temp_H.append(0.0)
                    internal_forces_temp_V.append(0.0)
                    internal_forces_temp_H.append(0.0)
                    internal_forces_temp_V.append(0.0)
        for load in loads:
            if load.joint == joint:
                external_forces_temp_H.append(load.getxcoef())
                external_forces_temp_V.append(load.getycoef())
            else:
                external_forces_temp_H.append(0.0)
                external_forces_temp_V.append(0.0)
        internal_forces.append(internal_forces_temp_H)
        internal_forces.append(internal_forces_temp_V)
        external_forces.append(-sum(external_forces_temp_H))
        external_forces.append(-sum(external_forces_temp_V))
    Amatrix = np.array(internal_forces)
    bmatrix = np.array(external_forces)
    try:
        condition = np.linalg.cond(Amatrix)
        if condition > 100:
            print("Warning the system may be ill-conditioned an thus the truss is unstable.")
        temp = np.linalg.solve(Amatrix, bmatrix).tolist()
    except np.linalg.LinAlgError:
        print("The truss is not statically determined.")
        return
    for i in range(len(members)):
        members[i].giveload(round(temp[i],2))
        k = 1
    for n in range(len(supports)):
        if supports[n].id == 1:
            supports[n].givevalue(round(temp[i+k], 2))
            k =+ 1
        elif supports[n].id == 2:
            supports[n].givexcoef(round(temp[i+k],  2))
            supports[n].giveycoef(round(temp[i+k+1], 2))
            k =+ 2

def resettocalculate(supports, members):
    for element in supports:
        element.reset()
    for element in members:
        element.reset()
       

if __name__ == "__main__":
    joints = (Joint('A',0, 0), Joint('B',2 ,0), Joint('C',1, 1))
    members = (Member(joints[0], joints[1]), Member(joints[1], joints[2]), Member(joints[0], joints[2]))
    loads = ([Load(joints[2], 100, 270)])
    supports = (RollerSupport(joints[0], 90), PinnedSuppport(joints[1]))
    calculateinternalforces(joints, members, loads, supports)
    for member in members:
        print("Internal load is:", member.load)
    print("Support load is:", supports[0].value)
    print("Support loadx is ", supports[1].xcoef)
    print("Support loady is ", supports[1].ycoef)
