function getCSRFToken() {
    let cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        let [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return ""; // Return empty string if CSRF token is not found
}
    function deleteWorker(workerId) {
    if (confirm("Aniq bu ishchini o'chirmoqchimisz?")) {
        fetch(`/showworkers/delete/${workerId}/`, {
            method: "DELETE",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFToken()  // CSRF protection
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) }); // 🔍 Handle errors
            }
            return response.json(); // ✅ Parse JSON response
        })
        .then(data => {
            console.log("Server Response:", data); // 🔍 Debugging
            if (data.success) {
                document.getElementById(`worker-${workerId}`).remove();
            } else {
                console.log("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
           
        });
    }
}




document.addEventListener("DOMContentLoaded", function () {
    // ✅ Worker Modal
    const workerModal = document.getElementById("modal-add-workers");
    const openWorkerBtn = document.querySelector(".adder");
    const closeWorkerBtn = document.getElementById("close-add-items");
    const workerForm = document.getElementById("form-add-worker");
    const workerSaveBtn = document.getElementById("btn-save-worker");

    // ✅ Expense Modal
    const expenseModal = document.getElementById("modal-add-expanse-worker");
    const openExpenseBtn = document.querySelector(".expanseadder");
    const closeExpenseBtn = document.getElementById("close-add-expanse");
    const expenseForm = document.getElementById("form-add-expanse-worker"); 
    const expenseSaveBtn = document.getElementById("btn-save-expanse-worker");

    // ✅ Ensure modals are hidden on page load
    if (workerModal) workerModal.style.display = "none";
    if (expenseModal) expenseModal.style.display = "none";

    // ✅ Show Worker Modal
    if (openWorkerBtn) {
        openWorkerBtn.addEventListener("click", function () {
            workerModal.style.display = "flex";
        });
    }

    // ✅ Close Worker Modal
    if (closeWorkerBtn) {
        closeWorkerBtn.addEventListener("click", function () {
            workerModal.style.display = "none";
        });
    }

    // ✅ Show Expense Modal
    if (openExpenseBtn) {
        openExpenseBtn.addEventListener("click", function () {
            expenseModal.style.display = "flex";
        });
    }

    // ✅ Close Expense Modal
    if (closeExpenseBtn) {
        closeExpenseBtn.addEventListener("click", function () {
            expenseModal.style.display = "none";
        });
    }

    // ✅ Close modals when clicking outside
    window.addEventListener("click", function (event) {
        if (event.target === workerModal) {
            workerModal.style.display = "none";
        }
        if (event.target === expenseModal) {
            expenseModal.style.display = "none";
        }
    });

    // ✅ Submit Worker Form
    if (workerForm && workerSaveBtn) {
        workerForm.addEventListener("submit", function (event) {
            event.preventDefault();
            let formData = new FormData(workerForm);
            let url = workerSaveBtn.getAttribute("data-url");

            if (!url) {
                console.log("Worker URL is missing! Check your Django template.");
                return;
            }

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Ishchi muvaffaqiyatli qo‘shildi!");
                    workerModal.style.display = "none";
                    workerForm.reset();
                    location.reload(); // Refresh the page
                } else {
                    console.log("Xatolik: " + data.error);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                console.log("Server bilan aloqa yo‘q!");
            });
        });
    }

    // ✅ Submit Expense Form
    if (expenseForm && expenseSaveBtn) {
        expenseForm.addEventListener("submit", function (event) {
            event.preventDefault();
            let formData = new FormData(expenseForm);
            let url = expenseSaveBtn.getAttribute("data-url");

            if (!url) {
                console.log("Expense URL is missing! Check your Django template.");
                return;
            }

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Harajat muvaffaqiyatli qo‘shildi!");
                    expenseModal.style.display = "none";
                    expenseForm.reset();
                    location.reload(); // Refresh the page
                } else {
                    console.log("Xatolik: " + data.error);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                console.log("Server bilan aloqa yo‘q!");
            });
        });
    }
});



document.addEventListener("DOMContentLoaded", function () {
    let modal = document.getElementById("modal-update-expanse");
    let expanseInput = document.querySelector("#form-update-expanse input[name='value-expanse']");
    let form = document.getElementById("form-update-expanse");

    // 🔹 Ensure modal is hidden initially
    modal.style.display = "none";

    // ✅ Open modal when clicking <td>
    document.querySelectorAll("td[data-worker-id]").forEach(td => {
        td.addEventListener("click", function () {
            let workerId = this.getAttribute("data-worker-id");
            let currentCost = this.textContent.trim();

            // ✅ Fill input field with current value
            expanseInput.value = currentCost;

            // ✅ Store worker ID in form (for submission)
            form.setAttribute("data-worker-id", workerId);

            // ✅ Open modal
            modal.style.display = "flex";
        });
    });

    // ✅ Prevent form submission from refreshing the page
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // ❌ Stops default page refresh

        let workerId = form.getAttribute("data-worker-id"); // Get worker ID
        let newExpanseValue = parseInt(expanseInput.value); // Get new value

        // ✅ Send data to backend via AJAX
        fetch(form.getAttribute("data-url"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),  // CSRF token for security
            },
            body: JSON.stringify({
                worker_id: workerId,
                new_expanse_value: newExpanseValue,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);

            // ✅ Close modal after saving
            modal.style.display = "none";

            // ✅ Update the <td> with the new value
            document.querySelector(`td[data-worker-id="${workerId}"]`).textContent = newExpanseValue;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    // ✅ Function to get CSRF token
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    // ✅ Close modal when clicking the close button
    document.getElementById("close-update-item").addEventListener("click", function () {
        modal.style.display = "none";
    });

    // ✅ Close modal when clicking outside the modal content
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});










document.addEventListener("DOMContentLoaded", function () {
    let modal = document.getElementById("modal-update-expanse-name");
    let expanseInput = document.querySelector("#form-update-expanse-name input[name='value-expanse-name']");
    let formUpdate = document.getElementById("form-update-expanse-name");
    let formDelete = document.getElementById("form-delete-expanse-name");
    let deleteBtn = document.getElementById("btn-delete-expanse-name");

    // 🔹 Hide modal initially
    modal.style.display = "none";

    // ✅ Open modal when clicking <th>
    document.querySelectorAll("th[data-expansing-id]").forEach(th => {
        th.addEventListener("click", function () {
            let expanseId = this.getAttribute("data-expansing-id");
            let currentCost = this.textContent.trim();

            // ✅ Fill input field with current value
            expanseInput.value = currentCost;

            // ✅ Store expanse ID in forms
            formUpdate.setAttribute("data-expanse-id", expanseId);
            formDelete.setAttribute("data-expanse-id", expanseId);

            // ✅ Open modal
            modal.style.display = "flex";
        });
    });

    // ✅ Handle Update (Save)
    formUpdate.addEventListener("submit", function (event) {
        event.preventDefault(); // ❌ Prevent page reload

        let expanseId = formUpdate.getAttribute("data-expanse-id");
        let newExpanseValue = expanseInput.value;

        fetch(formUpdate.getAttribute("data-url"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                expanse_id: expanseId,
                new_expanse_value: newExpanseValue,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);

            // ✅ Update the table without reload
            document.querySelector(`th[data-expansing-id="${expanseId}"]`).textContent = newExpanseValue;

            // ✅ Close modal
            modal.style.display = "none";
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    // ✅ Handle Delete
    formDelete.addEventListener("submit", function (event) {
        event.preventDefault();

        let expanseId = formDelete.getAttribute("data-expanse-id");
        let deleteUrl = formDelete.getAttribute("data-url");

        if (!expanseId) {
            alert("Hech qanday harajat tanlanmagan!");
            return;
        }

        if (!confirm("Haqiqatan ham o'chirmoqchimisiz?")) {
            return;
        }

        fetch(deleteUrl, {
            method: "POST", // Change to DELETE if needed
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ expanse_id: expanseId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // ✅ Remove item from UI
                document.querySelector(`th[data-expansing-id="${expanseId}"]`).remove();

                // ✅ Close modal
                modal.style.display = "none";

                // ❗ Reload (optional, only if needed)
                location.reload();
            } else {
                alert("O'chirishda xatolik yuz berdi!");
            }
        })
        .catch(error => console.error("Error deleting:", error));
    });

    // ✅ CSRF Token Function
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    // ✅ Close modal when clicking the close button
    document.getElementById("close-update-item-name").addEventListener("click", function () {
        modal.style.display = "none";
    });

    // ✅ Close modal when clicking outside the modal content
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});


document.getElementById("search-input").addEventListener("keyup", function () {
    let searchQuery = this.value.toLowerCase();
    let rows = document.querySelectorAll("#table-body tr");

    rows.forEach(row => {
        let rowText = row.textContent.toLowerCase();
        row.style.display = rowText.includes(searchQuery) ? "" : "none";
    });
});