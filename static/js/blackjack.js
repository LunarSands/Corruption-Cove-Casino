fetch(api_url)
        .then(data=>data.json())
        .then(data=>display_state(data));
    function display_hand(hand,id){
        document.getElementById(id).innerHTML = "";
        for(card of hand){
            document.getElementById(id).innerHTML += `<img class="card" src="${cards_url}/${card[0]+card[1]}.png"">`
        }
        return hand?.map(card=> card.join("")).join(",");
    }
    function display_state(state){
        console.log(state);
        hands = state.hands;
        dealer_hand = state.dealer_hand;
        bet = JSON.stringify(state.bets);
        document.querySelectorAll('.actions>button').forEach(button=>button.setAttribute('disabled',true));
        document.getElementById('how-to').removeAttribute('disabled');
        Object.entries(state.valid_actions)
            .forEach(entry=>entry[1].forEach(action=>document.getElementById(`${action}_${entry[0]}`).removeAttribute('disabled')));
        document.getElementById('hand-0').innerHTML="";
        document.getElementById('hand-1').innerHTML="";
        for (let i = 0; i < hands.length; i++) {
            display_hand(hands[i],`hand-${i}`);
        }
        display_hand(dealer_hand,'dealer-hand');
        if(state.finished){
            setTimeout(()=>alert(`You won ${state.winnings}`),500);
        }
    }
    function do_action(action,hand_no, rate){
        let rate = parseFloat(rate);
        console.log(action);
        fetch(api_url,{method:'post',headers:{'X-CSRFToken':csrftoken},body:JSON.stringify(
            {action:action,hand_no:hand_no,bet:{amount:parseInt(document.getElementById('bet_amount').value)/rate}}
        )})
        .then(res=> res.json())
        .then(json=>display_state(json));
    }