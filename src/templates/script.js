// Author: Lucas Tucker

document.getElementById('queryForm').addEventListener('submit', function(event) {
    document.getElementById('loader').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    event.preventDefault();
    var query = document.getElementById('query').value;
    fetch('http://localhost:8000', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'query=' + encodeURIComponent(query),
    })
    .then(response => {
        document.getElementById('loader').style.display = 'none'
        document.getElementById('result').style.display = 'block';
        return response.text()
    })
    .then(data => document.getElementById('result').innerText = data);
});
