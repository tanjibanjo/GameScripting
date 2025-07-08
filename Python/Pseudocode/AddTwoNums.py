#take two numbers from user and print the sum

#check if it is number
def isNum(userInput):
    return bool(userInput.isdigit() or isinstance(userInput, float)) #casting to bool to make sure it returns the way we want

#while not a number, keep prompting
def tryAgain(userInput):
    while not isNum(userInput):
        userInput = input("That is not a number I can add. Try again: ")
    return userInput

#__MAIN__
num1 = input("Give me a number: ")
num1 = tryAgain(num1)

num2 = input("Give me one more number: ")
num2 = tryAgain(num2)

print(num1 + " + " + num2 + " = " + str(float(num1) + float(num2)))