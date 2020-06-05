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
        const items = () => {
            getItems().then(itemsJSON => {                
                // Display the result count
                displayResultCount(parseInt(itemsJSON.totalResults));

                if (parseInt(itemsJSON.totalResults) != 0) {

                    // Loop through each item and create the card for each item
                    let itemNumber = 0;

                    let cardHolder = document.createElement("div");
                    cardHolder.setAttribute("id", "card_holder");

                    for (let item in itemsJSON) {
                        if (itemNumber < 10) {
                            createItemCard(cardHolder, itemsJSON[item], itemNumber);
                        }

                        itemNumber += 1;
                    }

                    document.body.appendChild(cardHolder);

                    // Create Event Listener for each Card
                    const cardArray = Array.prototype.slice.call(document.querySelectorAll('.card'));

                    cardArray.forEach((card) => {
                        card.addEventListener('click', () => {
                            let details = Array.prototype.slice.call(card.getElementsByClassName("extra_detail"));

                            for (let  i in details) {
                                details[i].classList.remove('hidden');
                            };
                        });
                    });

                    // Create Event Listener for the Close Buttons
                    cardArray.forEach((card) => {
                        document.getElementById(card.id + "_close_button").addEventListener('click', (e) => {
                            e.stopPropagation();
                            let details = Array.prototype.slice.call(card.getElementsByClassName("extra_detail"));
                            for (let  i in details) {
                                details[i].classList.add('hidden');
                            };
                        });
                    });

                };
            });
        };

        // Before we get our items, check to clear out any initial search results (result_count, result_count_empty, and card_holder)
        if (document.getElementById("result_count_empty") != null) {
            document.body.removeChild(document.getElementById("result_count_empty"));
        }

        if (document.getElementById("result_count") != null) {
            document.body.removeChild(document.getElementById("result_count"));
        }

        if (document.getElementById("card_holder") != null) {
            document.body.removeChild(document.getElementById("card_holder"));
        }

        items();
    };
});

// Event listener for 'Clear' button
clear.addEventListener("click", () => {
    
    // Clear Button must also clear out the result area if present
    if (document.getElementById("result_count_empty") != null) {
        document.body.removeChild(document.getElementById("result_count_empty"));
    }

    if (document.getElementById("result_count") != null) {
        document.body.removeChild(document.getElementById("result_count"));
    }

    if (document.getElementById("card_holder") != null) {
        document.body.removeChild(document.getElementById("card_holder"));
    }

})

// Function to execute GET request to our Python Flask server
function getItems() {

    const promise = new Promise((resolve, reject) => {
        // Get Form Data
        let keywords = document.getElementById("key_words").value;

        let request_url = "/items?keywords=" + keywords;

        if (document.getElementById("price_from").value != "") {
            request_url += "&price_from=" + document.getElementById("price_from").value;
        };

        if (document.getElementById("price_to").value != "") {
            request_url += "&price_to=" + document.getElementById("price_to").value;
        };

        if (document.getElementById("new").checked == true) {
            request_url += "&new=" + document.getElementById("new").value;
        };

        if (document.getElementById("used").checked == true) {
            request_url += "&used=" + document.getElementById("used").value;
        };

        if (document.getElementById("very_good").checked == true) {
            request_url += "&very_good=" + document.getElementById("very_good").value;
        };

        if (document.getElementById("good").checked == true) {
            request_url += "&good=" + document.getElementById("good").value;
        };

        if (document.getElementById("acceptable").checked == true) {
            request_url += "&acceptable=" + document.getElementById("acceptable").value;
        };

        if (document.getElementById("return_accepted").checked == true) {
            request_url += "&return_accepted=" + document.getElementById("return_accepted").value;
        };

        if (document.getElementById("free_shipping").checked == true) {
            request_url += "&free_shipping=" + document.getElementById("free_shipping").value;
        };

        if (document.getElementById("expedited_shipping").checked == true) {
            request_url += "&expedited_shipping=" + document.getElementById("expedited_shipping").value;
        };
        
        request_url += "&sort_by=" + document.getElementById("sort_by").value;
        
        let xhttp = new XMLHttpRequest();
        xhttp.responseType = 'json';

        xhttp.onload = () => {
            if (xhttp.status == 200) {
                resolve(xhttp.response);
            };

            if (xhttp.status >= 400) {
                reject(xhttp.response);
            };
        };

        xhttp.open("GET", request_url, true);
        xhttp.send();
    });

    return promise;
};

// Function to display the result count
function displayResultCount(count) {
    // Remove the current result count if present
    if(document.getElementById("result_count") != null) {
        let removeResultCountDiv = document.getElementById("result_count");
        document.body.removeChild(removeResultCountDiv);
    };

    // Display the current result count
    if (count == 0) {
        let resultCountDiv = document.createElement("div");
        resultCountDiv.setAttribute("id", "result_count_empty");

        let resultCount = document.createElement("h2");
        resultCount.innerHTML = "No Results found"
        resultCountDiv.appendChild(resultCount);

        document.body.appendChild(resultCountDiv);
    } else {
        let resultCountDiv = document.createElement("div");
        resultCountDiv.setAttribute("id", "result_count");

        let resultCount = document.createElement("h2");
        resultCount.innerHTML = count + " Results found for " + "<span class='italic'>" + document.getElementById("key_words").value + "</span>";
        resultCountDiv.appendChild(resultCount);
        
        document.body.appendChild(resultCountDiv);
    };

};

// Function to create an item card
function createItemCard(cardHolder, item, itemNumber) {

    let cardDiv = document.createElement("div");
    cardDiv.setAttribute("class", "card");
    cardDiv.setAttribute("id", "item_" + itemNumber);

    let imageDiv = document.createElement("div");
    imageDiv.setAttribute("class", "image_div");
    let contentDiv = document.createElement("div");
    contentDiv.setAttribute("class", "content_div");

    cardDiv.appendChild(imageDiv);
    cardDiv.appendChild(contentDiv);

    // Display the image
    let itemImage = document.createElement("img");

    itemImage.setAttribute("src", item.galleryURL);
    
    if (item.galleryURL == "static/img/ebay_default.jpg") {
        itemImage.setAttribute("width", "160");
        itemImage.setAttribute("height", "100");
    };

    itemImage.setAttribute("alt", "item image");
    itemImage.setAttribute("class", "item_image")

    imageDiv.appendChild(itemImage);

    // Create the close button and its container(Starts Hidden)
    let closeButtonDiv = document.createElement("div");
    closeButtonDiv.setAttribute("class", "align_right");

    let closeButton = document.createElement("button");
    closeButton.setAttribute("type", "button");
    closeButton.setAttribute("class", "close_button extra_detail hidden");
    closeButton.setAttribute("id", "item_" + itemNumber + "_close_button");
    closeButton.innerHTML = "&times;"

    closeButtonDiv.appendChild(closeButton);
    contentDiv.appendChild(closeButtonDiv);

    // Display the Title
    let titleLink = document.createElement("a");
    titleLink.setAttribute("href", item.viewItemURL);
    titleLink.setAttribute("target", "_blank");
    titleLink.setAttribute("class", "bold truncate");
    titleLink.innerHTML = item.title;

    contentDiv.appendChild(titleLink);

    // Display the Category
    let category = document.createElement("p");

    let categoryRedirect = document.createElement("a");
    categoryRedirect.setAttribute("href", item.viewItemURL);
    categoryRedirect.setAttribute("target", "_blank");

    let redirectIcon = document.createElement("img");
    redirectIcon.setAttribute("src", "static/img/redirect.png");
    redirectIcon.setAttribute("alt", "redirect icon");
    redirectIcon.setAttribute("width", "15");
    redirectIcon.setAttribute("height", "15");
    redirectIcon.setAttribute("class", "redirect_icon");

    categoryRedirect.appendChild(redirectIcon);

    category.innerHTML = "Category: " + "<span class='italic'>" + item.category + "&nbsp;" + "</span>";

    category.appendChild(categoryRedirect);

    contentDiv.appendChild(category);
    
    // Display the Condition
    let condition = document.createElement("p");
    condition.innerHTML = "Condition: " + item.condition + "&nbsp;";

    if (item.topRatedListing == "true") {
        let topRatedImage = document.createElement("img");
        topRatedImage.setAttribute("src", "static/img/topRatedImage.png");
        topRatedImage.setAttribute("alt", "top rated image");
        topRatedImage.setAttribute("width", "20");
        topRatedImage.setAttribute("height", "30");
        condition.appendChild(topRatedImage);
    };

    contentDiv.appendChild(condition);

    // Create the returns field (Starts Hidden)
    let returns = document.createElement("p");
    returns.setAttribute("class", "extra_detail hidden");
    
    if (item.returnsAccepted == "true") {
        returns.innerHTML = "Seller <span class='bold'>accepts</span> returns";
    } else {
        returns.innerHTML = "Seller <span class='bold'>does not accept returns</span>";
    };

    contentDiv.appendChild(returns);

    // Create the shipping details (Starts Hidden)
    let shippingDetails = document.createElement("p");
    shippingDetails.setAttribute("class", "extra_detail hidden");

    if (item.freeShipping == "true") {
        shippingDetails.innerHTML = "Free Shipping";
    } else {
        shippingDetails.innerHTML = "No Free Shipping";
    };

    if (item.expeditedShipping == "true") {
        shippingDetails.innerHTML += " -- Expedited Shipping available";
    };

    contentDiv.appendChild(shippingDetails);

    // Display the Price
    let price = document.createElement("p");
    price.setAttribute("class", "bold");
    price.innerHTML = "Price: $" + item.sellingPrice;
    
    if (parseFloat(item.shippingPrice) > 0.0) {
        price.innerHTML += " ( + $" + item.shippingPrice + " for shipping)";
    };

    // Add the location (Starts Hidden)
    price.innerHTML += " <span class='italic extra_detail hidden unbold inline'>" + item.shipLocation + "</span>";

    contentDiv.appendChild(price);

    // Add the card to the page
    cardHolder.appendChild(cardDiv);
};