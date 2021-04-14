#! /usr/bin/python3
#import ../bin/smqs
import time as t
import sys
import readline
sys.path.append("progs/")
import schoolsim_smqs
import schoolsim_bjcurses
import schoolsim_buzzwords
import random
import datetime
import os



class Obj:
    def __init__(self, name, uses):
        self.name = name
        self.uses = uses

    def use(self):
        for x in range(0, 3):
            print("Using...")
            t.sleep(0.5)
        print("Used!")
        self.uses -= 1

class Player:
    def __init__(self, name, inv, loc, traits):
        self.name = name
        self.inv = inv
        self.gradepad = 0
        self.loc = loc
        self.traits = traits
        self.wakinghours = 1.5

        if "rich" in self.traits:
            self.bux = 50
        elif "alex" in self.traits:
            self.bux = 75
        else:
            self.bux = 10

        if "pet" in self.traits:
            self.reps = 30
            self.rept = 60
            self.traits.append("tired")
            self.reptbonusdone = False
        else:
            self.reps = 60
            self.rept = 60

        if "cool" in self.traits:
            self.repsbonusdone = False


    def use(self, obj):
        if obj in self.inv:
            self.inv[obj].use()

    def getinv(self):
        counter = 1
        for item in self.inv.values():
            print(str(counter) + ": " + item.name + ", " + str(item.uses) + " uses left")
            counter += 1

    def go(self, loc):
        self.loc = loc


def say(text, speed=0.05):
    for char in text:
        print(char, end="")
        sys.stdout.flush()
        t.sleep(speed)
    print()

def frmtlist(inlist):
    result = ""
    for item in inlist:
        result += item + ","
    return result[:-1]

def strtodict(string):
    if string != "{}":
        string = string[1:-1] #remove brackets
        string = string.split(", ") # split to k-v pairs
        for item in string:
            item = item.split(": ") # split keys and vals
        print("Split up", string)


        result = {}
        c = 0
        while c < len(string):
            result[string[c][1:-1]] = string[c+1][1:-1]
            print("strc", string[c][1:-1])
            c += 2
        print("res", result)
        return result
    
    else:
        return {}

def goforth(player, asleep, time):
    yes = ["Y", "y", "yes"]
    no = ["N", "n", "no"]
    time += 0.5
    player.wakinghours += 0.5
    if player.reps > 120:
        player.reps = 120
    if player.rept > 120:
        player.rept = 120

    if "tired" in player.traits and player.gradepad > -3:
        player.gradepad -= 1

    if "cool" in player.traits and not player.repsbonusdone:
        player.reps += 2
        if player.reps >= 90:
            player.repsbonusdone = True

    if "pet" in player.traits and not player.reptbonusdone:
        player.rept += 2
        if player.rept >= 90:
            player.reptbonusdone = True

    if ("cool" in player.traits) and (player.reps < 30):
        player.traits.remove("cool")
        del player.repsbonusdone
        print("You were so uncool that you aren't cool anymore.")
    
    if ("pet" in player.traits) and (player.rept < 30):
        player.traits.remove("pet")
        del player.reptbonusdone
        print("The teachers hated you so much that you aren't their pet anymore/")

    if player.wakinghours >= 13:
        if "tired" not in player.traits:
            player.traits.append("tired")


    if (player.loc in ["cafe", "lib", "main"]) and (time >= 8.5) and (time <= 15):
        player.rept -= 10
        if player.rept < 1:
            say("\"HEY! What are you doing out of class again?\"")
            t.sleep(3)
            say("\"Your actions have convinced us that you do not want to go here.\"")
            t.sleep(1)
            say("\"You will be sent to prison tomorrow.\"",)
            print("\nGame over.")
            sys.exit()
    rand_enc = random.randint(1, 5) 
    
    if not asleep:
        if rand_enc == 5:
            
            if "with_knifeb" not in player.traits:

                if "with_knife" in player.traits:
                    say("\"wao...\"")
                    say("\"HOOMAN HAZ NAIF!\"")
                    say("\"RUN AWAY!!!\"")
                    print("The owl army disperses.")
                    player.traits.append("with_knifeb")
                else:
                    say("\"The OWL ARMY haz captured u!!!!!!!!\"", 0.05)
                    say("\"We wil now taek r PAYMINT!\"", 0.05)
                    if player.bux > 9:
                        player.bux -= 10
                        print("You lost 10 bux.")
                    else:
                        say("\"...\"", 0.5)
                        t.sleep(2)
                        say("\"Hooman dosnt hav r PAEMANT!\"")
                        say("\"Thiss INNSIHDUNT wil be weported!\"")
                        say("\"You're DAEZ r numbred!\"")
                        player.rept = 0
                        print("You will be sent to prison once you move from this room.")

        elif rand_enc == 1:
            if "with_knife" not in player.traits:
                print("You find a knife.")
                take_yorn = input("Do you take it?").lower()
                if take_yorn in yes:
                    player.traits.append("with_knife")
                    player.rept -= 20
                    print("You take the knife.")
                else:
                    print("You leave the knife there.")
                    with open("ascii/sad-knife", "r") as sad_knife:
                            sad_knifestr = sad_knife.read()
                    print(sad_knifestr)

    else:
        if rand_enc == 5:
            if player.bux > 9:
                player.bux -= 10
                print("The Owl Army robbed you in your sleep.")
            else:
                print("You will be sent to prison once you step out of this room.")
    return time

            

def main(): # start a game from another program
    yes = ["Y", "y", "yes"]
    no = ["N", "n", "no"]
    saveorno = input("Use a save?").lower()
    if saveorno in no:
        coffeenum = 0
        bjnum = 0
        time = 8.5

        playername = input("What is your name? ")
        
        playertrait = 0
        while playertrait not in ["1", "2", "3", "4"]:
            playertrait = input(
            """Select a trait:

            1. Cool
            2. Pet
            3. Rich
            """)

            if playertrait == "1":
                playertrait = "cool"
                break
            elif playertrait == "2":
                playertrait = "pet"
                break
            elif playertrait == "3":
                playertrait = "rich"
                break
            elif playertrait == "4":
                playertrait = "alex"
                break
            else:
                print("\nChoose 1, 2, or 3", file=sys.stderr)

        player = Player(playername, {}, "main", [playertrait])

        print("Go to school")

    elif saveorno in yes:
        if os.name == "posix":
            saves = os.popen("ls -1r saves/").read().split("\n")
        elif os.name == "nt":
            print(os.popen("dir /-O saves\\").read())
            saves = os.popen("dir /-O saves\\").read().split("\n")[:-2][7:]
            for x in saves:
                x = x[38:]
                print(x)
        for x in range(0, len(saves)-1):
            print(f"{x}: {saves[x]}")
        savetouse = int(input("Type the name of the save you want to use: "))
        with open("saves/"+saves[savetouse]) as savefiletouse:
            savestring = savefiletouse.read()
            unprocvarlist = savestring.split("\n")
            varlist = []
            for x in unprocvarlist:
                if x[:3] != "inv":
                    varlist.append(x.split(": "))
                else:
                    varlist.append(x.split(": ", 1))
            varlist = varlist[:-1]
            vardic = {}
            print("varlist", varlist)
            input()
            for item in varlist:
                try:
                    vardic[item[0]] = int(item[1])
                except ValueError:
                    if "," in item[1] and item[1][0] != "{":
                        vardic[item[0]] = item[1].split(",")
                    elif "{" == item[1][0]:
                        vardic[item[0]] = strtodict(item[1])
                    else:
                        vardic[item[0]] = item[1]
            print(vardic)
            player = Player(vardic["name"], vardic["inv"], vardic["loc"], vardic["traits"])
            player.gradepad = int(vardic["gradepad"])
            player.wakinghours = float(vardic["wakinghours"])
            player.bux = int(vardic["bux"])
            player.reps = int(vardic["reps"])
            player.rept = int(vardic["rept"])
            if "repsbonusdone" in vardic:
                player.repsbonusdone = vardic["repsbonusdone"]
            if "reptbonusdone" in vardic:
                player.reptbonusdone = vardic["reptbonusdone"]

            coffeenum = int(vardic["coffeenum"])
            bjnum = int(vardic["bjnum"])
            time = float(vardic["time"])


    while True:
        
        cmd = input("> ")

        if cmd == "":
            continue
        else:
            cmd = cmd.lower()
            cmd = cmd.strip()
            cmd = cmd.split()
            
            if cmd[0] == "go":
                time = goforth(player, False, time)

                        
            if (cmd[0] == "go") and (cmd[1] in ["l", "lib", "library"]) and (player.loc != "lib") and (player.loc not in ["math"]):
                player.loc = "lib"
            
            elif (cmd[0] == "go") and (cmd[1] in ["c", "cafe", "café"]) and (player.loc != "cafe") and (player.loc not in ["math"]):
                player.loc = "cafe"

            elif cmd[0] == "go" and cmd[1] in ["m", "main"] and player.loc != "main":
                player.loc = "main"

            elif cmd[0] == "go" and cmd[1] in ["ma", "math"] and player.loc == "main" and player.loc != "math":
                mathscore = schoolsim_smqs.main()
                if mathscore > 10:
                    for x in range(0, 100000):
                        print("E", end="")
                        player.rept = 120
                        player.reps = 120
                    print()
                
                elif 11 > mathscore > 8:
                    print("You got an A, nerd.")
                    player.rept += 10
                    if "cool" in player.traits:
                        player.reps += 10

                elif 6 < mathscore < 9:
                    print("B stands for bad.")
                    player.rept += 7
                    if "cool" in player.traits:
                        player.reps += 7
                
                elif mathscore == 6:
                    print("You got a C")
                    
                elif 1 < mathscore < 6:
                    print("You got a D, delightful")
                    player.rept -= 7
                    if "cool" in player.traits:
                        player.reps -= 7

                elif -1 < mathscore < 2:
                    print("You got an F.")
                    player.rept -= 10
                    if "cool" in player.traits:
                        player.reps -= 10
            
            
            # use
            elif cmd[0] in ["u", "use"]:
                try:
                    player.use(cmd[1])
                    if (player.inv[cmd[1]].uses == 0) and (player.inv[cmd[1]].name[0:6] == "coffee"):
                        del player.inv[cmd[1]]
                        if "tired" in player.traits:
                            player.traits.remove("tired")

                except KeyError:
                    print("That object doesn't exist!", file=sys.stderr)

            elif cmd[0] in ["slp", "sleep"]:
                for x in range(0, 5):
                    print("Zzzzzz...")
                    goforth(player, True, time)

                player.wakinghours = 0
                player.traits.remove("tired")
            
            elif cmd[0] in ["i", "inv", "inventory"]:
                player.getinv()

            elif player.loc == "cafe" and cmd[0] == "buy":
                if player.bux > 4:
                    obj = Obj(f"coffee-{coffeenum}", 3)
                    player.inv[obj.name] = obj
                    coffeenum += 1
                    player.bux -= 5
                    print("Avery says to you: ", end="")
                    say(f"\"{schoolsim_buzzwords.genBuzzword()} is going to be the next big thing!\"")
            
            elif player.loc == "cafe" and cmd[0] == "bj":
                if "killed_john" not in player.traits:
                    if bjnum == 0:
                        say("\"Hi, I'm John, and I have the magical power to sit here all day.\"")
                        say("\"Would you like to play blackjack?\"")
                        bjnum = 1
                        if input() in yes:
                            say("\"Ok good I really need money.\"")
                            prevbux = player.bux
                            player.bux = schoolsim_bjcurses.main(False, player.bux)
                            player.reps = player.bux - prevbux
                        
                        else:
                            say("\"Then why are you here? (just to suffer?)\"")
                            
                        

                    if "with_knife" in player.traits and "killed_john" not in player.traits:
                        stab_or_no = input("Stab him for a hundred bux?")
                        
                        if stab_or_no in yes:
                            say("\"*gasp* What is that?!\"")
                            say("\"AAAAHHHHHHH\"")
                            print("John falls dead on the floor.")
                            player.bux += 100
                            player.traits.append("killed_john")
                            caughtchance = random.randint(1, 2)
                            if caughtchance == 1:
                                say("\"What the hell!?\"")
                                say("\"GUARDS!!\"")
                                print("You were sent to death row.")
                                t.sleep(1)
                                print("Why would you kill someone in a public place?")
                                t.sleep(1)
                                with open("ascii/jail", "r") as jail:
                                        jailstr = jail.read()
                                print(jailstr)
                                sys.exit()

                        else:
                            player.bux = schoolsim_bjcurses.main(False, player.bux) 


                else:
                    print("There is no one to play blackjack with.")


                


            elif player.loc == "lib" and cmd[0] == "read":
                for x in range(0, 3):
                    print("Reading...")
                    t.sleep(0.5)
                print("Read!")

                if player.rept < 120:
                    player.rept += 1
                else:
                    print("rept full")
                
                if player.gradepad < 3:
                    player.gradepad += 1
                else:
                    print("Gradepad full", file=sys.stderr)

            #say
            elif cmd[0] in ["s", "say"]:
                if cmd[1] in ["t", "time"]:
                    print(time)
                elif cmd[1] == "rept":
                    print(player.rept)
                elif cmd[1] == "reps":
                    print(player.reps)
                elif cmd[1] in ["l", "loc", "location"]:
                    print(player.loc)
                elif cmd[1] in ["g", "gpd", "gradepad"]:
                    print(player.gradepad)
                elif cmd[1] in ["t", "tra", "traits"]:
                    print(player.traits)
                elif cmd[1] in ["b", "bux"]:
                    print(player.bux)
                elif cmd[1] in ["w", "wkh", "wakinghours"]:
                    print(player.wakinghours)

            elif cmd[0] in ["q", "quit", "exit"]:
                sys.exit()

            elif cmd[0] in ["save"]:
                if input("Really save?").lower() in yes:
                    if os.name == "posix":
                        thedate = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                    elif os.name == "nt":
                        thedate = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
                    with open(f"saves/{thedate}", "w") as savefile:
                        if "cool" in player.traits:
                            savefile.write(
                                    f"name: {player.name}\n"
                                    f"inv: {player.inv}\n"
                                    f"gradepad: {player.gradepad}\n"
                                    f"loc: {player.loc}\n"
                                    f"traits: {frmtlist(player.traits)}\n"
                                    f"wakinghours: {player.wakinghours}\n"
                                    f"bux: {player.bux}\n"
                                    f"reps: {player.reps}\n"
                                    f"rept: {player.rept}\n"
                                    f"repsbonusdone: {player.repsbonusdone}\n"
                                    f"coffeenum: {coffeenum}\n"
                                    f"bjnum: {bjnum}\n"
                                    f"time: {time}\n"
                            )

                        elif "pet" in player.traits:
                            savefile.write(
                                    f"name: {player.name}\n"
                                    f"inv: {player.inv}\n"
                                    f"gradepad: {player.gradepad}\n"
                                    f"loc: {player.loc}\n"
                                    f"traits: {frmtlist(player.traits)}\n"
                                    f"wakinghours: {player.wakinghours}\n"
                                    f"bux: {player.bux}\n"
                                    f"reps: {player.reps}\n"
                                    f"rept: {player.rept}\n"
                                    f"reptbonusdone: {player.reptbonusdone}\n"
                                    f"coffeenum: {coffeenum}\n"
                                    f"bjnum: {bjnum}\n"
                                    f"time: {time}\n"
                            )

                        else:
                            savefile.write(
                                    f"name: {player.name}\n"
                                    f"inv: {player.inv}\n"
                                    f"gradepad: {player.gradepad}\n"
                                    f"loc: {player.loc}\n"
                                    f"traits: {frmtlist(player.traits)}\n"
                                    f"wakinghours: {player.wakinghours}\n"
                                    f"bux: {player.bux}\n"
                                    f"reps: {player.reps}\n"
                                    f"rept: {player.rept}\n"
                                    f"coffeenum: {coffeenum}\n"
                                    f"bjnum: {bjnum}\n"
                                    f"time: {time}\n"
                            )


                        savefile.close()
                        sys.exit()

            else:
                print(f"Unknown command \"{cmd[0]}\".", file=sys.stderr)
        


        



if __name__ == "__main__":
    import os
    import atexit

    histfile = os.path.join(os.path.expanduser("~"), ".python_history")
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass
    main()
