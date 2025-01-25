document.getElementById('recommend-button').addEventListener('click', getRecommendations);
document.getElementById('swap-button').addEventListener('click', swapRecommendations);
document.getElementById('more-info-button').addEventListener('click', getMoreInfo);

let recommendations = [];
let inputSongNumber;

async function getRecommendations() {
    inputSongNumber = parseInt(document.getElementById('song-number').value);
    const response = await fetch('http://localhost:5000/api/recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ song_number: inputSongNumber })
    });
    recommendations = await response.json();
    displayRecommendations();
    getSongInfo();
}

async function getSongInfo() {
    const response = await fetch('http://localhost:5000/api/song_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ song_number: inputSongNumber })
    });
    const songInfo = await response.json();
    displaySongInfo(songInfo);
}

function displaySongInfo(songInfo) {
    const songInfoDiv = document.getElementById('song-info');
    songInfoDiv.innerHTML = `
        <p>Song: ${songInfo.song_name}</p>
        <p>Artist: ${songInfo.artist_name}</p>
        <p>Album: ${songInfo.album_name}</p>
        <p>Year of Release: ${songInfo.date}</p>
    `;
}

function displayRecommendations() {
    const recommendationsList = document.getElementById('recommendations-list');
    recommendationsList.innerHTML = '';
    recommendations.forEach((song, index) => {
        const songItem = document.createElement('li');
        songItem.innerHTML = `Day ${song.number}: ${song.song_name} by ${song.artist_name}`;
        recommendationsList.appendChild(songItem);
    });
}

function swapRecommendations() {
    if (recommendations.length >= 8) {
        [recommendations[6], recommendations[7]] = [recommendations[7], recommendations[6]];
        displayRecommendations();
    }
}

async function getMoreInfo() {
    const response = await fetch('http://localhost:5000/api/visualize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ song_number: inputSongNumber })
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    displayMoreInfo(url);
}

function displayMoreInfo(imageUrl) {
    const moreInfoDiv = document.getElementById('more-info');
    moreInfoDiv.innerHTML = `<img src="${imageUrl}" alt="Similarity Visualization">`;
}