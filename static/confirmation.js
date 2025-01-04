document.addEventListener("DOMContentLoaded", () => {
    const deleteForms = document.querySelectorAll(".delete-form");
    deleteForms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            const confirmation = confirm("Are you sure you want to delete this application?");
            if (!confirmation) {
                event.preventDefault(); // Prevent form submission
            }
        });
    });
});
