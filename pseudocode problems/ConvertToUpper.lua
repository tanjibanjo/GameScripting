--Lane Pollock
--Pseudocode to Lua Assignments

-- take user input and capitalize it, then print the result.

function capitalizeInput()
    --local variables
    local userInput = nil;
    local upperCaseResult = nil;

    --prompt for input
    while(userInput == nil or userInput == ""  or userInput == string.upper(userInput) or tonumber(userInput)) do
        print("Enter input to capitalize: ")
        userInput = io.read()
    end

    upperCaseResult = string.upper(userInput);

    print(upperCaseResult)
end