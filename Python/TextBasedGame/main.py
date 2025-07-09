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
    playerCharacter = Character("name", 1, 1, 1, "class") #default values
    levelsPassed = 0.0 
    pause = '' #can be used as a dummy variable to pause the game

    #start the game by loading enemies and characters
    loadEnemies(enemyList)
    loadCharacters(characterList)

    #print intro
    printIntro()

    #get player character, and first encounter set up
    getPlayerCharacter(playerCharacter, characterList, enemyList)

    


if __name__ == "__main__":
    main()