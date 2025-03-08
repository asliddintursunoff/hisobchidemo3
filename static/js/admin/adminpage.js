document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("td").forEach(td => {
        let span = td.querySelector(".number-display");
        if (span) {
            td.addEventListener("click", function (event) {
                if (event.detail === 2) { // Фақат икки марта босганда очиш
                    editNumber(this);
                }
            });
        }
    });
});

function editNumber(td) {
    let span = td.querySelector(".number-display");
    let form = td.querySelector(".edit-form");

    if (form) {
        closeAllForms();
        span.style.display = "none";
        form.style.display = "block";

        let input = form.querySelector("input");
        input.focus();
        input.select();
    }
}

// ✅ Бошқа ҳужжатларга босилганда формани ёпиш
document.addEventListener("click", function (event) {
    if (!event.target.closest("td")) {
        closeAllForms();
    }
});

function getCSRFToken() {
    return document.querySelector("meta[name='csrf-token']").getAttribute("content");
}

function closeAllForms() {
    document.querySelectorAll(".edit-form").forEach(form => {
        let td = form.closest("td");
        let span = td.querySelector(".number-display");

        form.style.display = "none";
        span.style.display = "block";
    });
}

function submitForm(event, form, progressId) {
    event.preventDefault(); // Reload'ни олдини олиш

    let input = form.querySelector("input[type='number']");
    let newValue = input.value.trim();
    let year2 = document.getElementById("year2").value;
    let month2 = document.getElementById("month2").value;

    if (!/^\d+$/.test(newValue)) {
        showFlashMessage("❌ Илтимос, тўғри сон киритинг!", "error");
        return;
    }

    fetch("/update-progress-item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            progress_id: progressId,
            progress_value: parseInt(newValue),
            year2 : year2,
            month2 : month2,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let td = form.closest("td");
            let span = td.querySelector(".number-display");

            span.textContent = data.new_value;
            form.style.display = "none";
            span.style.display = "block";
            showFlashMessage("✅ Маълумот сақланди!", "success");
        } else {
            showFlashMessage("❌ Хатолик: " + data.error, "error");
        }
    })
    .catch(error => console.error("Fetch Error:", error));
}

function validateInteger(input) {
    input.value = input.value.replace(/[^0-9]/g, ""); // Фақат сонларга рухсат бериш
}

// ✅ Флеш хабарни кўрсатиш функцияси
function showFlashMessage(message, type) {
    let flashMessage = document.getElementById("flash-message");
    if (!flashMessage) return;

    flashMessage.textContent = message;
    flashMessage.style.display = "block";
    flashMessage.style.backgroundColor = type === "success" ? "green" : "red";
    flashMessage.style.color = "white";

    setTimeout(() => {
        flashMessage.style.display = "none";
        //for reloading
        location.reload();
        //for reloading
    }, 1500);
}




document.getElementById("save-btn").addEventListener("click", function(event) {
    event.preventDefault();  // Prevent form submission

    let workName = document.getElementById("work-name").value;
    let workPrice = document.getElementById("work-price").value;
    let productType = document.getElementById("mahsulot_turi1").value;

    // Validate input
    if (!workName || !workPrice) {
        showFlashMessage("Илтимос, барча майдонларни тўлдиринг!", "error");
        return;
    }

    fetch("/adminpage/addworker/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            work_name: workName,
            price: parseInt(workPrice),
            types: productType,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showFlashMessage("Иш муваффақиятли қўшилди!", "success");
            document.getElementById("work-name").value = "";
            document.getElementById("work-price").value = "";
            document.getElementById("mahsulot_turi1").value;
        } else {
            showFlashMessage("Хатолик: " + data.error, "error");
        }
    })
    .catch(error => console.error("Error:", error));
});

// Function to show flash messages
function showFlashMessage(message, type) {
    let flashMessage = document.getElementById("flash-message");
    flashMessage.innerText = message;
    flashMessage.style.display = "block";
    flashMessage.style.color = "#fff";
    flashMessage.style.padding = "10px";
    flashMessage.style.marginTop = "10px";
    flashMessage.style.borderRadius = "5px";
    
    if (type === "success") {
        flashMessage.style.backgroundColor = "green";
    } else {
        flashMessage.style.backgroundColor = "red";
    }

    setTimeout(() => {
        flashMessage.style.display = "none";
        //for reloading
        location.reload();
        //for reloading
    },1);  // Hide after 3 seconds
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length, cookie.length);
            break;
        }
    }
    return cookieValue;
}






//for ADDING WORKER

document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL
    let currentUrl = window.location.href;

    // Get all buttons
    let buttons = document.querySelectorAll(".btn-link .btn");

    buttons.forEach((button) => {
        let btnLink = button.parentElement.href; // Get <a> link

        // If the button link matches the current URL, add active class
        if (currentUrl === btnLink) {
            button.classList.add("active");
        }
    });
});

$(document).ready(function () {
    // Function to show flash messages
    function showFlashMessage(message, type = "success") {
        let flashDiv = $("#flash-message");
        flashDiv.html(message).removeClass().addClass("flash-message " + type).fadeIn();

        setTimeout(function () {
            flashDiv.fadeOut();
        }, 3000);
    }

    // Handle form submission using AJAX
    $("#worker-form").submit(function (e) {
        e.preventDefault(); // Prevent default form submission

        let formData = $(this).serializeArray(); // Serialize form data

        $.ajax({
            type: "POST",
            url: workerFormUrl, // Use a global variable set in the template
            data: formData,
            success: function (response) {
                showFlashMessage("Ишчи ва Прогресс муваффақиятли яратилди!", "success");
                setTimeout(function () {
                    location.reload();
                }, 100);
            },
            error: function (xhr, status, error) {
                showFlashMessage("Хатолик юз берди: " + xhr.responseText, "error");
            }
        });
    });
});






$(document).ready(function () {
    // Function to show flash messages
    function showFlashMessage(message, type = "success") {
        let flashDiv = $("#flash-message");
        flashDiv.html(message).removeClass().addClass("flash-message " + type).fadeIn();
        setTimeout(function () {
            flashDiv.fadeOut();
        }, 3000);
    }

    // Open modal when clicking "Ishchi qo'shish"
    $(".adder").click(function () {
        console.log("Opening modal...");
        $("#modal-add-items").fadeIn();
    });

    // Close modal when clicking "X"
    $("#close-add-items").click(function () {
        console.log("Closing modal...");
        $("#modal-add-items").fadeOut();
    });

    // Handle form submission via AJAX
    $("#form-add-item").submit(function (event) {
        event.preventDefault();  

        console.log("Submitting form via AJAX...");
        
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        let url = $("#btn-save-item").data("url");  
        let selectedOption = $("#select-item-type").find("option:selected");

        let formData = {
            type_date: $("#hidden-item-date").val(),
            type_name: $("#input-item-name").val(),
            type_id: selectedOption.val() || "None", // If not selected, send "None"
        };

        // Validation
        if (!formData.type_name) {
            showFlashMessage("Барча майдонларни тўлдиринг!", "error");
            return;
        }

        $.ajax({
            type: "POST",
            url: url,
            headers: { "X-CSRFToken": csrfToken },
            data: JSON.stringify(formData),
            contentType: "application/json",
            success: function (response) {
              
                showFlashMessage("Янги ишчи муваффақиятли қўшилди!", "success");
                $("#modal-add-items").fadeOut();
                setTimeout(function () {
                    location.reload();
                }, 1500);
            },
            error: function (xhr) {
                console.log("❌ AJAX Error:", xhr.responseText);
                showFlashMessage("Хатолик юз берди: " + xhr.responseText, "error");
            },
        });
    });
});










//for adding multipe workers
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal-add-worker2"); // Modal element
    const openBtn = document.querySelector(".adderworker"); // Button to open modal
    const closeBtn = document.getElementById("close-add-worker2"); // Close button
    const form = document.getElementById("form-add-worker2"); // Form element
    const flashDiv = document.createElement("div"); // Flash message container

    // Ensure modal is hidden on page load
    modal.style.display = "none";

    // Flash message styling
    flashDiv.style.position = "fixed";
    flashDiv.style.top = "20px";
    flashDiv.style.left = "50%";
    flashDiv.style.transform = "translateX(-50%)";
    flashDiv.style.padding = "10px 20px";
    flashDiv.style.borderRadius = "5px";
    flashDiv.style.display = "none";
    flashDiv.style.zIndex = "1001";
    document.body.appendChild(flashDiv);

    // Function to show flash message
    function showFlashMessage(message, type = "success") {
        flashDiv.innerHTML = message;
        flashDiv.style.backgroundColor = type === "success" ? "green" : "red";
        flashDiv.style.color = "white";
        flashDiv.style.display = "block";

        setTimeout(() => {
            flashDiv.style.display = "none";
        }, 3000);
    }

    // Open modal when clicking the button
    openBtn.addEventListener("click", function () {
        modal.style.display = "flex";
    });

    // Close modal when clicking the close button
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Close modal when clicking outside the modal content
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Handle form submission to send JSON data
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent normal form submission

        // Get the worker type (t.id) from hidden input
        let workerType = document.getElementById("hidden-worker2-date").value;
        // Get all checkboxes within the worker-checkboxes div
        let checkboxes = document.querySelectorAll("#worker-checkboxes input[type='checkbox']");
        let workersArray = [];

        // Create an array of objects: {worker_id: number, status: boolean}
        checkboxes.forEach(checkbox => {
            workersArray.push({
                "worker_id": parseInt(checkbox.value),
                "status": checkbox.checked
            });
        });

        // Build the JSON payload
        let payload = {
            "worker2_type": workerType,
            "workers": workersArray
        };

        // Get the backend URL from the data-url attribute of the save button
        let url = document.getElementById("btn-save-worker2").getAttribute("data-url");

        fetch(url, {
            method: "POST",
            body: JSON.stringify(payload),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showFlashMessage("Ishchilar muvaffaqiyatli saqlandi!", "success");
                modal.style.display = "none"; // Close modal after success
                form.reset(); // Clear form fields
                setTimeout(function () {
                    location.reload();
                }, 1500);
            } else {
                showFlashMessage("Xatolik yuz berdi!", "error");
            }
        })
        .catch(error => {
            showFlashMessage("Server bilan aloqa yo‘q!", "error");
        });
    });
});
