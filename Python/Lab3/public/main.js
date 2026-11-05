async function sendCommand(command) {
    var response = await fetch(`/api/${command}`);
    var replyText = await response.text();
    console.log(replyText);
    
    document.querySelector("#replyText").innerHTML = replyText;
    
    return(replyText);

}


function main(){
    console.log("Hello JavaScript:");
    //document.querySelector("#reset").innerHTML = "Hello";

    document.querySelector("#reset").onclick = () => {
        console.log("You pressed the button!");
        sendCommand("RESET");
    };
    document.querySelector("#x1").onclick = () => {
        sendCommand("X-AXIS 1");
    };
    document.querySelector("#x2").onclick = () => {
        sendCommand("X-AXIS 2");
    };
    document.querySelector("#x3").onclick = () => {
        sendCommand("X-AXIS 3");
    };
    document.querySelector("#x4").onclick = () => {
        sendCommand("X-AXIS 4");
    };
    document.querySelector("#x5").onclick = () => {
        sendCommand("X-AXIS 5");
    };

    document.querySelector("#gOpen").onclick = () => {
        sendCommand("GRIPPER OPEN");
    };
    document.querySelector("#gclose").onclick = () => {
        sendCommand("GRIPPER CLOSE");
    };
    document.querySelector("#Status").onclick = () => {
        sendCommand("LOADER_STATUS");
    };
    document.querySelector("#zExtend").onclick = () => {
        sendCommand("Z-AXIS EXTEND");
    };
    document.querySelector("#zRetract").onclick = () => {
        sendCommand("Z-AXIS RETRACT");
    };
    document.querySelector("#Move").onclick = () => {
        let startPos = document.querySelector("#moveFrom").value;
        let endPos = document.querySelector("#moveTo").value;
        sendCommand(`MOVE ${startPos} ${endPos}`);
    };
}
main();