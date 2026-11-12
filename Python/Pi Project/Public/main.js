async function sendBlindCommand(command) {
    var response = await fetch(`/api/blinds/${command}`);
    var replyText = await response.text();
    document.querySelector("#replyText").innerHTML = replyText;
    return replyText;
}

async function rotateDegrees(degrees) {
    var response = await fetch(`/api/rotate/${degrees}`);
    var replyText = await response.text();
    document.querySelector("#replyText").innerHTML = replyText;
    return replyText;
}

async function setAlarmTime(hour, minute) {
    var response = await fetch(`/api/alarm/${hour}/${minute}`);
    var replyText = await response.text();
    document.querySelector("#replyText").innerHTML = replyText;
    return replyText;
}

function main() {
    document.querySelector("#open").onclick = () => {
        sendBlindCommand("open");
    };
    
    document.querySelector("#close").onclick = () => {
        sendBlindCommand("close");
    };

    document.querySelector("#rotateBtn").onclick = () => {
        let degrees = document.querySelector("#degreesInput").value;
        rotateDegrees(degrees);
    };

    document.querySelector("#setAlarmBtn").onclick = () => {
        let hour = document.querySelector("#alarmHour").value;
        let minute = document.querySelector("#alarmMinute").value;
        setAlarmTime(hour, minute);
    };
}

main();