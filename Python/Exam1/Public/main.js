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
}
main();