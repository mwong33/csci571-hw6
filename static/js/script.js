// Form Validation
const form = document.getElementById("form");
const clear = document.getElementById("clear");

const fromPrice = document.getElementById("from_price");
const toPrice = document.getElementById("to_price");

form.addEventListener("submit", (e) => {
    if ((fromPrice.value !== "" && toPrice.value !== "") && fromPrice.value > toPrice.value) {
        e.preventDefault();
        alert("Oops! Lower price limit cannot be greater than upper price limit! Please try again.");
    } else if (fromPrice.value < 0 || toPrice.value < 0) {
        e.preventDefault();
        alert("Price Range values cannot be negative! Please try a value greater than or equal to 0.0");
    }
})