let isLoading = true;

// Show the loading message
document.getElementById("loading-message").style.display = "block";

// Send the request to the backend
fetch('/lucky')
    .then(response => response.json())
    .then(data => {
        isLoading = false;
        // Hide the loading message
        document.getElementById("loading-message").style.display = "none";
        document.getElementById("loading-message").classList.remove("loading-animation");

        // Display the result
        // document.getElementById("result").style.display = "block";
        document.getElementById("result").innerHTML = data.lucky_number ;
    });

const loadingMessage = document.getElementById("loading-message");
let dots = 0;
setInterval(() => {
    if(isLoading) {
    dots = (dots + 1) % 4;
    loadingMessage.innerText = `Polling${'.'.repeat(dots)}`;
    }
}, 1000);