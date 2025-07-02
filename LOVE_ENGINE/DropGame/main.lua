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

    local count = 100; --number of stars on our canvas
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

--function draws the title screen
function titleDraw()
    love.graphics.setFont(love.graphics.newFont(100));
    --formatted print text
    love.graphics.printf(titleText, 0, 200, love.graphics.getWidth(), "center");

    --reset color
    love.graphics.setColor(1,1,1);
    --type, x, y, width, height, cornerx, cornery, segments
    love.graphics.rectangle("fill", 830, 800, 250, 100, 10, 10, 6)
    love.graphics.setColor(.3,.8,0)
    love.graphics.setFont(love.graphics.newFont(75))
    love.graphics.printf("Play", 830, 800, 250, "center")
    love.graphics.setColor(1,1,1) --reset color back to white
end

--function to draw the end screen
function drawEndScreen() 
    love.graphics.setFont(love.graphics.newFont(100));
    love.graphics.setColor(1,1,0);
    --formatted print text
    love.graphics.printf("Game Over", 0, 200, love.graphics.getWidth(), "center");
    love.graphics.printf("Score: " .. score, 0, 300, love.graphics.getWidth(), "center");
    --reset color
    love.graphics.setColor(1,1,1);
    --type, x, y, width, height, cornerx, cornery, segments
    love.graphics.rectangle("fill", 830, 800, 250, 100, 10, 10, 6)
    love.graphics.setColor(.3,.8,0)
    love.graphics.setFont(love.graphics.newFont(40))
    love.graphics.printf("Play Again?", 830, 800, 250, "center")
    love.graphics.setColor(1,1,1) --reset color back to white



end

--function to draw the score in the top right of the screen
function drawScore() 
    love.graphics.setFont(love.graphics.newFont(60));
    love.graphics.setColor(.3, .5, 0);
    --print the text to top right of screen - hard coded for 1080p
    love.graphics.printf(score, 1800, 75, 100, "center")

end

--function to draw the PowerUp in a random place
function drawPowerUp() 
    --draws power up at a random spot on the screen (hopefully)
    love.graphics.draw(powerUp, powerUpX, powerUpY);

    powerUpIsDrawn = true;

end



-- ******************************************************
--LOAD
-- ******************************************************
function love.load()
    --Randomization
    math.randomseed(os.time());
    math.random(); math.random(); math.random();
    
    --by default, love sets window to 800x600
    success = love.window.updateMode(1920, 1080);
    starsTable = randomizeStars(); --initialize stars x and y values into a table
    titleLoad(); --call screen function
    score = 0; --score is how many successful planets clicked before falling to edge
 
    --load image and set var to control click checks
    powerUp = love.graphics.newImage("icon_exclamationSmall.png");
    powerUpMod = math.random(7, 13);
    powerUpIsDrawn = false;
    powerUpX = math.random(20, love.graphics.getWidth() - powerUp:getWidth() - 20);
    powerUpY = math.random(20, love.graphics.getHeight() - powerUp:getHeight() - 80);
    --meteor setup
    meteor = love.graphics.newImage("meteor_large.png");

    

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
    minSpeed = 15;
    maxSpeed = 30;
    speedMod = math.random(3, 10);
    --i = planetNums;

    

    --populate the planets
    for i = planetNums, 0, -1 do
        --random point between 0 and width of screen minus width of picture (X COORDINATE IS AT TOP LEFT CORNER)
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
            if x >= 830 and x <= 1050 and y >=800 and y <= 900 then
                scene = 1;
            end

        end
        --if in game
        if scene == 1 then
            --check each image to see if collision with mouse
            for i, value in ipairs(planetX) do
                if ((x >= planetX[i]) and (x <= planetX[i] + planetA:getWidth()) and (y >= planetY[i]) and (y <= planetY[i] + planetA:getHeight())) then
                    print("Clicked on planet");
                    score = score + 1;
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
                    break --only clicks one planet and not overlapping
                end --end if
            end --end for all planets  

            --check if collision with power up
            if(powerUpIsDrawn == true) then
                if(x >= powerUpX and x <= powerUpX + powerUp:getWidth() and y >= powerUpY and y <= powerUpY + powerUp:getHeight()) then
                    --move sprite off screen
                    powerUpX = 0
                    powerUpY = 0 - powerUp:getHeight();
                    --adjust the new powerUpMod that acts as a trigger for drawing the powerup
                    powerUpMod = score + math.random(6, 12);
                    --Use the power up, which will make the planets go slower
                    for i, value in ipairs(planetX) do
                        planetSpeed[i] = 30;
                    end
                    minSpeed = minSpeed - 40;
                    maxSpeed = maxSpeed - 40;
                    speedMod = 10;

                    powerUpIsDrawn = false; --reset check boolean

                end
            end --end isdrawn check
        end --end scene if

        --if game over
        if scene == 2 then
            if x >= 830 and x <= 1050 and y >=800 and y <= 900 then
                love.event.quit('restart');
            end
        end
    end -- button if
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
                scene = 2;
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

        --draw meteors at bottom
        for i = 0, love.graphics.getWidth(), meteor:getWidth() do
            love.graphics.draw(meteor, i, love.graphics.getHeight() - meteor:getHeight());
        end

        --draw score
        drawScore();

        --under the right circumstances, draw the powerUp
        --powerUpMod is the trigger for drawing the power up- if the score reaches a certain amount - it only dissapears when clicked.
        if score >= powerUpMod then
            if powerUpIsDrawn == false then --if powerup is being 'respawned' get new positions for it, then lock behind check so it doesn't move around
                powerUpX = math.random(20, love.graphics.getWidth() - powerUp:getWidth() - 20);
                powerUpY = math.random(20, love.graphics.getHeight() - powerUp:getHeight() - 80);
            end
            drawPowerUp();
        end

    end
    --game over
    if (scene == 2) then
        drawEndScreen();
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
