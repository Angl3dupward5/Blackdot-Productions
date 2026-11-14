document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.querySelector(".nav-toggle");
    const navigation = document.querySelector(".nav-links");

    if (!toggle || !navigation) {
        return;
    }

    // Open and close the mobile navigation
    toggle.addEventListener("click", function () {

        const isOpen = navigation.classList.toggle("is-open");

        toggle.setAttribute("aria-expanded", isOpen);

        toggle.textContent = isOpen ? "✕" : "☰";

    });

    // Close menu when a navigation link is selected
    navigation.querySelectorAll("a").forEach(function (link) {

        link.addEventListener("click", function () {

            navigation.classList.remove("is-open");

            toggle.setAttribute("aria-expanded", "false");

            toggle.textContent = "☰";

        });

    });

    // Close menu when Escape is pressed
    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            navigation.classList.remove("is-open");

            toggle.setAttribute("aria-expanded", "false");

            toggle.textContent = "☰";

        }

    });

});