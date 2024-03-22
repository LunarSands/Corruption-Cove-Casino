// on initialize: set default images on stationay wheels
const WHEEL_OPACITY_TIME = 1500;
const SPIN_TIME = 2000;
var message = "You have won: "
for (let i = 1; i<=3; i++){
    document.getElementById("s" + i).src = "/static/images/slots/" + machine + "/1.png";
}

function startWheels() {
    document.getElementById("w1").style["opacity"] = 100;
    document.getElementById("w2").style["opacity"] = 100;
    document.getElementById("w3").style["opacity"] = 100;
    // send request to server, get randomly generated results of the spin, set final images to them
    // at server level - update bets, update money account
    let request = {action:'start', machine:machine}
    $.post({url:slots_api,
        data:JSON.stringify(request),
        headers:{'X-CSRFToken':csrftoken},
        success: function(output) {
            let spinResultObjects = output.spin_result;
            let spinResultAmount = output.spin_amount;
            message = message.concat(spinResultAmount);
            if (spinResultAmount == 1000){
                message = message.concat(", JACKPOT!");
            }
            message = message.concat("\nYou have lost: -100");
            let slotResultImgObjects = document.getElementsByClassName('wheel stopped');

            for (let index=0; index<slotResultImgObjects.length; index++) {
                const imgElement = slotResultImgObjects[index];
                const resultElement = spinResultObjects[index];
                imgElement.src = "/static/images/slots/" + machine + "/" + resultElement + ".png";
            }

            setTimeout(stopWheels, SPIN_TIME);
        }, error: function () {
            alert("An error occured...");
            setTimeout(stopWheels, 0);
        }
    });
}

function stopWheels() {
    setTimeout(function() {
        document.getElementById("w1").style["opacity"] = 0;
        setTimeout(function() {
            document.getElementById("w2").style["opacity"] = 0;
            setTimeout(function() {
                document.getElementById("w3").style["opacity"] = 0;
                setTimeout(function() {
                    alert(message);
                    location.reload();
                }, WHEEL_OPACITY_TIME)
            }, WHEEL_OPACITY_TIME)
        }, WHEEL_OPACITY_TIME)  
    }, WHEEL_OPACITY_TIME)
}