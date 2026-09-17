classdef MyShape < handle

    properties
        Patch matlab.graphics.primitive.Patch
        
    end

    methods
        function obj = MyShape(xCoords,yCoords, color)
            obj.Patch = patch(xCoords, yCoords, color);
        end

        function move(obj,dx,dy)
            obj.Patch.XData = obj.Patch.XData + dx
            obj.Patch.YData = obj.Patch.YData + dy
        end
    end
end