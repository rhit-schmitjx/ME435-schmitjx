async function onOff(command) {
    var response = await fetch(`/api/led/${command}`);
    var replyText = await response.text();
    console.log(replyText);
    
    document.querySelector("#replyText").innerHTML = replyText;
    
    return(replyText);

}

async function flash(numFlashes, timeDelay) {
    var response = await fetch(`/api/flash/${numFlashes}/${timeDelay}`);
    var replyText = await response.text();
    console.log(replyText);
    
    document.querySelector("#replyText").innerHTML = replyText;
    
    return(replyText);

}


function main(){
    console.log("Hello JavaScript:");
    //document.querySelector("#reset").innerHTML = "Hello";

    document.querySelector("#on").onclick = () => {
        console.log("LED On button pressed");
        onOff("ON");
    };
    document.querySelector("#off").onclick = () => {
        console.log("LED Off button pressed");
        onOff("OFF");
    };
    document.querySelector("#flash").onclick = () => {
        let numFlashes = document.querySelector("#numFlashes").value;
        let timeDelay = document.querySelector("#timeDelay").value;
        flash(numFlashes, timeDelay);
    };
}
main();