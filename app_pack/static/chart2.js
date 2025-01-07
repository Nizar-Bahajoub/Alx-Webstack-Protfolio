document.body.addEventListener('click', function(event) {
    var dropdown = document.getElementById("dropdownContent");
    var user = document.querySelector(".user");

    // Check if the clicked element is not the user element or the dropdown content
    if (!user.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = "none"; // Close the dropdown
    }
});

function toggleDropdown() {
    var dropdown = document.getElementById("dropdownContent");
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
}