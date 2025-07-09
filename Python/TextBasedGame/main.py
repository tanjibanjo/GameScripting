# Lane Pollock
# Game Scripting
# Text-Based Adventure
# Create a text based adventure with at least 10 prompts

#IMPORTS
from TextBasedUtilities import *

#__MAIN__
def main():
    #local variables
    enemyList = []
    characterList = []
    playerCharacter = Character("You", 50, 30, 85, "class") #default values
    currentEnemy = Enemy("name", 1, 1, False) #default values - this will be reset with values every encounter
    levelsPassed = 0.0 
    count = 0 #keeps track of how many enemies you have faced

    #start the game by loading enemies and characters
    loadEnemies(enemyList)
    loadCharacters(characterList)

    #INTRO SEQUENCE
    encounterResult = introSequence() #stores the true or false in a variable

    if(encounterResult == True): #at door of villager
        print("The door opens, but just barely. There's litle light but you hear a voice from within.")
        #get player character
        getPlayerCharacter(playerCharacter, characterList)
    else: #camped
        print("You hear a noise, and jump up to see what it is. What a drag.\n")

        pause = input("[] (when you see empty brackets, press enter to progress)")

        print()

        #get enemy from list and assign
        currentEnemy = enemyList[getEnemy(enemyList)]
        #enemy cannot be villager
        while(currentEnemy.name == "Greedy Villager"):
            #get enemy from list and assign
            currentEnemy = enemyList[getEnemy(enemyList)]

        #combat encounter
        encounterResult = combatEncounter(playerCharacter, currentEnemy, levelsPassed)
        count += 1

        #if survived, go to the village and get character all the same
        if(encounterResult == True):
            print("You made it, and decide to go to the village because it sucks out here. Walking up to the house, the door creaks open and you hear a voice.")
            pause = input("[]")
            #get player character
            getPlayerCharacter(playerCharacter, characterList)

    pause = input("[]")

    #next encounter is the village person encounter
    encounterResult = villagePersonEncounter()
    if (encounterResult == False): #not helping villager
        currentEnemy = enemyList[8] #greedy villager
        print("Give me your shit, then.")
        encounterResult = combatEncounter(playerCharacter, currentEnemy, levelsPassed)

        if(encounterResult == True):
            print("You rummage around the villager's house as you take shelter. Strange notes and bones lay around.\nYou think maybe it was a good thing you didn't help them.")
            count += 1

    pause = input("[]")

    #transition to the next encounter
    print("\nThe next day, ther's no one around. No villagers. You decide to carry on, into what the villager called 'the nothing'. Just looks like a forest to you.")

    #journey begins, combat encounters
    print("You journey on through the forest. There really is nothing but trees here, until you hear something in the distance. You venture closer...")

    pause = input("[]")

    #load new enemy
    currentEnemy = enemyList[getEnemy(enemyList)]
    #combat
    encounterResult = combatEncounter(playerCharacter, currentEnemy, levelsPassed)
    
    if(encounterResult == True):
        count +=1
        print("Not what you expected. You think what am I even looking for out here?")

    pause = input("[]")

    print("You continue...")

    pause = input("[]")

    #load new enemy
    currentEnemy = enemyList[getEnemy(enemyList)]
    #combat
    encounterResult = combatEncounter(playerCharacter, currentEnemy, levelsPassed)

    if(encounterResult == True):
        count +=1
        print("You sense you're making progress, even if it's slow.")


if __name__ == "__main__":
    main()