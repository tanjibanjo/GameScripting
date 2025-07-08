#Lane Pollock
#8 Juy 2025
#Pseudocode to Python
#take a user string and print out capitalized version

#check if number
def checkIfNumber(userInput):
    if userInput.isdigit():
        print("Numbers cannot be capitalized.")
    return userInput.isdigit()

#check if spaces
def checkIfSpaces(userInput):
    if userInput.isspace():
        print("Spaces cannot be capitalized.")
    return userInput.isspace()

#check if empty
def checkIfEmpty(userInput):
    if not userInput:
        print("Empty!")
        return True
    else:
        return False

#check if already capitalized
def checkIfCapped(userInput):
    if userInput == str.upper(userInput):
        print("Already capitalized.")
        return True
    else:
        return False

#check all
def checkAll(userInput):
    while CheckIfNumber(userInput) or CheckIfSpaces(userInput) or CheckIfEmpty(userInput) or CheckIfCapped(userInput):
        userInput = input("Type something else: ")
    return userInput

strToUpper = input("Write something to capitalize: ")
print(str.upper(checkAll(strToUpper)))

#most simple - but not elegant
#print(str.upper(input("Write something to capitalize: ")))