let currentPlace = null;

function loadRandomPlace() {
    fetch('/random_place')
        .then(res => res.json())
        .then(data => {
            currentPlace = data;
            document.getElementById('place-img').src = data.img;
            document.getElementById('hint').innerText = 'Hint: ' + data.hint;
            document.getElementById('result').innerText = '';
            document.getElementById('guess-input').value = '';
            document.getElementById('next-btn').style.display = 'none';
            document.getElementById('submit-btn').disabled = false;
        });
}

document.getElementById('submit-btn').onclick = function() {
    const guess = document.getElementById('guess-input').value;
    fetch('/guess', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({guess: guess, coords: currentPlace.coords})
    })
    .then(res => res.json())
    .then(data => {
        if(data.error) {
            document.getElementById('result').innerText = data.error;
        } else {
            document.getElementById('result').innerText = `${data.message} (You were ${data.distance} km away)`;
            document.getElementById('next-btn').style.display = 'inline-block';
            document.getElementById('submit-btn').disabled = true;
        }
    });
};

document.getElementById('next-btn').onclick = function() {
    loadRandomPlace();
};

window.onload = loadRandomPlace;
