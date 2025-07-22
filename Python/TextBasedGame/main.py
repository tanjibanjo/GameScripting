# Lane Pollock
# Game Scripting
# Text-Based Adventure

####################
#This text based adventure takes you, a traveler, through a dangerous and war-torn country as you fight (or not) your way through encounters on your journey.
####################

#IMPORTS
from TextBasedUtilities import *

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
        print("Give me your shit, then.")
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