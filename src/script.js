document.getElementById('queryForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var query = document.getElementById('query').value;
    fetch('http://localhost:8000', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'query=' + encodeURIComponent(query),
    })
    .then(response => response.json())
    .then(data => document.getElementById('result').innerText = data.result);
});

// document.getElementById('window').addEventListener('click', async _ => {
//     try {
//         fetch('http://localhost:8000', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({type: "window", data: "window"})
//         });
//     } catch(err) {
//         console.error('Error on window button')
//     }
// });

// document.getElementById('automerging').addEventListener('click', async _ => {
//     try {
//         fetch('http://localhost:8000', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({type: "automerging", data: "automerging"})
//         });
//     } catch(err) {
//         console.error('Error on window button')
//     }
// });