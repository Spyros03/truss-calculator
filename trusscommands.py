from trusselements import *
from trussfunctions import *




joints= dict()
members= dict()
supports= dict()
loads= dict()
saved_joints = joints
saved_members = members
saved_supports = supports
saved_loads = loads


def myhelp():
    print("help: Informs about all the available commands.")
    print("add: Add a truss element such is (joint, member, load, support).")
    print("remove: Remove a truss element such is (joint, member, load, support).")
    print("truss: Lists all the elements of the current truss.")
    print("calculatetruss: Calculates all the internal forces of the members")
    print("new: Creates a new truss.")
    print("load: Loads a truss from a '.truss' file.")
    print("save: Saves a truss to a '.truss' file.")
    print("export: Exports the calculated results to '.txt' file.")
    print("quit: Exits the program.")


def add():
    while True:
        type = input("Enter the type of truss element that is being added:")
        if type == 'joint':
            name = input('Input joint name:')
            strcoords = input("Enter coordinates as (x,y):")
            coords = (strcoords.split(','))
            joints.update({name : Joint(name, float(coords[0]), float(coords[1]))})
        elif type == 'member':
            name = input('Input member name:')
            firstjoint = input('Enter first joint:')
            secondjoint = input('Enter the second joint:')
            if firstjoint not in joints.keys() or secondjoint not in joints.keys():
                print("Joint not found.")
                continue
            members.update({name : Member(joints[firstjoint], joints[secondjoint])})
        elif type == 'support':
            while True:
                name = input('Input support name:')
                type = input('Input support type (roller, pinned):')
                attjoint = input('Input attached join:')
                if attjoint not in joints.keys():
                        print("Joint not found.")
                        continue
                if type == 'pinned':
                    supports.update({name : PinnedSuppport(joints[attjoint])})
                elif type == 'roller':
                    supportangle = float(input("Enter the angle of the support:"))
                    supports.update({name : RollerSupport(joints[attjoint], supportangle)})
                elif type == 'c' or type == 'cancel':
                    break
                else:
                    print('Wrong type try again')
                    continue
        elif type == 'load':
            while True:
                attjoint = input('Give the joint which is the load applied:')
                if attjoint not in joints.keys():
                    print("Joint not found.")
                    continue
                name = input('Give the name of the load:')
                attr = input('Give value and angle of the load:').split()
                try:
                    loads.update({name : Load(joints[attjoint], attr[0], attr[1])})
                except:
                    print("Something went wrong.")
                    continue
        elif type == 'c' or type == 'close':
            break
        else:
            print("Unkown command please try again")
            

def remove():
    while True:
        type = input("Enter the type of truss element that is being removed and name:")
        if type[0] == 'joint':
            for member in members:
                if member.isconnected(type[1]):
                    members.pop(member)
            for load in loads:
                if load.joint == type[1]:
                    load.pop(load)
            for support in supports:
                if support.joint == type[1]:
                    support.pop(support)
            joints.pop(type[1])
        elif type[0] == 'member':
            members.pop(type[1])
        elif type[0] == 'support':
            support.pop(type[1])
        elif type[0] == 'load':
            load.pop(type[1])
        elif type[0] == 'c' or type [0] == 'close':
            break
        else:
            print("Unkown commadn try again.")


def truss():
    print("Joints:")
    print("            Name             xcoord               ycoord")
    joints_tup = joints.items()
    for joint in joints_tup:
        print('            {:<10s}       {:<6.2f}               {:<6.2f}'.format(joint[0], joint[1].x, joint[1].y))
    print("Members:")
    print("            Name             joint1               joint2 ")
    members_tup = members.items()
    for member in members_tup:
        print('            {:<10s}       {:<10s}           {:<10s}'.format(member[0], member[1].joint1.name, member[1].joint2.name))
    print("Supports:")
    print("            Name             joints               type               angle")
    supports_tup = supports.items()
    for support in supports_tup:
        if support[1].id == 1:
            print('            {:<10s}       {:<10s}           {:<1d}                  {:<6.2f}'.format(support[0], support[1].joint.name, support[1].id, support[1].angle))
        else:
            print('            {:<10s}       {:<10s}           {:<1d}                  None'.format(support[0], support[1].joint.name, support[1].id))
    print("Loads:")
    print("            Name             joints               value              angle")
    loads_tup = loads.items()
    for load in loads_tup:
        print('            {:<10s}       {:<10s}           {:<6.2f}             {:<6.2f}'.format(load[0], load[1].joint.name, load[1].value, load[1].angle))


def calculatetruss():
    members_tup = list(members.values())
    supports_tup = list(supports.values())
    loads_tup = list(loads.values())
    joints_tup = list(joints.values())
    resettocalculate(supports_tup, members_tup)
    calculateinternalforces(joints_tup, members_tup, loads_tup, supports_tup)
    members_tup = members.items()
    supports_tup = supports.items()
    print(" ")
    print("MemberName          Load           LoadType")
    print("-------------------------------------------")
    for member in members_tup:
        if member[1].load > 0:
            loadtype = 'tensile'
        elif member[1].load < 0:
            loadtype = 'compresive'
        else: loadtype = 'neutral'
        print("{:<10s}          {:<+7.2f}        {:<10s}".format(member[0], member[1].load, loadtype))
    print(" ")
    print("SupportName         xLoad          yload")
    print("----------------------------------------")
    for support in supports_tup:
        if support[1].id == 1:
            print("{:<11s}         {:<+7.2f}        {:<+7.2f}".format(support[0], support[1].getxcoef(), support[1].getycoef()))
        else:
            print("{:<11s}         {:<+7.2f}        {:<+7.2f}".format(support[0], support[1].xcoef, support[1].ycoef))


def save():
    while True:
        filename = input("Select file to save:")
        f = open(filename + '.truss', 'x')
        notoverride = False
        if f == -1:
            while True:
                ans = input("The file already exist do you wish to override (yes/no)?")
                if ans == 'yes': notoverride = False
                elif ans == 'no': notoverride = True
                else:
                    print("Please answer yes or no.")
                    continue
        if notoverride:
            f.close()
            continue
        f.close()
        f = open(filename + ".truss", "w")
        break
    f.write("Joints:\n")
    f.write("            Name            Xcoord            Ycoord\n")
    joints_tup = joints.items()
    for joint in joints_tup:
        f.write("            {:<10s}       {:<6.2f}               {:<6.2f}\n".format(joint[0], joint[1].x, joint[1].y))
    f.write("Members:\n")
    f.write("            Name             joint1               joint2\n")
    members_tup = members.items()
    for member in members_tup:
        f.write("            {:<10s}       {:<10s}           {:<10s}\n".format(member[0], member[1].joint1.name, member[1].joint2.name))
    f.write("Supports:\n")
    f.write("            Name             joints               type               angle\n")
    supports_tup = supports.items()
    for support in supports_tup:
        if support[1].id == 1:
            f.write("            {:<10s}       {:<10s}           {:<1d}                  {:<6.2f}\n".format(support[0], support[1].joint.name, support[1].id, support[1].angle))
        else:
            f.write("            {:<10s}       {:<10s}           {:<1d}                  None\n".format(support[0], support[1].joint.name, support[1].id))
    f.write("Loads:\n")
    f.write("            Name             joints               value              angle\n")
    loads_tup = loads.items()
    for load in loads_tup:
        f.write("            {:<10s}       {:<10s}           {:<6.2f}             {:<6.2f}\n".format(load[0], load[1].joint.name, load[1].value, load[1].angle))
    saved_joints = joints
    saved_members = members
    saved_supports = supports
    saved_loads = loads
    print("Truss saved successfully.")


def export():
    while True:
        filename = input("Select file to export:")
        f = open(filename + ".txt", "x")
        notoverride = False
        if f == -1:
            while True:
                ans = input("The file already exist do you wish to override (yes/no)?")
                if ans == "yes": notoverride = False
                elif ans == "no": notoverride = True
                else:
                    print("Please answer yes or no.")
                    continue
        if notoverride:
            f.close()
            continue
        f.close()
        f = open(filename + ".txt", "w")
        break
    members_tup = members.items()
    supports_tup = supports.items()
    f.write("MemberName          Load           LoadType\n")
    f.write("----------------------------------------------\n")
    try:
        for member in members_tup:
            if member[1].load > 0:
                loadtype = "tensile"
            elif member[1].load < 0:
                loadtype = "compresive"
            else: loadtype = "neutral"
            f.write("{:<10s}          {:<+7.2f}        {:<10s}\n".format(member[0], member[1].load, loadtype))
        f.write("\n")
        f.write("SupportName         xLoad          yload\n")
        f.write("-------------------------------------------\n")
        for support in supports_tup:
            if support[1].id == 1:
                f.write("{:<11s}         {:<+7.2f}        {:<+7.2f}\n".format(support[0], support[1].getxcoef(), support[1].getycoef()))
            else:
                f.write("{:<11s}         {:<+7.2f}        {:<+7.2f}\n".format(support[0], support[1].xcoef, support[1].ycoef))
        print("The results were exported successfuly.")
    except (AssertionError, ValueError, AttributeError):
            print("The truss is not caclulated and can not be exported calculate the truss first.")




def load():
    filename = input("Input the file you wish to open:")
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        print("File not found try again.")
        return
    def getline():
        while True:
            dline = file.readline()
            if dline == '':
                return dline
            dline = dline.split('#')[0]
            if dline.strip() != '':
                return dline
    try:
        dline = getline()
        if dline.strip() != 'Joints:':
            print("There was an error with the file.")
            return
        dline = getline()
        while True:
            dline = getline()
            if dline.strip() == "Members:":
                break
            dline = dline.split()
            joints.update({dline[0] : Joint(dline[0], float(dline[1]), float(dline[2]))})
        dline = getline()
        while True:
            dline = getline()
            if dline.strip() == "Supports:":
                break
            dline = dline.split()
            members.update({dline[0] : Member(joints[dline[1]], joints[dline[2]])})
        dline = getline()
        while True:
            dline = getline()
            if dline.strip() == "Loads:":
                break
            dline = dline.split()
            if dline[2] == "1":
                supports.update({dline[0] : RollerSupport(joints[dline[1]], float(dline[3]))})
            elif dline[2]  == "2":
                supports.update({dline[0] : PinnedSuppport(joints[dline[1]])})
            else:
                print("Something went wwrong try again.")
                return
        dline = getline()
        while True:
            dline = getline()
            if dline == '':
                break
            dline = dline.split()
            loads.update({dline[0]: Load(joints[dline[1]], float(dline[2]), float(dline[3]))})
        saved_joints = joints
        saved_members = members
        saved_supports = supports
        saved_loads = loads
        print("Truss loaded successfully.")
    except: 
        print("Something went wrong with the file try again.") 
        return 
 
    


def new():
    if saved_joints != joints or saved_members != members or saved_supports != supports or saved_loads != loads:
        ans = input("The truss is not saved want to save first? (y/n/c)")
        if ans == 'y':
            save()
        elif ans == 'c':
            return
        elif ans != 'n':
            print('You have to answer (y/n/c)')
            return
    joints= dict()
    members= dict()
    supports= dict()
    loads= dict()

   