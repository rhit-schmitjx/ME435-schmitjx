classdef LEDexam < hgsetget
    %PLATELOADER Controls the Beckman Coulter Plate Loader Robot
    %   Performs the basic actions to control the plate loader

    properties
        piAddress
    end

    methods (Access = private)
        
    end

    methods
        function response = LEDOnOff(obj, command)
            import matlab.net.*
            import matlab.net.http.*

            r = RequestMessage;
            uri = URI("http://" + obj.piAddress + ":5000/api/led/" + command);

            resp = send(r, uri);
            response = resp.Body.Data;

            fprintf("%s\n", response);
        end
        function response = Flash(obj, numFlash, timeDelay)
            import matlab.net.*
            import matlab.net.http.*

            r = RequestMessage;
            uri = URI("http://" + obj.piAddress + ":5000/api/flash/" + numFlash + "/" + timeDelay);

            resp = send(r, uri);
            response = resp.Body.Data;

            fprintf("%s\n",response);
        end

        function obj = LEDexam(piIP)
            obj.piAddress = piIP;
        end
    end
end