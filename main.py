import requests
from flask import Flask, request, jsonify

# App is hosted @ https://mjwong-csci-571-hw6.wl.r.appspot.com

app = Flask(__name__)

@app.route('/B15OWJ0eg1Pq.html')
def root():
    return app.send_static_file('B15OWJ0eg1Pq.html')

@app.route('/items', methods=['GET'])
def items():
    
    if request.method == 'GET':

        # Grab your parameters
        keywords = request.args.get('keywords')
        price_from = request.args.get('price_from')
        price_to = request.args.get('price_to')
        return_accepted = request.args.get('return_accepted')
        free_shipping = request.args.get('free_shipping')
        expedited_shipping = request.args.get('expedited_shipping')
        new = request.args.get('new')
        used = request.args.get('used')
        very_good = request.args.get('very_good')
        good = request.args.get('good')
        acceptable = request.args.get('acceptable')
        sort_by = request.args.get('sort_by')

        # Make the request to ebay
        request_response = get_find_items_advanced( 
            keywords=keywords, 
            price_from=price_from, 
            price_to=price_to, 
            return_accepted=return_accepted, 
            free_shipping=free_shipping, 
            expedited_shipping=expedited_shipping, 
            new=new,
            used=used,
            very_good=very_good,
            good=good,
            acceptable=acceptable,
            sort_by=sort_by)

        # We now need to filter our raw request_response down to 10 entries
        filtered_response = {}
        filtered_response["totalResults"] = request_response["findItemsAdvancedResponse"][0]["paginationOutput"][0]["totalEntries"][0]
        
        items = []

        if int(filtered_response["totalResults"]) >= 1:
            items = request_response["findItemsAdvancedResponse"][0]["searchResult"][0]["item"] #list
        
        filtered_item_number = 0
        item_number = 0

        while filtered_item_number < 10 and item_number < len(items):
            
            item = {}

            add = True
            
            # Check that the item has an image link
            if add and "galleryURL" in items[item_number].keys():
                item["galleryURL"] = items[item_number]["galleryURL"][0]
            else:
                item["galleryURL"] = "default"
            
            # Check that the item has a title
            if add and "title" in items[item_number].keys():
                item["title"] = items[item_number]["title"][0]
            else:
                add = False

            # Check that the item has a category
            if add and "primaryCategory" in items[item_number].keys():
                item["category"] = items[item_number]["primaryCategory"][0]["categoryName"][0]
            else:
                add = False
            
            # Check that the item has a eBay product link for redirection
            if add and "viewItemURL" in items[item_number].keys():
                item["viewItemURL"] = items[item_number]["viewItemURL"][0]
            else:
                add = False

            # Check that the item has condition for the item
            if add and "condition" in items[item_number].keys() and "conditionDisplayName" in items[item_number]["condition"][0].keys():
                item["condition"] = items[item_number]["condition"][0]["conditionDisplayName"][0]
            else:
                add = False

            # Check that the item is top rated
            if add and "topRatedListing" in items[item_number].keys():
                if items[item_number]["topRatedListing"][0] == "true": 
                    item["topRatedListing"] = "true"
                else:
                    item["topRatedListing"] = "false"
            else:
                add = False

            # Check that the item has a price + shipping price
            if add and  "sellingStatus" in items[item_number].keys() and "convertedCurrentPrice" in items[item_number]["sellingStatus"][0].keys() and "__value__" in items[item_number]["sellingStatus"][0]["convertedCurrentPrice"][0].keys():
                item["sellingPrice"] = items[item_number]["sellingStatus"][0]["convertedCurrentPrice"][0]["__value__"]
            else:
                add = False

            if add and  "shippingInfo" in items[item_number].keys() and "shippingServiceCost" in items[item_number]["shippingInfo"][0].keys() and "__value__" in items[item_number]["shippingInfo"][0]["shippingServiceCost"][0].keys():
                item["shippingPrice"] = items[item_number]["shippingInfo"][0]["shippingServiceCost"][0]["__value__"]
            else:
                add = False

            # Check if seller accepts return
            if add and  "returnsAccepted" in items[item_number].keys():
                if items[item_number]["returnsAccepted"][0] == "true":
                    item["returnsAccepted"] = "true"
                else:
                    item["returnsAccepted"] = "false"
            else:
                add = False

            # Check if free shipping is available
            if add and  "shippingInfo" in items[item_number].keys() and "shippingServiceCost" in items[item_number]["shippingInfo"][0].keys() and "__value__" in items[item_number]["shippingInfo"][0]["shippingServiceCost"][0].keys():
                if items[item_number]["shippingInfo"][0]["shippingServiceCost"][0]["__value__"] == "0.0":
                    item["freeShipping"] = "true"
                else:
                    item["freeShipping"] = "false"
            else:
                add = False

            # Check if expedited shpping is available
            if add and  "shippingInfo" in items[item_number].keys() and "expeditedShipping" in items[item_number]["shippingInfo"][0].keys():
                if items[item_number]["shippingInfo"][0]["expeditedShipping"][0] == "true":
                    item["expeditedShipping"] = "true"
                else:
                    item["expeditedShipping"] = "false"
            else:
                add = False

            # Check the ships from location
            if add and  "location" in items[item_number].keys():
                if len(items[item_number]["location"]) > 0 and items[item_number]["location"][0] != "":
                    item["shipLocation"] = items[item_number]["location"][0]
                else:
                    add = False
            else:
                add = False

            if add:
                filtered_response[f"item_{filtered_item_number}"] = item
                filtered_item_number += 1

            item_number += 1
                     
        return jsonify(filtered_response)


def get_find_items_advanced(
    keywords: str, price_from: float, price_to: float, return_accepted: str, free_shipping: str, expedited_shipping: str, 
    new: str, used: str, very_good: str, good: str, acceptable: str, sort_by: str) -> dict:

    base_url = "https://svcs.eBay.com/services/search/FindingService/v1"

    params = {
        "OPERATION-NAME": "findItemsAdvanced", 
        "SERVICE-VERSION": "1.0.0", 
        "SECURITY-APPNAME": "MatthewW-mjwong-PRD-02eb4905c-0b11768c",
        "RESPONSE-DATA-FORMAT": "JSON", 
        "REST-PAYLOAD": True,
        "paginationInput.entriesPerPage": 50,  
        "keywords": keywords
    }

    item_filter_count = 0

    if price_from:
        params[f"itemFilter({item_filter_count}).name"] = "MinPrice"
        params[f"itemFilter({item_filter_count}).value"] = price_from
        params[f"itemFilter({item_filter_count}).paramName"] = "Currency"
        params[f"itemFilter({item_filter_count}).paramValue"] = "USD"
        item_filter_count += 1

    if price_to:
        params[f"itemFilter({item_filter_count}).name"] = "MaxPrice"
        params[f"itemFilter({item_filter_count}).value"] = price_to
        params[f"itemFilter({item_filter_count}).paramName"] = "Currency"
        params[f"itemFilter({item_filter_count}).paramValue"] = "USD"
        item_filter_count += 1

    if return_accepted:
        params[f"itemFilter({item_filter_count}).name"] = "ReturnsAcceptedOnly"
        params[f"itemFilter({item_filter_count}).value"] = True
        item_filter_count += 1

    if free_shipping:
        params[f"itemFilter({item_filter_count}).name"] = "FreeShippingOnly"
        params[f"itemFilter({item_filter_count}).value"] = True
        item_filter_count += 1

    if expedited_shipping:
        params[f"itemFilter({item_filter_count}).name"] = "ExpeditedShippingType"
        params[f"itemFilter({item_filter_count}).value"] = "Expedited"
        item_filter_count += 1

    if new or used or very_good or good or acceptable:
        params[f"itemFilter({item_filter_count}).name"] = "Condition"

        condition_count = 0

        if new:
            params[f"itemFilter({item_filter_count}).value({condition_count})"] = 1000
            condition_count += 1

        if used:
            params[f"itemFilter({item_filter_count}).value({condition_count})"] = 3000
            condition_count += 1

        if very_good:
            params[f"itemFilter({item_filter_count}).value({condition_count})"] = 4000
            condition_count += 1

        if good:
            params[f"itemFilter({item_filter_count}).value({condition_count})"] = 5000
            condition_count += 1

        if acceptable:
            params[f"itemFilter({item_filter_count}).value({condition_count})"] = 6000

    if sort_by:
        params["sortOrder"] = sort_by
        
    response = requests.get(base_url, params=params)

    return response.json()

if __name__ == '__main__':
    app.run()