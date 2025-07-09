#Lane Pollock
#8 July 2025
#program holds utility functions for the text based adventure game 

from CharactersClass import Character
from CharactersClass import Enemy

#function takes list and loads 9 enemies
def loadEnemies(enemyList):
    #enemies list
    wolf = Enemy("Wolf", 50, 10, False)
    giantSpider = Enemy("Giant Spider", 90, 30, False)
    unicorn = Enemy("Unicorn", 1, -20, False) #this one returns health
    demon = Enemy("Demon", 65, 25, False)
    orc = Enemy("Orc", 40, 20, False)
    orcLeader = Enemy("Orc Leader", 80, 40, False)
    goblin = Enemy("Goblin", 35, 15, False)
    swordsman = Enemy("Swordsman", 50, 25, False)
    greedyVillager = Enemy("Greedy Villager", 20, 20, 0)

    #add all the enemies to the list - could initialize them in the extend statement, but it's not pretty
    #extend allows the list to not be resized every addition
    enemyList.extend([wolf, giantSpider, unicorn, demon, orc, orcLeader, goblin, swordsman, greedyVillager])

#function takes the list of characters and loads the options for player character
def loadCharacters(characterList):
    #characters to be added
    mage = Character("Mage", 50, "20-60", 40, "Mage")
    rogue = Character("Rogue", 65, "0-25 x2", 75, "Rogue")
    warrior = Character("Warrior", 80, "35-50", 50, "Warrior")

    #add characters
    characterList.extend([mage, rogue, warrior])

#function prints the welcome message and background to the story
def printIntro():
    print("Intro goes here")

#function prompts player for information on making their own character
def getPlayerCharacter(playerCharacter, characterList, enemyList):
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
        return

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
                except Exception as e:
                    print("An error occured.")
                    return
            case _: #default
                print("Not a choice...")

    #once name is good, assign to player character
    playerCharacter.name = name

    #now, get player class decision and load the rest of the stats to the player character
    print()
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
    print("\n{%s}," % name + " a %s. Good timing too, I could really use your help." % playerCharacter.type)