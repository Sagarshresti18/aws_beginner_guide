function submitData() {
    const name = document.getElementById("userName").value;
    const number = document.getElementById("userNumber").value;
    const photoInput = document.getElementById("userPhoto");
    const responseText = document.getElementById("response");

    // Validation
    if (name.trim() === "") {
        responseText.innerText = "Please enter your name!";
        responseText.style.color = "red";
        return;
    }

    if (number.trim() === "") {
        responseText.innerText = "Please enter a number!";
        responseText.style.color = "red";
        return;
    }

    // Check if photo is selected
    if (photoInput.files.length === 0) {
        responseText.innerText = "Please upload a photo!";
        responseText.style.color = "red";
        return;
    }

    const file = photoInput.files[0];

    // Convert image to Base64
    const reader = new FileReader();
    reader.onload = function(e) {
        const base64Image = e.target.result;

        // Send data to backend
        fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_name: name,
                user_number: number,
                user_photo: base64Image
            })
        })
        .then(response => response.json())
        .then(data => {
            responseText.innerText = data.message;
            responseText.style.color = "lightgreen";
            
            // Clear inputs
            document.getElementById("userName").value = "";
            document.getElementById("userNumber").value = "";
            document.getElementById("userPhoto").value = "";
        })
        .catch(error => {
            responseText.innerText = "Error storing data!";
            responseText.style.color = "red";
            console.error(error);
        });
    };

    reader.readAsDataURL(file);
}