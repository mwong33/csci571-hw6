// Form Validation
const form = document.getElementById("form");
const clear = document.getElementById("clear");

const fromPrice = document.getElementById("from_price");
const toPrice = document.getElementById("to_price");

// Event Listener for 'Search' button
form.addEventListener("submit", (e) => {

    e.preventDefault(); 

    if ((fromPrice.value !== "" && toPrice.value !== "") && fromPrice.value > toPrice.value) {
        alert("Oops! Lower price limit cannot be greater than upper price limit! Please try again.");
    } else if (fromPrice.value < 0 || toPrice.value < 0) {
        alert("Price Range values cannot be negative! Please try a value greater than or equal to 0.0");
    }

    createItemCard();
})

// Function to create an item card
function createItemCard() {

    var cardDiv = document.createElement("div");
    cardDiv.setAttribute("class", "card");
    document.body.appendChild(cardDiv);

    var title = document.createElement("p");
    title.innerHTML = "Title";
    cardDiv.appendChild(title);
    
    var condition = document.createElement("p");
    condition.innerHTML = "Condition:";
    cardDiv.appendChild(condition);

    var price = document.createElement("p");
    price.innerHTML = "Price:";
    cardDiv.appendChild(price);

}