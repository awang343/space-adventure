import time
import random
import string


class person:
    def __init__(self):
        self.location=1
        self.floor=1
        self.energy=100
        self.inventory=[]
        self.name=""
        self.numOfRoomChanges=0

    #The function that runs everytime the player changes rooms
    def changeLoc(self,locationNumber,roomList):
        #Check if the player is out of energy
        if self.energy==0:
            print("GAME OVER. YOUR PACK RAN OUT OF ENERGY.")
            time.sleep(5)
            main()
        #Update the number of room changes. In the time it takes for the user to move across three rooms, the code for the communication dept will change
        self.numOfRoomChanges+=1
        if self.numOfRoomChanges%3==0:
            roomList[11].code=str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))

        #When the change rooms, the communication dept will be locked (i.e. the communication dept locks when you leave it)
        roomList[11].locked=True

        #Energy use each time you change rooms
        self.energy-=10
        self.printStatusReport()

        #Changing the location of the player
        self.location=locationNumber

    #The function used to print the current energy level of the player
    def printStatusReport(self):
        print("Remaining energy in pack: "+str(self.energy)+"%")
class location:
    def __init__(self,locationNumber,name,connectedRooms,roomDescription,locked):
        self.locationNumber=locationNumber
        self.roomName=name
        self.connectedRooms=connectedRooms
        self.roomDescription=roomDescription
        self.locked=locked
        self.visitedBefore=False
class item:
    def __init__(self,itemID,name,originalLocation,useLocation,itemFunction,itemDescription,descriptionWhenObtained):
        self.ID=itemID
        self.name=name
        self.originalLocation=originalLocation
        self.useLocation=useLocation
        self.function=itemFunction
        self.description=itemDescription
        self.descriptionWhenObtained=descriptionWhenObtained
        self.pickedUp=False
    #The useItem function runs the function corresponding to the item
    def useItem(self,user,roomList,itemList):
        if self in user.inventory and (user.location==self.useLocation or self.useLocation==None):
            print("You used the "+self.name)
            self.function(user,roomList,itemList)
        else:
            print("You cannot use that item here.")

#Whenever an input is needed from the user, the game runs this function. All the options for that particular situation are specified in the phrases argument as a list
def userOption(phrases,textIfInvalid):
    while True:
        i=input("> ").upper()
        for index in range(len(phrases)):
            if phrases[index] in i:
                return phrases[index]
        print(textIfInvalid)

#Function used to setup the game, returns the newly created user, roomList, and itemList
def setup():
    #USER SETUP: creates the user object
    user=person()

    #ROOM SETUP: creates all the room objects
    roomNames=["ELEVATOR","BRIEFING CHAMBER","LAUNCH DOCK","ARMOURY","COMMANDER OFFICE","LIVING QUARTERS","CHARGING DOCK","MESS HALL","WATER PURIFICATION","NUTRIENT RECYCLER","OBSERVATORY","COMMUNICATION DEPT","SURFACE DOME","BACKUP GENERATOR"]
    roomDescriptions=["As the doors slide shut behind you, you see a poorly-lit panel of buttons labeled by the rooms that they send the elevator to. This base has 4 levels.",
                  "Unlike your recent visit here, it is completely isolated and plunged in darkness. Gas sits in the room like a brewing storm.",
                  "Harsh fluorescent lights shine through the entire room, which is large enough to fit three cruisers. It is a grated metal spaceport-like structure, which used to be filled with ships of all sorts. With the exception of a few old freighters, it is empty now.",
                  "It is a dark, cubical room fitted with crude steel benches and illuminated by a few flickering lightbulbs. To your right, you see racks of standard-issue armor, both gently-used and battle-scared, on the wall. To your left, you see racks of a variety of weapons used by soldiers such as yourself to enforce the regulation of the Tauron Passage.",
                  "It is a space foreign to you, as enlisted personnel are usually not allowed here. To the right are the commander's bunk and facilities, which look expensive. What petty corruption. In front of you is the commander's desk. On the wall, you see that there are a variety of switches that control parts of the base. One of them can turn the backup generator on and off, activating the elevator.",
                  "You see row after row of canvas bunks and steel footlockers lining the room. Without the tomfoolery usually occurring here, it seems strangely creepy and lonely. Unfortunately, you realize that the gas masks in the living quarters have been crushed by a fallen steel beam. Coughing, you reevaluate your options.",
                  "The room is filled with dimly glowing plasma batteries. In the center, there are a line of charging stations to charge your survival pack. To charge your pack, go to inventory and use the pack.",
                  "This large room is lined front to back with crude metal tables. Located on one wall is a window and door that leads to the kitchen, an small industrial-grade room that produces all of the Station's rations. In the middle of the mess hall is the chief engineer's dead body. Next to it, you see a crack in the floor.",
                  "This room is packed with columns of reverse osmosis pumps and iodine dispensers that makes water used by the station safe to drink and use. ",
                  "This metallic room contains many large processing machines with tubes that expand to the Mess Hall.",
                  "A bubble of clear glass, it contains the machinery required to chart distant star systems and create galaxy maps. Maybe you should look outside",
                  "A rather small room, it contains a wide control panel of computers and a large glass window that gives a grand view of the surface dome, the antenna, and the ominous star system. You will have to access the computers.",
                  "A wall of thick reinforced steel and glass, it shields the base against outside attacks and also provides photovoltaic energy for the base through light absorption. You observe giant cracks over the top where state-of-the-art inertia beams hit. It is leaking atmospheric haze. Against one of the walls sits the controller computer for the crane outside. Access the controller to use the crane to fix the antenna.",
                  "This smaller room houses the station's backup generator, a large, rectangular metal box with tons of wiring and dozens of circuit breakers. Next to the generator you see the commander's dead body."]
    #For each room, there is a list of connected rooms
    connectedRooms=[[12,7,5,1],[2,4,0],[3,1],[2],[1],[6,0],[5,13],[0,8],[9,7],[11,8],[12],[12,9],[0,10,11],[6]]
    #For some rooms, the room starts as being locked but can be opened by the user at some point
    locked=[True,False,False,False,True,False,False,False,False,False,False,True,False,False]

    roomList=[]
    for l in range(len(roomNames)):
        roomList.append(location(l,roomNames[l],connectedRooms[l],roomDescriptions[l],locked[l]))

    #ITEM SETUP: creates all the item objects
    itemNames=["SURVIVAL PACK","MAP","EXPLOSIVES","CASE","MESSAGING COORDINATES"]
    itemDescriptions=["",
                      "You see a map on the table.",
                      "In the corner you notice a pile of explosives.",
                      "On the desk, you see the commander's case.",
                      ""]
    descriptionWhenObtained=["",
                             "You take the map.",
                             "You obtain the explosives. Maybe these will help you break into another room.",
                             "You get the case. However, it is locked and can only be opened by the commander's fingerprint. You will have to find the dead commander's body.",
                             "You opened the case and got the messaging coordinates."]
    #The locations that the items start in
    originalLocations=[None,1,3,4,None]

    #The locations that the items are supposed to be used in
    useLocations=[6,None,1,13,None]
    itemFunctions=[chargePack,openMap,explosive,openCommanderBox,readMessagingCoordinates]

    itemList=[]
    for l in range(len(itemNames)):
        itemList.append(item(l,itemNames[l],originalLocations[l],useLocations[l],itemFunctions[l],itemDescriptions[l],descriptionWhenObtained[l]))

    #Creates the variable for the code to enter the communication department
    roomList[11].code=[]

    #Creates the codes to control the crane
    roomList[10].fixes=[]
    roomList[10].nextFix=[]
    craneCommands=["CLEAN UP DEBRIS","BUILD ANTENNA SUPPORT","PICK UP MATERIALS","DISMANTLE PARTS"]
    for thing in range(3):
        roomList[10].fixes.append([random.choice(string.ascii_uppercase)+str(random.randint(0,9)),random.choice(craneCommands),False])

    #Immediately puts the pack in the user's inventory at the beginning of the game
    user.inventory.append(itemList[0])
    itemList[0].pickedUp=True

    #Return all the objects created in setup
    return {"Room List":roomList,"Item List":itemList,"User":user}

#ITEM FUNCTIONS, functions that run when an item is used
#Some item functions have to take more arguments than they need because they all run from the useItem function in the item class which always plugs in roomList and user as two arguments
def chargePack(user,unnecessaryArg1,unnecessaryArg2):
    user.energy=100
    print("The pack is now fully charged.")
def openMap(unnecessaryArg1,unnecessaryArg2,unnecessaryArg3):
    print("")
    print("4F     -   Observatory    ----    Surface Dome   ----  Communication Department")
    print("       E                                                           |           ")
    print("       L                                                           |           ")
    print("3F     E   Mess Hall   ----    Water Purification  ----    Nutrient Recycler  ")
    print("       V                                                                    ")
    print("       A                                                                   ")
    print("2F     T   Living quarters ---- Charging dock ---- Backup Generator        ")
    print("       O                                                                   ")
    print("       R                                                                    ")
    print("1F     -   Briefing chambers   ----    Launch Dock                         ")
    print("                   |                        |                             ")
    print("           Commander Office              Armoury                         ")
    print("")
    print("Your goal is to reach the communication department to send a message.")
    print("To do this, you will have to get messaging coordinates, fix the antenna, and find the code to enter the communication department.")
def explosive(user,roomList,itemList):
    roomList[4].locked=False
    print("You blew up the door to the commander office. You can now enter.")
    user.inventory.remove(itemList[2])
def openCommanderBox(user,unnecessaryArg,itemList):
    print("You have successfully opened the case. Inside are the messaging coordinates you will need to send a backup request.")
    #Sets the messaging coordinates
    user.inventory.append(itemList[4])
    user.inventory.remove(itemList[3])
def readMessagingCoordinates(unnecessaryArg1,unnecessaryArg2,itemList):
    print("This confidential paper contains the coordinates required in order to send a message to the government.")

#The following functions are special functions that control certain features in different rooms of the base (e.g. the crane controller)
def commanderOfficeSwitch(roomList):
    print("You flipped the switch...")
    time.sleep(0.5)
    if roomList[0].locked:
        print("The backup generator is now functional.")
    else:
        print("The backup generator is now shut down.")
    roomList[0].locked=not roomList[0].locked
def messHallCrack(user,roomList):
    print("You look into the crack. It seems that the device showing the password to enter the communication dept is in it. You can't reach the device.")
    print("This device will be useful as you need to get into the communication dept to send a call for backup to the government.")
    print("However, the code on the device seems to change in the time it takes for you move through a number of rooms.")
    print("Currently, the code is:")
    print(roomList[11].code)
    movesBeforeChange=str(3-user.numOfRoomChanges%3)
    print("The code will change in "+movesBeforeChange+" moves")
def observatoryWindow(roomList):
    antennaFixed=True
    print("You look out the window. The antenna is badly damaged. You will have to repair it before trying to communicate with the government.")
    for fix in roomList[10].fixes:
        if not fix[2]:
            antennaFixed=False
            roomList[10].nextFix=fix
    if antennaFixed:
        print("You have successfully repaired the antenna. It is now fully functional.")
        return

    print("The next location of the antenna that needs fixing is "+roomList[10].nextFix[0])
    print("Command for the controller: "+roomList[10].nextFix[1])
def controller(roomList):
    if not roomList[10].visitedBefore:
        print("Maybe you should go to the observatory to check the antenna before trying to fix it.")
        return
    print("Type the location that the crane needs to go to:")
    location=input("> ")
    print("Type the command to tell the crane what to do at this location:")
    craneCommand=input("> ")

    if location==(roomList[10].nextFix[0]) and craneCommand.upper()==(roomList[10].nextFix[1]):
        roomList[10].nextFix[2]=True
        print("You have successfully fixed this part of the antenna. Go back to the observatory to check the repairs.")
    else:
        print("Looks like nothing happened. Maybe you typed the command or location wrong. Go to the observatory to check the status of the antenna.")
def computer(user,roomList):
    print("This computer is used to send messages to the government. Below are the requirements to send a message:")
    antennaFixed=True
    messagingCoordinatesObtained=False

    #Checks if the messaging coordinates have been obtained and if the antenna has been fixed
    for item in user.inventory:
        if item.name=="MESSAGING COORDINATES":
            messagingCoordinatesObtained=True
            break
    for fix in roomList[10].fixes:
        if not fix[2]:
            antennaFixed=False

    print("ANTENNA FIXED          "+str(antennaFixed))
    print("COORDINATES OBTAINED   "+str(messagingCoordinatesObtained))
    if antennaFixed and messagingCoordinatesObtained:
        print("Type the message you would like to send to the government to request backup.")
        input("> ")
        print("")
        print("Message sent successfully")
        input("Press enter...")
        return True
    else:
        print("One or more of the requirements is not done. Go finish it now.")
        return False
def elevatorProgram(roomList,itemList,user):
    print("---------------------------------------------------------------------------------")
    print(roomList[0].roomDescription)
    #For each floor, this dictionary contains the corresponding room you would enter if you exited the elevator on that floor
    floorToRoom={1:1,2:5,3:7,4:12}

    while True:
        print("What floor would you like to go to? Type in a number")
        try:
            choice=int(input("> "))
        except:
            print("You did not type a floor number.")
            elevatorProgram(roomList,itemList,user)
        if choice>=1 and choice<=4:
            user.floor=choice
            print("You are now on floor "+str(choice))
            print("Would you like to exit the elevator? The room you would be in would be the "+roomList[floorToRoom[user.floor]].roomName+".")
            while True:
                choice=input("> ")
                if choice.upper()=="YES":
                    user.changeLoc(floorToRoom[user.floor],roomList)
                    roomProgram(roomList,itemList,user)
                elif choice.upper()=="NO":
                    elevatorProgram(roomList,itemList,user)
                else:
                    print("INVALID INPUT")
        else:
            print("INVALID FLOOR")

#The standard function that controls what happens in a room
#Makes observations about the current room the user is in
def observeRoom(room,roomList,itemList,includeDescription):
    print("You are in the "+room.roomName)
    #Only prints the basic description of the room if the user has not visited the room before
    if includeDescription:
        print(room.roomDescription)
        room.visitedBefore=True
    for item in itemList:
        if item.originalLocation==room.locationNumber and not item.pickedUp:
            print(item.description)
    print("")
    print("From this room you can go to:")
    for connectedRoom in room.connectedRooms:
        print("\t"+roomList[connectedRoom].roomName)
def roomProgram(roomList,itemList,user):
    print("---------------------------------------------------------------------------------")
    #Saves the object for the current room for easy access
    currentRoom=roomList[user.location]
    print("")

    #Prints the description of the room
    observeRoom(currentRoom,roomList,itemList,not currentRoom.visitedBefore)

    itemsInRoom=[]
    roomItemIDNumbers=[]
    connectedRoomNames=[]
    connectedRoomNumbers=[]

    #Sets up the variables defined above
    for item in itemList:
        if item.originalLocation==user.location:
            itemsInRoom.append(item.name)
            roomItemIDNumbers.append(item.ID)
    for connectedRoom in currentRoom.connectedRooms:
        connectedRoomNames.append(roomList[connectedRoom].roomName)
        connectedRoomNumbers.append(roomList[connectedRoom].locationNumber)

    #Creates the list of options for the user
    options=connectedRoomNames+itemsInRoom
    if user.location==4:
        options.append("SWITCH")
    if user.location==7:
        options.append("CRACK")
    if user.location==10:
        options.append("OUTSIDE")
    if user.location==11:
        options.append("COMPUTER")
    if user.location==12:
        options.append("CONTROL")
    options.append("LOOK")
    options.append("INVENTORY")
    options.append("STATUS")
    options.append("HELP")

    #If the any of the options are part of the string the user types in, the corresponding code is run
    while True:
        print("")
        print("What would you like to do?")
        choice=userOption(options,"Invalid command. Is your command specific enough?")

        #If the user input contains the name of a connected room, the user will move to that room as long as that room isn't locked
        if choice in connectedRoomNames:
            room=roomList[connectedRoomNumbers[connectedRoomNames.index(choice)]]
            if not room.locked:
                user.changeLoc(room.locationNumber,roomList)
                if user.location==0:
                    elevatorProgram(roomList,itemList,user)
                else:
                    roomProgram(roomList,itemList,user)
            elif room.locationNumber==0:
                print("The elevator doesn't have power because the backup generator is not working. You could potentially turn the power on through the commander office.")
            elif room.locationNumber==4:
                print("The commander office is locked. Maybe you should find a way to break down the door")

            #Checks if the user inputted the correct code for the communication department
            elif room.locationNumber==11:
                print("TYPE IN THE THREE NUMBER CODE")
                if input("> ")==roomList[11].code:
                    print("Access granted. The communication department is now unlocked. When you leave again, the room will auto lock again.")
                    roomList[11].locked=False
                else:
                    print("Code input incorrect. Access denied.")

        #If the user inputs the name of an item that is located in the room, the user will "pick up" that item
        elif choice in itemsInRoom:
            item=itemList[roomItemIDNumbers[itemsInRoom.index(choice)]]
            if not item.pickedUp:
                user.inventory.append(item)
                item.pickedUp=True
                print(item.descriptionWhenObtained)
            else:
                print("You already got that item.")

        #If the user inputs anything else that is part of the valid options, the corresponding code is run
        elif choice=="LOOK":
            observeRoom(currentRoom,roomList,itemList,True)
            time.sleep(1)
        elif choice=="INVENTORY":
            inventory(roomList,itemList,user)
        elif choice=="STATUS":
            user.printStatusReport()
            time.sleep(1)
        elif choice=="SWITCH":
            commanderOfficeSwitch(roomList)
        elif choice=="CRACK":
            messHallCrack(user,roomList)
        elif choice=="OUTSIDE":
            observatoryWindow(roomList)
        elif choice=="CONTROL":
            controller(roomList)
        elif choice=="COMPUTER":
            if computer(user,roomList):
                end()
        elif choice=="HELP":
            howToPlay()

def printTitle():
    print("DO NOT TYPE WHILE TEXT IS PRINTING AT ANY POINT.")
    time.sleep(1)
    print(" _    _      _                            _          _____                       ______")
    print("| |  | |    | |                          | |        /  ___|                      | ___ \              ")
    print("| |  | | ___| | ___ ___  _ __ ___   ___  | |_ ___   \ `--. _ __   __ _  ___ ___  | |_/ /__ _  ___ ___ ")
    print("| |/\| |/ _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \   `--. \ '_ \ / _` |/ __/ _ \ |    // _` |/ __/ _ \\")
    print("\  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | /\__/ / |_) | (_| | (_|  __/ | |\ \ (_| | (_|  __/")
    print(" \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  \____/| .__/ \__,_|\___\___| \_| \_\__,_|\___\___|")
    print("                                                          | |")
    print("By Alan Wang, Justin Wang, and Bryan Lindsay              |_|")
    print("")
def backStory():
    print("---------------------------------------------------------------------------------")
    print("")
    print("You are a pilot flying fighters for the Intersystem Government. Currently you are stationed on the planet X2-4 alpha in the Tauron Passage, the only way to get through the astroid belt surrounding the hydrogen and rare earth mineral rich interior of the star system. The purpose of your base is to regulate trade in and out of this vital area. SpaceEx-odus wants to seize control and monopolize the export of these minerals.")
    input("Press enter...")
    print("")
    print("You begin your journey in the Briefing Room, where Supreme Commander Vulcan is administering daily patrol duties for the day (you hope that you're not tasked with cleaning the head again). Then, without warning, an alarm sounds from the intercom, warning of the unexpected presence of SpaceEx-odus cruisers in pursuit of forcefully bypassing the Tauron Passage for access to the material-rich inner star system. Taking a look at the camera and scanner, you see SpaceEx-odus cruisers approaching the base. You and the other pilots scramble to intercept - usually drones would be used for this but ship inspection requires actual personnel.")
    input("Press enter...")
    print("")
def howToPlay():
    print("---------------------------------------------------------------------------------")
    print("\033[4mHOW TO PLAY\033[0m")
    print("In order to perform any action, type it into the console (i.e. 'leave room','pick up the map','open the box')")
    print("When you would like to use an item, open your inventory and type the name of the item you would like to use.")
    print("When you would like to look at the room you're in and make observations, type 'look'.")
    print("If something doesn't work, make sure you spelled it correctly. Type 'help' if you want to see these tips at any point.")
    print("")
    print("Note: Your pack requires energy. Each time you move into another room, the percentage will go down by 10%. If you run out of energy at any point, you die. Make sure to check your energy often by typing 'status'. In order to charge your pack, go to the charging dock.")

    time.sleep(2)
def intro():
    print("---------------------------------------------------------------------------------")
    print("Your squadron clashes head on with the enemy forces. Soon, you realize that you are no match for SpaceEx-odus' overwhelming firepower. As you look around, you realize all of the other pilots have been downed. You are now alone - however some pilots have damaged the SpaceEx-odus flagship, honoring the late Elong Musk. They temporarily retreat to a safe distance.")
    input("Press enter...")
    print("")
    print("Being low on fuel, you return to base, only to find that the planet's highly toxic atmosphere has leaked into the base and killed the other military personnel. Since your are the only one alive, you realize that you must contact the government and alert them about the SpaceEx-odus attack so that they can send backup.")
    print("")
    print("The airlock closes behind you as your lungs start reacting to the chemicals. Your pack will provide air and regulate your blood glucose, but will not filter toxins out of the air. You slice off a sleeve of your shirt, making a makeshift air filter to try to protect yourself as you make your way to the gas masks in the living quarters.")
    print("")
    print("However, before doing that, you realize that you should first go to the briefing chambers to obtain a floor plan to help you navigate the base...")
    time.sleep(2)
    print("")

#Run when the user completes the game
def end():
    print("Just as you hit send, you burst into a fit of coughing from the toxic air.")
    print("As you slowly lose consciousness, you see the government battleships warping in firing at the attacking SpaceEx-odus ships.")
    time.sleep(2)
    print("---------------------------------------------------------------------------------")
    print("Congratulations! You have finished the game. To play again, type play again. To exit, type exit.")
    if input("> ").upper()=="PLAY AGAIN":
        main()
    else:
        veryNumber=0
        while True:
            string="Are you "
            for very in range(veryNumber):
                string=string+"very "
            veryNumber+=1
            string=string+"sure?"
            print(string)
            if input("> ").upper()!="YES":
                main()


#Opens the user inventory
def inventory(roomList,itemList,user):
    print("\033[4mInventory\033[0m")
    itemNames=[]
    for item in itemList:
        itemNames.append(item.name)

    options=[]
    for item in user.inventory:
        print("-"+item.name)
        options.append(item.name)
    options.append("CLOSE")
    print("")
    print(("What item would you like to use? Type close to close the inventory"))
    choice=userOption(options,"Invalid item choice")
    if choice=="CLOSE":
        return
    for item in user.inventory:
        if choice==item.name:
            item.useItem(user,roomList,itemList)
            break
    time.sleep(1)


#Gives the user the option to start the game, sets up the game
def newGame():
    print("Type start to start a new game")
    print("")
    while True:
        answer=input("> ").upper()
        if answer=="START":
            print("LOADING...")
            time.sleep(3)
            print("\n"*100)
            gameInfoDict=setup()
            print("What is your name?")
            gameInfoDict["User"].name=input("> ")
            if "BARRON" in gameInfoDict["User"].name.upper() or "TIM" in gameInfoDict["User"].name.upper():
                easterEgg()
                return
            while True:
                print("Do you want to skip the backstory and how to play?")
                choice=input("> ").upper()
                if choice=="NO":
                    backStory()
                    intro()
                    howToPlay()
                    input("Press enter...")
                    break
                elif choice=="YES":
                    print("You have skipped the tutorial and the backstory. You are the only remaining survivor after the battle with SpaceEx-odus. You are back at the base where you will have to send a message to the government asking for backup.")
                    break
            gameInfoDict["User"].location=2
            roomProgram(gameInfoDict["Room List"],gameInfoDict["Item List"],gameInfoDict["User"])

#Prints a fake error to the console if the user's name contains tim or barron
def easterEgg():
    print("Traceback (most recent call last):")
    print("File \"/bin/pythonanywhere_runner.py\", line 22, in _pa_run")
    print("File \"/home/WWWWWW/projects/adventureGame.py\", line 105")
    print("UserNameError: IQ TOO HIGH :D")
    print("")
    time.sleep(2)
    main()

#The main function is run to start the entire script
def main():
    printTitle()
    newGame()



main()
