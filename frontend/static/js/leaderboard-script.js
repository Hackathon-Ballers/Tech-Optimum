const json = fetch('https://google.com')
  .then(response => response.json())
  .then(data => console.log(data));