document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-dark");
    toggleButton.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        // Optional: Save preference in localStorage
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });

    // Load preference on startup
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
    }
});
