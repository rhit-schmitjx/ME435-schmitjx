function hackyMqttTest()
    clc
    fprintf("Hacky MQTT Test in MATLAB\n")
    mqClient = mqttclient("tcp://mosquitto.csse.rose-hulman.edu");
    % mqClient.Connected
    mqClient.subscribe("schmitjx", "Callback", @myCallback)
    for k = 1:3
       pause(1)
    %     message = sprintf("My number is %d.", k);
    %     write(mqClient, "fisherds", message);
       messageStruct.type = "chat";
       messageStruct.payload = sprintf("My number is %d.", k);
       message = jsonencode(messageStruct);
       mqClient.write("schmitjx", message);
    end
    pause(1)  % small delay to receive the last message
end

function myCallback(topic, message)
    messageStruct = jsondecode(message);
    messageType = messageStruct.type
    payload = messageStruct.payload
end
