// Helper: Get CSRF token from meta tag.
function getCSRFToken() {
    var meta = document.querySelector("meta[name='csrf-token']");
    return meta ? meta.getAttribute("content") : "";
}

// Helper: Validate that an input contains only digits.
function validateInteger(input) {
    input.value = input.value.replace(/[^0-9]/g, "");
}

document.addEventListener("DOMContentLoaded", function () {
    // Attach click event on each "change" button.
    document.querySelectorAll("button.change").forEach(function (button) {
        button.addEventListener("click", function (e) {
            var row = e.target.closest("tr");
            if (!row || row.classList.contains("editing")) return;
            row.classList.add("editing");

            // Get the cells that will be edited.
            var numberCell = row.querySelector(".number-cell");
            var dateCell = row.querySelector(".date-cell");
            var buttonsCell = row.querySelector(".profile-buttons");

            // Retrieve current values.
            var currentNumber = numberCell.textContent.trim();
            // Use the ISO date from a data attribute; fallback to the cell text if not set.
            var currentDateISO = dateCell.getAttribute("data-iso") || dateCell.textContent.trim();

            // Replace number cell content with an input field.
            var numberInput = document.createElement("input");
            numberInput.type = "number";
            numberInput.name = "progress_value";
            numberInput.className = "inputs";
            numberInput.value = currentNumber;
            numberInput.min = "0";
            numberInput.step = "1";
            numberInput.setAttribute("oninput", "validateInteger(this)");
            numberCell.innerHTML = "";
            numberCell.appendChild(numberInput);

            // Replace date cell content with a datetime-local input.
            var dateInput = document.createElement("input");
            dateInput.type = "datetime-local";
            dateInput.name = "progress_date";
            dateInput.value = currentDateISO; // Must be in ISO format: YYYY-MM-DDTHH:MM
            dateCell.innerHTML = "";
            dateCell.appendChild(dateInput);

            // Replace the buttons cell with a single "Save" button.
            buttonsCell.innerHTML = "";
            var saveButton = document.createElement("button");
            saveButton.type = "button";
            saveButton.className = "save-btn";
            saveButton.textContent = "Save";
            buttonsCell.appendChild(saveButton);

            // Save button click event.
            saveButton.addEventListener("click", function () {
                var newNumber = parseInt(numberInput.value);
                var newDateISO = dateInput.value;  // ISO formatted date from the input.
                var progressId = row.id.split("-")[1];

                fetch("/history/change/" + progressId + "/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    body: JSON.stringify({
                        number: newNumber,
                        date: newDateISO
                    })
                })
                .then(function (response) {
                    if (!response.ok) {
                        return response.text().then(function (text) { throw new Error(text); });
                    }
                    return response.json();
                })
                .then(function (data) {
                    if (data.success) {
                        // Update cells with the new values.
                        numberCell.textContent = data.new_value;
                        dateCell.textContent = data.new_date; // e.g., "H:i d/m/Y" formatted.
                        // Also update the data-iso attribute with the ISO date.
                        dateCell.setAttribute("data-iso", newDateISO);

                        // Restore the original buttons using global variables for the icon URLs.
                        buttonsCell.innerHTML = `
                            <button type="button" class="change" title="O'zgartirish">
                                <img src="${editIconUrl}" alt="O'zgartirish">
                            </button>
                            <button onclick="deleteProgress(${progressId})" type="button" class="delete" title="Royhatdan o'chirish">
                                <img src="${deleteIconUrl}" alt="Royhatdan o'chirish">
                            </button>
                        `;
                        // Rebind the change event on the new change button if needed.
                        buttonsCell.querySelector("button.change").addEventListener("click", function(e) {
                            // Optionally call the same function or reload the row for editing.
                        });
                        row.classList.remove("editing");
                    } else {
                        alert("Error: " + data.error);
                    }
                })
                .catch(function (error) {
                    console.error("Error updating progress:", error);
                    alert("Error updating progress. Check console for details.");
                });
            });
        });
    });
});

function deleteProgress(progressId) {
    if (confirm("Are you sure you want to delete this progress?")) {
        fetch(`/history/${progressId}/`, {  // URL: /history/id/
            method: "DELETE",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFToken()
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Remove the corresponding table row from the DOM
                const row = document.getElementById(`progress-${progressId}`);
                if (row) {
                    row.remove();
                }
            } else {
                alert("Error deleting progress: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error deleting progress:", error);
            alert("Error deleting progress. Check console for details.");
        });
    }
}