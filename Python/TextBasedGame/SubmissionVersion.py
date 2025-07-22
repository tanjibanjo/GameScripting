# Lane Pollock
# Game Scripting
# Text-Based Adventure
# note: Each section have their own original source code files -
# CharacterClass.py and Utility file have been combined in this version of code so that there is only one file to submit

####################
#This text based adventure takes you, a traveler, through a dangerous and war-torn country as you fight (or not) your way through encounters on your journey.
####################

#IMPORTS
import random

####################
#CHARACTER AND ENEMY CLASSES  -
####################
class Character:
    def __init__(self, name, health, attack, dex, type):
        self.name = name
        self.health = health
        self.attack = attack
        self.dex = dex
        self.type = type

class Enemy:
    def __init__(self, name, health, attack, used, score):
        self.name = name
        self.health = health
        self.attack = attack
        self.used = used
        self.score = score

####################
#UTILITY FUNCTIONS FOR ENOUNTERS AND COMBAT SIM
####################
#function prints game over
def gameOver(levelsPassed):
    print("-JOURNEY OVER-")
    print(f"Score: {levelsPassed}\n") 


#function takes list and loads 9 enemies
def loadEnemies(enemyList):
    #enemies list
    wolf = Enemy("Wolf", 50, 10, False, 125)
    giantSpider = Enemy("Giant Spider", 90, 30, False, 250)
    unicorn = Enemy("Unicorn", 1, -20, False, 25) #this one returns health
    demon = Enemy("Demon", 65, 25, False, 140)
    orc = Enemy("Orc", 40, 20, False, 100)
    orcLeader = Enemy("Orc Leader", 80, 40, False, 175)
    goblin = Enemy("Goblin", 35, 15, False, 75)
    swordsman = Enemy("Swordsman", 50, 25, False, 100)
    greedyVillager = Enemy("Greedy Villager", 40, 20, 0, 75)

    #add all the enemies to the list - could initialize them in the extend statement, but it's not pretty
    #extend allows the list to not be resized every addition
    enemyList.extend([wolf, giantSpider, unicorn, demon, orc, orcLeader, goblin, swordsman, greedyVillager])

#function takes the list of characters and loads the options for player character
def loadCharacters(characterList):
    #characters to be added
    mage = Character("Mage", 50, "20-60", 30, "Mage")
    rogue = Character("Rogue", 65, "0-25 x2", 75, "Rogue")
    warrior = Character("Warrior", 80, "33-44", 45, "Warrior")

    #add characters
    characterList.extend([mage, rogue, warrior])

#function prints the welcome message and background to the story - returns true if player goes to the house, false if they camp
def introSequence():
    print("You walk along the path, wary of monsters and of mortals known to ambush in the area.\nAlong comes a fork in the road. Left or Right? That is the question.")
    choice = input("[enter direction]: ")
    #sorry, either way you get to the village 
    print(f"You go {choice}. As you walk, the day dissapears to reveal dark. You think about shelter, but in the distance you see a light. Do you approach?")

    while(choice != "y" and choice != "n"):
        choice = input("[y/n] ")
    
    match(choice):
        case "y":
            print("You get closer. Through the trees you can see someone in their home. It is a small village in the countryside that has been damaged by monsters. \nThe people are cautious, but maybe they'll help you. You walk up and gently knock on the door.")
            return True
        case "n":
            print("You spot a clearing to the left and decide it's a good enough spot. You camp off to the side of the clearing and fall asleep.")
            return False

#function prompts player for information on making their own character
def getPlayerCharacter(playerCharacter, characterList):
    print()
    #first get name
    name = input("What do they call you, stranger? ")
    choice = -1 #set playerChoice up

    #validate
    print("%s, huh? Is that the right way to pronounce it?\n[1] That's right.\n[2] Not quite. (re-enter name)" % name)
    
    try:
        #get user validation
        while(choice < 1 or choice > 2):
            if(choice != -1): #not first time running
                print("Enter a valid choice...")
                choice = int(input())
            else:
                choice = int(input())
    except Exception as e:
        print("An error occured.")
        choice = 2 #send player into loop below

    while(choice != -1):
        #switch on choice
        match(choice):
            case 1: #name is good, advance
                print("Well, alright. Don't think I've seen you around here before. What do you do, %s?" % name)
                choice = -1 #break while
            case 2: #re enter name
                name = input("What do they call you, stranger? ")
                choice = -1
                #repeat validation
                print("%s, huh? Is that the right way to pronounce it?\n[1] That's right.\n[2] Not quite. (re-enter name)" % name)
    
                try:
                    #get user validation
                    while(choice < 1 or choice > 2):
                        if(choice != -1): #not first time running
                            print("Enter a valid choice...")
                            choice = int(input())
                        else:
                            choice = int(input())
                except Exception as e: #note: this is really just to handle if they input a letter
                    print("An error occured.")
                    choice = 2 #send back through loop 
            case _: #default
                print("Not a choice...")

    #once name is good, assign to player character
    playerCharacter.name = name

    #now, get player class decision and load the rest of the stats to the player character
    #print the options
    for character in characterList:
        print(character.name + "\n\tHealth: %s" % character.health + "\n\tAttack: " + character.attack + "\n\tDexterity: %s" % character.dex)

    try:
        #get player choice (should be reset to -1)
        while(choice < 1 or choice > 3):
            if(choice != -1):
                print("Enter a valid choice...")
            choice = int(input("[1-3]: "))
    except Exception as e:
        print("An error occured.")
        return

    #after valid choice, load the stats
    match(choice):
        case 1: #mage
            playerCharacter.type = characterList[0].name
            playerCharacter.health = characterList[0].health
            playerCharacter.attack = characterList[0].attack
            playerCharacter.dex = characterList[0].dex
            choice = -1 #reset
        case 2: #rogue
            playerCharacter.type = characterList[1].name
            playerCharacter.health = characterList[1].health
            playerCharacter.attack = characterList[1].attack
            playerCharacter.dex = characterList[1].dex
            choice = -1
        case 3: #warrior
            playerCharacter.type = characterList[2].name
            playerCharacter.health = characterList[2].health
            playerCharacter.attack = characterList[2].attack
            playerCharacter.dex = characterList[2].dex
            choice = -1
        case _:
            print("Huh?")
            
    #print info and start adventure
    print("\n%s," % name + " a %s. Good timing too, I could really use your help." % playerCharacter.type)

#function for 'wait' ability for player
def wait(playerCharacter):
    if(playerCharacter.name == "You"):
        print("You wait.")
    else:
        print(f"{playerCharacter.name} waits.")


#function for 'flee' ability for player - returns true or false based on success of flee
def flee(playerCharacter):
    #generate a random number between 0-100 and set
    randNum = random.randint(0, 100)

    #do a dex check
    if(randNum >= playerCharacter.dex): #if dex is 80, this represents 80% success rate
        print("Flee unsuccessful.")
        return False
    else:
        print("Flee successful.")
        return True
    
#function is for attack against player, takes enemy attack and applies it
def attackPlayer(playerCharacter, enemy):
    if(enemy.name != "Unicorn"): #skip if unicorn
        #generate enemy attack within a range of possible numbers
        #if enemy attack is 10, the range is 7 - 11/ 20 is 12 - 21 / 30 is 17-31
        enemyAttack = 1 + (enemy.attack / 2) + random.randint(1, int(enemy.attack / 2)) 

        #apply attack
        playerCharacter.health -= enemy.attack
        if(playerCharacter.health < 0):
            playerCharacter.health = 0

        #print update
        print(f"Enemy attacks for {enemyAttack} damage. Player HP at {playerCharacter.health}.")
    elif(enemy.name == "Unicorn"):
        #apply health boost
        playerCharacter.health -= enemy.attack

        #update
        print("The unicorn slowly approaches. As it nears, you can see the reflections in its eyes and its horn glows.\nThe next thing you know, you're waking up on the floor feeling surprisingly rested.")

        #decrement the unicorn health to 0 to end the encounter
        enemy.health -= 1

#this function is for player attacking the enemy
def attackEnemy(playerCharacter, enemy):
    #depending on which character the player is, generate an attack in that range.
    if(playerCharacter.type == "Mage"):
        playerAttack = random.randint(20, 60) #20-60
    elif(playerCharacter.type == "Rogue"):
        playerAttack = (random.randint(0,25) + random.randint(0,25)) #0-25 x2
    else: #warrior is 35-50
        playerAttack = random.randint(33, 44)
    
    #apply attack
    enemy.health -= playerAttack
    if(enemy.health <0):
        enemy.health = 0

    #update
    print(f"Player attacks for {playerAttack} damage. Enemy HP at {enemy.health}")

#function takes the enemy list and generates a random index to choose for the combat encounter
#RETURNS INDEX
def getEnemy(enemyList):
    #get random index
    index = random.randint(0, 8)
    
    while(enemyList[index].used == True): #if the enemy has been used already, get new index
        index = random.randint(0,8)

    #return the index so the enemy can be set in the main
    return index

#function simulates a combat encounter - takes one enemy and the player character
def combatEncounter(playerCharacter, enemy):
    #variables
    actionChoice = -1 
    fleeAttempt = False #represent success of flee
    if(enemy.name != "Unicorn"):
        print(f"{enemy.name} approaches...\nHP: {enemy.health}\nAttack: {enemy.attack}")
    elif(enemy.name == "Unicorn"):
        print(f"{enemy.name} approaches...")

    #player always goes first in this demo
    while(playerCharacter.health > 0 and enemy.health > 0 and fleeAttempt != True): #both are alive and not fled

        #get choice
        print("What will you do?")
        try:
            actionChoice = int(input("[1] Attack\n[2] Flee\n[3] Wait\n"))
        except Exception as e:
            actionChoice = 4

        #match on choice
        match(actionChoice):
            case 1:
                attackEnemy(playerCharacter, enemy)
            case 2:
                if(flee(playerCharacter) == True):
                    fleeAttempt = True
            case 3:
                wait(playerCharacter)
            case _:
                print("Turn was lost.")
        
        #enemy turn
        if(fleeAttempt != True and enemy.health > 0):
            attackPlayer(playerCharacter, enemy)

    #return results
    if(enemy.health <= 0):
        print(f"{enemy.name} defeated.\nRemaining HP: {playerCharacter.health}\n")
        enemy.used = True
        return True
    elif(fleeAttempt == True):
        print(f"Player got away.\nRemaining HP: {playerCharacter.health}\n")
        enemy.used = True
        return True
    elif(playerCharacter.health <= 0):
        print(f"{playerCharacter.name} was lost.\n")
        return False


#function contains the villagePerson encounter and its logic
def villagePersonEncounter():
    print()
    print("This land is beyond saving. There's tell that a paradise lays beyond the nothing, but it's too dangerous.\nY-you can make it though. The orb- please return it to me.")
    try:
        choice = int(input("[1] If you can shelter me for the evening, I'll go look.\n[2] What? I just met you, you're crazy.\n"))
    except Exception as e:
        choice = int(input())
    
    if(choice == 1):
        print("The villager sticks out their hand and points you to a small shed behind the house. You enter it, and make shelter for the night.")
        print("There's woodworkings and notes -designs for caskets- scattered about. Business must be booming.\nYou think to yourself, what is really out there?")
        return True
    if(choice == 2):
        print("You deny the villager. As you turn to move on, you hear a scuffle. Turning around, you see the villager with a knife in their hand.")
        return False
    
#function contains the innkeeper encounter
def innkeeperEncounter(playerCharacter):
    choice = input("[]")

    print("\nYou smell something funny. It's kind of weird, but you're so hungry you follow it anyway.")
    print("Through the forest, you come across a building. It's out of place. There's music coming from within. Enter?")
    while(choice != "y" and choice != "n"):
        choice = input("[y/n] ")

    #impplement choice
    if(choice == "n"):
        print("You walk along, deciding it's not worth the trouble.")
        return False
    elif(choice == "y"):
        print("You enter the inn, or whatever it is. There's an inkeeper inside with a big smile on their face.")
        print("[innkeeper] I've been waiting for you. Now I can finally take a breather. Just answer me this: ")
        print("Who makes it has no need of it. Who buys it has no use for it. Who uses it can neither see nor feel it. What is it?")

        playerGuess = input("[enter answer]: ")

        if(playerGuess == "coffin" or playerGuess == "Coffin" or playerGuess == "a coffin" or playerGuess == "casket" or playerGuess == "Casket" or playerGuess == "a casket"):
            print("I knew it was you. Here's the orb. [hands over orb]")
            return True
        else:
            print("[the innkeeper laughs] Absolutely. Here's a drink, cheers to new company.")
            print("\nEverything begins to go fuzzy...")

            pause = input("[]")

            print("You wake up in the back of the house in a pile of mud and debris. You weren't supposed to make it, but you did.")
            
            #player loses health from this
            playerCharacter.health -= 10
            print(f"Player health at {playerCharacter.health}")
            return False

#function handles ending options
def orbDecisions(playerCharacter, levelsPassed, hasOrb, questTaken):
    if(hasOrb == True and questTaken == True):
        choice = input("[]")
        print("Return orb to the villager?")

        while(choice != "y" and choice != "n"):
            choice = input("[y/n] ")
        
        if(choice == "y"):
            print("You return to the villager. When you hand them the orb, you notice a glow eminating from the ground all around. The souls of the town are at peace.")
            pause = input("[]")
            print("When you turn back around, the villager is gone.\nAll that remains is a map. You pick it up, and smirk.")
            print("[dexterity increased by 10]")
            playerCharacter.dex += 10
            return True
        elif(choice == "n"):
            print("You focus all your energy on the orb. It glows, and you feel powerful. A slight grin appears on your face as you walk away, onward.")
            print("[health raised by 15]") 
            playerCharacter.health += 15
            return False
    elif(hasOrb == True and questTaken == False):
        choice = input("[]")
        print("Use orb?")
        while(choice != "y" and choice != "n"):
            choice = input("[y/n] ")
        
        if(choice == "y"):
            print("You focus all your energy on the orb. It glows, and you feel powerful. A slight grin appears on your face as you walk away, onward.")
            print("[health raised by 15]") 
            playerCharacter.health += 15
            return False
        elif(choice == "n"):
            print("There's something supernatural about this orb. You decide no one should have the power it holds, so you bury it where it cannot be found.\nBy the tree where you bury it, you notice a piece of paper.")
            pause = input("[]")
            print("You pick it up. It is a map. You look on into the distance in anticipation of the journey ahead.")
            print("[dexterity increased by 10]")
            playerCharacter.dex += 10
            return True
        
    else:
        pause = input("[]")
        print("The journey to Paradise continues...but you know you're on the right path...maybe.")


def endGame(hasMap):
    if(hasMap == True):
        #prompt for continuing journey
        print("Do you follow the map?")
        choice = input("[y/n] ")
        #validate
        while(choice != "y" and choice != "n"):
            choice = input("[y/n] ")
        #handle y/n
        if(choice == "n"):
            return False
        else:
            print("You continue.\n")
            return True
    else: #no map means they have orb
        #prompt for continuing journey
        print("Do you continue onward?")

        choice = input("[y/n] ")
        #validate
        while(choice != "y" and choice != "n"):
            choice = input("[y/n] ")

        if(choice == "n"):
            return False
        else:
            print("You go on, and it feels like you just know the right way. Is this the orb?\n")



#__MAIN__
def main():
    #local variables
    enemyList = []
    characterList = []
    playerCharacter = Character("You", 50, 30, 85, "class") #default values
    currentEnemy = Enemy("name", 1, 1, False, 0) #default values - this will be reset with values every encounter
    levelsPassed = 0.0
    count = 0 #keeps track of how many enemies you have faced
    questTaken = False
    hasOrb = False
    hasMap = False

    #start the game by loading enemies and characters
    loadEnemies(enemyList)
    loadCharacters(characterList)

    print("\n[] When you see open brackets, press enter to continue.")
    pause = input("[]")

    print("")

    #INTRO SEQUENCE
    encounterResult = introSequence() #stores the true or false in a variable

    if(encounterResult == True): #at door of villager
        pause = input("[]")
        print("The door opens, but just barely. There's little light but you hear a voice from within.")
        #get player character
        getPlayerCharacter(playerCharacter, characterList)
    else: #camped
        pause = input("[]")
        print("You hear a noise, and jump up to see what it is. What a drag.\n")

        

        print()
        #get enemy from list and assign
        currentEnemy = enemyList[getEnemy(enemyList)]
        #enemy cannot be villager
        while(currentEnemy.name == "Greedy Villager" or currentEnemy.name == "Unicorn"):
            #get enemy from list and assign
            currentEnemy = enemyList[getEnemy(enemyList)]

        #combat encounter
        encounterResult = combatEncounter(playerCharacter, currentEnemy)
        count += 1

        #if survived, go to the village and get character all the same
        if(encounterResult == True):
            levelsPassed += currentEnemy.score
            print("You made it, and decide to go to the village because it sucks out here. Walking up to the house, the door creaks open and you hear a voice.")
            pause = input("[]")
            #get player character
            getPlayerCharacter(playerCharacter, characterList)
        else: #dead
            gameOver(levelsPassed)
            return

    pause = input("[]")

    #next encounter is the village person encounter
    encounterResult = villagePersonEncounter()
    if (encounterResult == False): #not helping villager
        currentEnemy = enemyList[8] #greedy villager
        print("'Give me your sh*t, then.'")
        encounterResult = combatEncounter(playerCharacter, currentEnemy)

        if(encounterResult == True):
            levelsPassed += currentEnemy.score
            print("You rummage around the villager's house as you take shelter. Strange notes - plans of coffins- and bones lay around.\nYou think maybe it was a good thing you didn't help them.")
            count += 1

        else:
            gameOver(levelsPassed)
            return
    else: #helping the villager
        questTaken = True

    pause = input("[]")

    #transition to the next encounter
    print("\nThe next day, there's no one around. No villagers. You decide to carry on, into what the villager called 'the nothing'. Just looks like a forest to you.")

    #journey begins, combat encounters
    print("You journey on through the forest. There really is nothing but trees here, until you hear something in the distance. You venture closer...")

    pause = input("[]")

    #load new enemy
    currentEnemy = enemyList[getEnemy(enemyList)]
    #combat
    encounterResult = combatEncounter(playerCharacter, currentEnemy)
    
    if(encounterResult == True):
        levelsPassed += currentEnemy.score
        count +=1
        print("Not what you expected. You think, what am I even looking for out here?")
    else:
        gameOver(levelsPassed)
        return

    pause = input("[]")

    print("You continue...")

    pause = input("[]")

    #load new enemy
    currentEnemy = enemyList[getEnemy(enemyList)]
    #combat
    encounterResult = combatEncounter(playerCharacter, currentEnemy)

    if(encounterResult == True):
        levelsPassed += currentEnemy.score
        count +=1
        print("You sense you're making progress, even if it's slow.")
    else:
        gameOver(levelsPassed)
        return


    #next encounter - strange innkeeper
    print("")
    encounterResult = innkeeperEncounter(playerCharacter)
    if(encounterResult == True):
        hasOrb = True

    pause = input("[]")
    
    if(hasOrb == True):
        print("\n[looking at the orb] Paradise, huh?")
    else:
        print("[you reflect on the journey you've had]")

    #get player's decision with the orb - returns true if now has map/false if has orb
    encounterResult = orbDecisions(playerCharacter, levelsPassed, hasOrb, questTaken)

    #if true, player has map/ if not player has orb
    if(encounterResult == True):
        hasMap = True
        hasOrb = False
    else:
        hasMap = False
        hasOrb = True

    #get decision to continue or not - false is no true is yes
    encounterResult = endGame(hasMap)

    if(encounterResult == False):
        gameOver(levelsPassed)
        return
    else:
        i = 0
        while(i < 3):
            pause = input("[]")
            #get new enemy
            currentEnemy = enemyList[getEnemy(enemyList)]
            #combat
            encounterResult = combatEncounter(playerCharacter, currentEnemy)
            #result
            if(encounterResult == True):
                levelsPassed += currentEnemy.score
                count += 1
                print("The journey continues...")
                i += 1
            else:
                gameOver(levelsPassed)
                return

    pause = input("[]")
    print("...")
    pause = input("[]")
    #if they make it to this point, they make it to paradise
    print("The trees clear. The skies are a beautiful pink and blueish hue. You feel the breeze brush up against you, and close your eyes.")
    levelsPassed += 149

    print("\nYou think, this must be paradise.")
    gameOver(levelsPassed)

if __name__ == "__main__":
    main()