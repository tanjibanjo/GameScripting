--Lane Pollock
--LoveEngine
--Drop Game
--26 Jun 2025

--DEBUGGER RUNNING - F5 for debug, or SHIFT F5 for non-debug

-- NEEDED CODE FOR LOVE DEBUGGER
if arg[2] == "debug" then
    require("lldebugger").start()
end

-- ******************************************************MAIN BLOCK

--[[
- Game where multiple images fall from the sky
- User clicks to send themselves back to the top
- Click images before they hit the bottom or game over

- Should have title screen, level 1, game over
]]

--create a randomized table of stars
function randomizeStars()
    --set up randomization
    math.randomseed(os.time());
    math.random(); math.random(); math.random();

    count = 100; --number of stars on our canvas
    stars = {}; --table of x,y values for our star locations

    while count > 0 do
        stars[#stars+1] = math.random(0, love.graphics.getWidth()); --random x value
        stars[#stars+1] = math.random(0, love.graphics.getHeight()); --random y value
        --decrease lcv
        count = count - 1;
    end
    return stars; --return the table
end

--function to draw the stars, takes a table of x and y coordinates
function drawStars(stars)
    --starglow (bigger brush, light opacity)
    love.graphics.setColor(math.random(), math.random(), math.random(), .22) --fourth value is the opacity /alpha
    love.graphics.setPointSize(10)
    love.graphics.points(stars)
    --center (small brush, high opacity)
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.setPointSize(2)
    love.graphics.points(stars)

end

--function to set the window size
function titleLoad()
    planetA = love.graphics.newImage("planet_blue_smaller.png");
    titleText = "Drop Game";
    love.window.setTitle(titleText);
end

function titleDraw()
    love.graphics.setFont(love.graphics.newFont(100));
    --formatted print text
    love.graphics.printf(titleText, 0, 200, love.graphics.getWidth(), "center");

    --reset color
    love.graphics.setColor(1,1,1);
    --type, x, y, width, height, cornerx, cornery, segments
    love.graphics.rectangle("fill", 50, 450, 250, 100, 10, 10, 6)
    love.graphics.setColor(.3,.8,0)
    love.graphics.setFont(love.graphics.newFont(75))
    love.graphics.printf("Play", 50, 450, 250, "center")
    love.graphics.setColor(1,1,1) --reset color back to white
end

-- ******************************************************
--LOAD
-- ******************************************************
function love.load()
    --by default, love sets window to 800x600
    success = love.window.updateMode(800, 600);
    starsTable = randomizeStars();
    titleLoad(); --call screen function
    

    --[[create scene variable 
        0 = title screen
        1 = game screen
        2 = game over screen]]

    scene = 0;
    
    --get planet variables
    
    planetNums = 5;
    planetX = {} --where at (x)
    planetY = {} --where at (y)
    planetSpeed = {} --how fast
    minSpeed = 20;
    maxSpeed = 45;
    speedMod = 10;
    --i = planetNums;

    --Randomization
    math.randomseed(os.time());
    math.random(); math.random(); math.random();

    --populate the planets
    for i = planetNums, 0, -1 do
        --random point between 0 and widh of screen minus width of picture (X COORDINATE IS AT TOP LEFT CORNER)
        planetX[#planetX+1] = math.random(0, love.graphics.getWidth() - planetA:getWidth());
        --get random y value between 1 and 2 planets' height ABOVE the window so they drop from offscreen **Remember, LOVE literally uses pixel coordinates
        planetY[#planetY+1] = 0 - math.random(planetA:getHeight(), planetA:getHeight()*2);

        --get random speed between min and max
        planetSpeed[#planetSpeed+1] = math.random(minSpeed, maxSpeed);
    end

end --end load

-- ******************************************************
--CLICK THINGS
-- ******************************************************
function love.mousepressed(x, y, button, istouch)
    --if left click
    if button == 1 then
        --if on title screen
        if scene == 0 then
            --click on play button, play game
            if x >= 50 and x <= 300 and y >=450 and y <= 550 then
                scene = 1;
            end

        end
        --if in game
        if scene == 1 then
            --check each image to see if collision with mouse
            for i, value in ipairs(planetX) do
                if ((x >= planetX[i]) and (x <= planetX[i] + planetA:getWidth()) and (y >= planetY[i]) and (y <= planetY[i] + planetA:getHeight())) then
                    print("Clicked on planet");
                    --re seed the random
                    math.randomseed(os.time());
                    math.random(); math.random(); math.random();
                    --send back to top and mod speed
                    maxSpeed = maxSpeed + speedMod;
                    minSpeed = minSpeed + speedMod;
                    speedMod = speedMod + 5;
                    planetX[i] = math.random(0, love.graphics.getWidth() - planetA:getWidth())
                    planetY[i] = 0 -math.random(planetA:getHeight(), planetA:getHeight() * 2);
                    planetSpeed[i] = math.random(planetSpeed[i], maxSpeed);
                    break --only clicks one thing and not overlapping
                end
            end
        end
    end
end

-- ******************************************************
--UPDATE
-- ******************************************************
function love.update(dt)

    if scene == 0 then
        
    end


    --if gameplay screen
    if scene == 1 then
        for i, value in ipairs(planetX) do
            --move slime
            if(planetY[i] + planetA:getHeight() >= love.graphics.getHeight()) then
                print("GAMEOVER")
                love.event.quit('restart');
            end

            planetY[i] = planetY[i] + planetSpeed[i] * dt;
        end
    end
end

-- ******************************************************
--DRAW
-- ******************************************************
function love.draw()
    drawStars(stars)
    --title screen
    if (scene == 0) then
        titleDraw();
    end
    --gameplay
    if (scene == 1) then
        for i, value in ipairs(planetX) do
            love.graphics.draw(planetA, planetX[i], planetY[i])
        end
    end
    --game over
    if (scene == 2) then

    end

end


-- ******************************************************
--END MAIN BLOCK
-- ******************************************************

-- NEEDED CODE FOR LOVE DEBUGGER
local love_errorhandler = love.errorhandler

function love.errorhandler(msg)
    if lldebugger then
        error(msg, 2)
    else
        return love_errorhandler(msg)
    end
end
