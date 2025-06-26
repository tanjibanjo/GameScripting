--Lane Pollock
--LoveEngine
--26 Jun 2025

--DEBUGGER RUNNING - F5 for debug, or SHIFT F5 for non-debug

-- NEEDED CODE FOR LOVE DEBUGGER
if arg[2] == "debug" then
    require("lldebugger").start()
end

-- MAIN 
function love.load()

end

function love.update(dt)

end

function love.draw()

end


-- END MAIN

-- NEEDED CODE FOR LOVE DEBUGGER
local love_errorhandler = love.errorhandler

function love.errorhandler(msg)
    if lldebugger then
        error(msg, 2)
    else
        return love_errorhandler(msg)
    end
end
