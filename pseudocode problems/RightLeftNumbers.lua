--Lane Pollock
--Pseudocode to Lua Assignments
--this function will generate 10 random numbers, assigning them to left or right based on if they are even or odd, then display results

function runGenerator()
    --local variables
    local i = 0;
    local randomNum = nil;
    local evenCount = 0;
    local oddCount = 0;

    --seed and warm up the generator
    math.randomseed(os.time());
    math.random(); math.random(); math.random();

    --set up main loop
    while (i <  10) do
        randomNum = math.random(0, 100);

        print("Number: " .. randomNum);

        if(randomNum == 0) then --0 gets counted as even
            print("RIGHT");
            evenCount = evenCount + 1;
        elseif (randomNum % 2 == 0) then --number is even
            print("RIGHT");
            evenCount = evenCount + 1;
        else --number is odd
            print("LEFT");
            oddCount = oddCount + 1;
        end

        --increment index
        i = i + 1;

    end

    --print the closing stats
    print("Number of occurances\nLeft: " .. oddCount .. "\nRight: " .. evenCount);

end