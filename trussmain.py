from trusscommands import *



commands = {'help': myhelp, 'add' : add, 'remove' : remove, 'truss' : truss, 'new' : new,\
            'calculatetruss' : calculatetruss, 'load' : load , 'save' : save, 'export' : export}

def startUI():
    print("Welocome to TrussCalculator.")
    while True:
        temp = input('Enter a command:').strip()
        if temp in commands:
            commands[temp]()
        elif temp == 'quit':
            if saved_joints != joints or saved_members != members or saved_supports != supports or saved_loads != loads:
                ans = input("The truss is not saved want to save first? (y/n/c)")
                if ans == 'y':
                    save()
                elif ans == 'c':
                    return
                elif ans != 'n':
                    print('You have to answer (y/n/c)')
                    return
            break
        else:
            print("Unkown command try again")




if __name__ == '__main__':
    startUI()
