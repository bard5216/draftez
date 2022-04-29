
window.draftpickHandler = function(event) {
    var data = JSON.parse(event.data);
    console.log("sse draftpick event:", data);


    var el = document.getElementById(`player-${data.player_id}`);
    if (el) {
        console.log(el);
        el.style['background-color'] = "orange";
    } else {
        console.log(`Could not locate player ${data.player_id}`);
    }
    // get the user card
    el = document.getElementById(`user-${data.user_id}`);
    // coln should be a table
    var coln = el.getElementsByTagName('table')
    if (coln) {
        // a Collection
        var table = coln[0];
        console.log(el);
        table.rows[data.round - 1].cells[1].innerHTML = data.player_name;
        table.rows[data.round - 1].cells[2].innerHTML = data.player_team_abbrev;
    }
    // Show notification.
    let msg = "<p class='is-size-4'>" + data.player_name + "(" + data.player_team_abbrev + ")</p>"
            + "<p class='is-size-6' style='margin-top: 1rem;line-height: 1;'>selected by " + data.user_name 
            + " in round " + data.round 
            + "</p>";
            //+ this.current_user.name;
    // The toast event must be wrapped in the CustomEvent > 'detail' property
    window.dispatchEvent(new CustomEvent('toast', {detail: {type: 'info', html: msg}}));
};


window.draftStatusHandler = function(event) {
    var data = JSON.parse(event.data);
    console.log("sse draft-status event: ", data);

    var el = document.getElementById("round");
    // console.log(el);
    if (el) {
        el.innerHTML = data.round;
    }
};

var event_source = new EventSource("/draft/stream");
event_source.onmessage = function(event) {
    var data = event.data;
    console.log("sse received with unknown event type:",data);
}
event_source.addEventListener('draft-status', function(event) {
    if (event['data']) {
        var data = JSON.parse(event['data']);
        window.dispatchEvent(new CustomEvent("draft-status", {detail: data}));
        //console.log("event_source.draft-status event: ", data);
    }
}, false);
event_source.addEventListener('draft-pick', function(event) {
    if (event['data']) {
        console.log("dispatching sse draft-pick event. data:",event['data']);
        var data = JSON.parse(event['data']);
        window.dispatchEvent(new CustomEvent("draft-pick", {detail: data}));
    }
}, false);