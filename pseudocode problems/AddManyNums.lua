
--Lane Pollock
--Pseudocode to Lua Assignments
--add numbers from the user until they say they are done

function printUserSum()
    local addNum = nil;
    local sum = 0;
    local done = false;
    local userChoice = nil;

    -- loop to control how many numbers to add
    while (done == false) do
        while(addNum == nil or addNum == "" or not tonumber(addNum)) do
            print("Enter number to add to sum: ");
            addNum = io.read();
        end
        --add number to sum, then reset variable **very important because our while loop checks 
        sum = addNum + sum;
        addNum = nil;

        --prompt if user wants to add another
        while(userChoice == nil or (userChoice ~= 'y' and userChoice ~= 'n')) do
            print("Add another?[y/n]");
            userChoice = io.read();
        end

        if(userChoice == 'n') then
            done = true;
        end

        --reset userChoice
        userChoice = nil;

    end
    print("Total: " .. sum);
end
