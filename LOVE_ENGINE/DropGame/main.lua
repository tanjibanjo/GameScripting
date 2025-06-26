-- NEEDED CODE FOR LOVE DEBUGGER
if arg[2] == "debug" then
    require("lldebugger").start()
end
-- END





-- NEEDED CODE FOR LOVE DEBUGGER
local love_errorhandler = love.errorhandler

function love.errorhandler(msg)
    if lldebugger then
        error(msg, 2)
    else
        return love_errorhandler(msg)
    end
end
-- END