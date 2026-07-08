document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const loading = document.getElementById("loading");
    const button = document.querySelector("button");

    form.addEventListener("submit", function () {

        loading.style.display = "block";

        button.disabled = true;

        button.innerHTML = "Processing...";

    });

});