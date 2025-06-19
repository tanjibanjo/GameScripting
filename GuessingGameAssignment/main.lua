--[[
Lane Pollock
19 Jun 2025
Lua Language - Guessing Game
Assignment: Create a lua program that chooses a random number from 1-100 and gives player 7 attempts to guess it correctly
--]]

--local variables
local correctNumber = nil;
local userGuess = nil;
local attempts = 0;
local continue = true;
local playAgain = true;
local userChoice = nil;

--set up main loop
while(playAgain ~= false) do --player wants to keep playing
    print("Welcome to the guessing game. A number will be generated between 1-100, and it's your job to guess it.\nYou have seven tries.")

    --seed and warm generator
    math.randomseed(os.time())
    math.random(); math.random(); math.random();

    --generate number
    correctNumber = math.random(100);
    print("\nNumber is generated.");

    --guessing loop
    while(attempts < 7 and continue == true) do --while user has not guessed 7 times or guessed correctly
        --get user guess
        while(userGuess == nil or not tonumber(userGuess)) do--while nil or not number
            print("Enter a valid guess 1-100: ");
            userGuess = io.read();
        end

        --check guess
        if(userGuess == correctNumber) then --if correct, stop loop
            continue = false;
        else
            attempts = attempts + 1; --else, increment attempts
            print("Incorrect, attempts remaining: " .. 7 - attempts)
        end

        --reset guess variable and continue
        userGuess = nil;
    end

    --check continue status and print win/lose message
    if(continue == false) then --user has won
        print("Number guessed correctly!");
    else
        print("No more attempts remaining.");
        print("Correct number was " .. correctNumber);
    end

    print("Press 'q' to quit or Enter to play again.")
    --prompt if user wants to play again?
    while(userChoice == nil or tonumber(userChoice)) do --while choice is a number or nil
        userChoice = io.read();
    end
    if(userChoice == 'q') then
        playAgain = false;
        print("Goodbye.");
    else
        --reset the game variables
        userChoice = nil;
        userGuess = nil;
        continue = true;
        attempts = 0;
        correctNumber = nil;
    end

end