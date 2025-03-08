document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete").forEach(button => {
        button.addEventListener("click", function () {
            let dateId = this.dataset.id;  // Get the correct ID
            
            if (!dateId) {
                console.error("Error: Date ID is missing!");
                return;
            }
            
            if (confirm("Are you sure you want to delete this item?")) {
                fetch(`/adminpage/deletedate/${dateId}/`, {  
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => { throw new Error(text); });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Remove the deleted item from the DOM
                        let buttonElement = document.querySelector(`[data-id='${dateId}']`);
                        if (buttonElement) {
                            buttonElement.closest(".rect1").remove();
                            location.reload();
                        }
                    } else {
                        alert("Error: " + data.error);
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("An error occurred. Check the console for details.");
                });
                
            }
        });
    });
});

// Function to get CSRF token
function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split("; ");
    cookies.forEach(cookie => {
        let [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            cookieValue = value;
        }
    });
    return cookieValue;
}


//for showing month

document.addEventListener("DOMContentLoaded", function () {
    flatpickr("#monthPicker", {
        dateFormat: "F Y", // Show "Mart 2025"
        locale: "uz", // Set language to Uzbek
        disableMobile: "true", // Ensures consistent behavior across devices
        plugins: [
            new monthSelectPlugin({
                shorthand: true, // Use short month names if preferred
                dateFormat: "F Y", // Show month name and year
                altFormat: "F Y", // Alternative format for display
                theme: "light" // Light theme for better visibility
            })
        ]
    });
});





document.addEventListener("DOMContentLoaded", function () {
    const monthPicker = document.getElementById("monthPicker");
    const productNameInput = document.querySelector("input[name='product_name']");
    const copyDateSelect = document.querySelector("select[name='copydate_data']");
    const saveButton = document.querySelector("button[name='save-button1']");

    // Define month mapping in Uzbek
    const monthMapping = {
        "Январ": "01", "Феврал": "02", "Март": "03", "Апрел": "04",
        "Май": "05", "Июн": "06", "Июл": "07", "Август": "08",
        "Сентябр": "09", "Октябр": "10", "Ноябр": "11", "Декабр": "12"
    };

    saveButton.addEventListener("click", function () {
        let dateInput = monthPicker.value.trim();
        let productName = productNameInput.value || null;
        let copyValueId = copyDateSelect.value || null; // Default to None if not selected

        // Validate product name
        

        // Validate month input
        if (!dateInput) {
            showFlashMessage("Илтимос, ойни танланг!", "danger");
            return;
        }

        let parts = dateInput.split(" ");
        if (parts.length !== 2) {
            showFlashMessage("Хатолик: Сана нотўғри форматда!", "danger");
            return;
        }

        let monthName = parts[0]; // Example: Феврал
        let year = parts[1]; // Example: 2025
        let month = monthMapping[monthName];

        if (!month) {
            showFlashMessage("Хатолик: Ой нотўғри форматда!", "danger");
            return;
        }

        sendDataToBackend(year, month, copyValueId, productName);
    });

    function sendDataToBackend(year, month, copyValueId, productName) {
        fetch("/adminpage/createdate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                year: parseInt(year, 10),
                month: parseInt(month, 10),
                copy_value_id: copyValueId,  // Can be null
                productname: productName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.succes) {
                showFlashMessage("Сана муваффақиятли сақланди!", "success");
            } else {
                showFlashMessage("Хатолик: " + data.error, "danger");
            }
        })
        .catch(error => showFlashMessage("Хатолик юз берди: " + error, "danger"));
    }

    function getCSRFToken() {
        let cookieValue = null;
        document.cookie.split(";").forEach(cookie => {
            let trimmedCookie = cookie.trim();
            if (trimmedCookie.startsWith("csrftoken=")) {
                cookieValue = trimmedCookie.substring("csrftoken=".length, trimmedCookie.length);
            }
        });
        return cookieValue;
    }

    function showFlashMessage(message, type) {
        const flashContainer = document.getElementById("flash-messages");
        const flashMessage = document.createElement("div");
        flashMessage.className = `flash-message ${type}`;
        flashMessage.innerText = message;
        
        flashContainer.appendChild(flashMessage);

        setTimeout(() => {
            flashMessage.remove();
            location.reload();
        }, 1); // Remove after 5 seconds
    }
});
