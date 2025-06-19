--Lane Pollock
--Pseudocode to Lua Assignments

--take two numbers from user, print together and return sum
function printTwoNumSum()
    --variables
    local num1 = nil;
    local num2 = nil;
    local sum = 0;

    while (num1 == nil or num1 == "" or not tonumber(num1)) do
        --prompt for numbers
        print("Enter first number: ");
        num1 = io.read();
    end

    while (num2 == nil or num2 == "" or not tonumber(num2)) do
        --prompt for numbers
        print("Enter second number: ");
        num2 = io.read();
    end

    sum = num1 + num2;
    print(sum);

end