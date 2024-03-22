var moneyBet = 0;
const currentBets = new Map();
var request = {action:'start',bets:[]}
const resultMap = new Map();
const oddsBet = new Map();
const betData = JSON.parse(document.getElementById('bet-data').textContent);
const betTypes = betData.map(bet_data=>bet_data.type);
const order = [0, 14, 31, 2, 33, 18, 27, 6, 21, 10, 19, 23, 4, 25, 12, 35, 16, 29, 8, 34, 13, 32, 9, 20, 17, 30, 1, 26, 5, 7, 22, 11, 36, 15, 28, 3, 24];
const red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36];

for (let i = 0; i < order.length; i++) {
    resultMap.set(i, order[i]);
}

for (let i = 0; i < betTypes.length; i++) {
    currentBets.set(betTypes[i], 0);
}

for (let i = 1; i < 37; i++){
    if (red.includes(i)){
        document.getElementsByClassName("bet-" + i)[0].style["background-color"] = "rgb(174, 13, 13)";
    }
    else {
        document.getElementsByClassName("bet-" + i)[0].style["background-color"] = "black";
    }
}
document.getElementsByClassName("bet-red")[0].style["background-color"] = "rgb(174, 13, 13)";
document.getElementsByClassName("bet-black")[0].style["background-color"] = "black";

function addBetValue(bet) {
    currentBets.set(bet, currentBets.get(bet)+100)
    moneyBet += 100;
    checkBet()
}

function checkBet() {
    let outputText = "You have placed:<br>";
    for (let i = 0; i < betTypes.length; i++) {
        if (currentBets.get(betTypes[i]) != 0){
            if (betTypes[i].replace('bet-','') == '1st' || betTypes[i].replace('bet-','') == '2nd' || betTypes[i].replace('bet-','') == '3rd'){
                outputText = outputText.concat(currentBets.get(betTypes[i]), " on the ", betTypes[i].replace('bet-',''), " dozen<br>");
            }
            else if (betTypes[i].replace('bet-','') == 'row1'){
                outputText = outputText.concat(currentBets.get(betTypes[i]), " on the 1st column<br>");
            }
            else if (betTypes[i].replace('bet-','') == 'row2'){
                outputText = outputText.concat(currentBets.get(betTypes[i]), " on the 2nd column<br>");
            }
            else if (betTypes[i].replace('bet-','') == 'row3'){
                outputText = outputText.concat(currentBets.get(betTypes[i]), " on the 3rd column<br>");
            }
            else{
                outputText = outputText.concat(currentBets.get(betTypes[i]), " on ", betTypes[i].replace('bet-',''), "<br>");
            }
        }
    }
    if (outputText == "You have placed:<br>"){
        outputText = outputText.concat("No bets so far!");
    }
    document.getElementById("bet-info").innerHTML = outputText;
}
function clearBet() {
    for (let i = 0; i < betTypes.length; i++) {
        currentBets.set(betTypes[i], 0)
    }
    moneyBet = 0;
    request = {action:'start',bets:[]}
    checkBet()
}

function validate(){
    var flag = false;
    for (let i = 0; i < betTypes.length; i++) {
        if (currentBets.get(betTypes[i]) != 0){
            flag = true;
            break;
        }
    }
    if (flag){
        startBall();
    }
    else{
        alert("Place your bets before starting the ball!")
    }
}

function startBall(){
    for (const betType of currentBets.keys()) {
        request.bets.push({'type':betType,'amount':currentBets.get(betType)})
    }
    $.post({url:play_roulette_url,
        data:JSON.stringify(request),
        headers:{'X-CSRFToken':csrftoken},
        success: function(output) {
        let message = "Your winnings: ";
        let result = output.result
        let winnings = output.winnings
        message = message.concat(winnings);
        message = message.concat("\nYour losses: -");
        message = message.concat(moneyBet);
        document.getElementsByClassName("ball_roulette")[0].style["display"] = "inline";
        document.getElementsByClassName("ball_roulette")[0].style["animation-iteration-count"] = order[result]/37 + 3;
        document.getElementsByClassName("ball_roulette")[0].style["animation-play-state"] = "running";
        setTimeout(function(){
            document.getElementsByClassName("ball_roulette")[0].src = roulette_ball_url;
            setTimeout(function() {
                alert(message);
                location.reload();
            }, 1000)
        }, (order[result]/37 + 3) * 2000)
    }})
}