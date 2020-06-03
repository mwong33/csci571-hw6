// Form Validation
const form = document.getElementById("form");
const clear = document.getElementById("clear");

const priceFrom = document.getElementById("price_from");
const priceTo = document.getElementById("price_to");

// Event Listener for 'Search' button
form.addEventListener("submit", (e) => {

    e.preventDefault(); 

    if ((priceFrom.value !== "" && priceTo.value !== "") && parseFloat(priceFrom.value) > parseFloat(priceTo.value)) {
        alert("Oops! Lower price limit cannot be greater than upper price limit! Please try again.");
    } else if (priceFrom.value < 0 || priceTo.value < 0) {
        alert("Price Range values cannot be negative! Please try a value greater than or equal to 0.0");
    } else {
        itemsJSON = getItems();
        createItemCard();
    }
})

// Function to execute GET request to our Python Flask server
function getItems() {

    // Get Form Data
    var keywords = document.getElementById("key_words").value;

    var request_url = "/items?keywords=" + keywords;

    if (document.getElementById("price_from").value != "") {
        request_url += "&price_from=" + document.getElementById("price_from").value;
    }

    if (document.getElementById("price_to").value != "") {
        request_url += "&price_to=" + document.getElementById("price_to").value;
    }

    if (document.getElementById("new").checked == true) {
        request_url += "&new=" + document.getElementById("new").value;
    }

    if (document.getElementById("used").checked == true) {
        request_url += "&used=" + document.getElementById("used").value;
    }

    if (document.getElementById("very_good").checked == true) {
        request_url += "&very_good=" + document.getElementById("very_good").value;
    }

    if (document.getElementById("good").checked == true) {
        request_url += "&good=" + document.getElementById("good").value;
    }

    if (document.getElementById("acceptable").checked == true) {
        request_url += "&acceptable=" + document.getElementById("acceptable").value;
    }

    if (document.getElementById("return_accepted").checked == true) {
        request_url += "&return_accepted=" + document.getElementById("return_accepted").value;
    }

    if (document.getElementById("free_shipping").checked == true) {
        request_url += "&free_shipping=" + document.getElementById("free_shipping").value;
    }

    if (document.getElementById("expedited_shipping").checked == true) {
        request_url += "&expedited_shipping=" + document.getElementById("expedited_shipping").value;
    }
    
    request_url += "&sort_by=" + document.getElementById("sort_by").value;
    
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhttp.responseText);
            return JSON.parse(xhttp.responseText);
        }

        if (this.status == 404) {
            console.log("File or resource not found!");
        }
    };

    xhttp.open("GET", request_url, true);
    xhttp.send();
}

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