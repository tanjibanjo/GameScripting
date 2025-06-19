--Lane Pollock
--Pseudocode to Lua Assignments

--get user input and generate a random number from 1 to that number

function GenerateRandomUserNumber()
    --local variables
    local maxNum = nil;
    local playAgain = true;

    --seed the generator and warm it up
        math.randomseed(os.time());
        math.random(); math.random(); math.random();

    --main loop
    while(playAgain ~= false) do

        --get input from user for the max number
        print("Enter a number. A random number will be generated between 1 and your number.")
        maxNum = io.read();
        --validate
        while(maxNum == nil or maxNum == "" or not tonumber(maxNum)) do
            print("Invalid. Enter a number.")
            maxNum = io.read();
        end

        --generate and print the random number
        print("Random Number: " .. math.random(maxNum));

        print("Press q to quit. Enter to continue.");

        if(io.read() == 'q') then
            playAgain = false;
        end


    end
end