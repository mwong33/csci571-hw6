import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/items', methods=['GET'])
def items():
    
    if request.method == 'GET':

        keywords = request.args.get('keywords')
        price_from = request.args.get('price_from')
        price_to = request.args.get('price_to')
        returns_accepted = request.args.get('returns_accepted')
        free_shipping = request.args.get('free_shipping')
        expedited_shipping = request.args.get('expedited_shipping')
        new = request.args.get('new')
        used = request.args.get('used')
        very_good = request.args.get('very_good')
        good = request.args.get('good')
        acceptable = request.args.get('acceptable')

        request_response = {}

        no_condition = True

        if new:
            request_response["new"] = get_find_items_advanced( 
                keywords=keywords, 
                price_from=price_from, 
                price_to=price_to, 
                returns_accepted=returns_accepted, 
                free_shipping=free_shipping, 
                expedited_shipping=expedited_shipping, 
                condition=1000)

            no_condition = False

        if used:
            request_response["used"] = get_find_items_advanced( 
                keywords=keywords, 
                price_from=price_from, 
                price_to=price_to, 
                returns_accepted=returns_accepted, 
                free_shipping=free_shipping, 
                expedited_shipping=expedited_shipping, 
                condition=3000)

            no_condition = False

        if very_good:
            request_response["very_good"] = get_find_items_advanced( 
                keywords=keywords, 
                price_from=price_from, 
                price_to=price_to, 
                returns_accepted=returns_accepted, 
                free_shipping=free_shipping, 
                expedited_shipping=expedited_shipping, 
                condition=4000)

            no_condition = False

        if good:
            request_response["good"] = get_find_items_advanced( 
                keywords=keywords, 
                price_from=price_from, 
                price_to=price_to, 
                returns_accepted=returns_accepted, 
                free_shipping=free_shipping, 
                expedited_shipping=expedited_shipping, 
                condition=5000)

            no_condition = False

        if acceptable:
            request_response["acceptable"] = get_find_items_advanced( 
                keywords=keywords, 
                price_from=price_from, 
                price_to=price_to, 
                returns_accepted=returns_accepted, 
                free_shipping=free_shipping, 
                expedited_shipping=expedited_shipping, 
                condition=6000)

            no_condition = False

        if no_condition:
            request_response = get_find_items_advanced( 
                keywords=keywords, 
                price_from=price_from, 
                price_to=price_to, 
                returns_accepted=returns_accepted, 
                free_shipping=free_shipping, 
                expedited_shipping=expedited_shipping, 
                condition=None)
        
        return jsonify(request_response)


def get_find_items_advanced(
    keywords: str, price_from: float, price_to: float, returns_accepted: bool, free_shipping: bool, expedited_shipping: bool, condition: int) -> dict:

    base_url = "https://svcs.eBay.com/services/search/FindingService/v1"

    params = {
        "OPERATION-NAME": "findItemsAdvanced", 
        "SERVICE-VERSION": "1.0.0", 
        "SECURITY-APPNAME": "MatthewW-mjwong-PRD-02eb4905c-0b11768c",
        "RESPONSE-DATA-FORMAT": "JSON", 
        "REST-PAYLOAD": "true",
        "paginationInput.entriesPerPage": "10",  
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

    if returns_accepted:
        params[f"itemFilter({item_filter_count}).name"] = "ReturnsAcceptedOnly"
        params[f"itemFilter({item_filter_count}).value"] = "true"
        item_filter_count += 1

    if free_shipping:
        params[f"itemFilter({item_filter_count}).name"] = "FreeShippingOnly"
        params[f"itemFilter({item_filter_count}).value"] = "true"
        item_filter_count += 1

    if expedited_shipping:
        params[f"itemFilter({item_filter_count}).name"] = "ExpeditedShippingType"
        params[f"itemFilter({item_filter_count}).value"] = "Expedited"
        item_filter_count += 1

    if condition:
        params[f"itemFilter({item_filter_count}).name"] = "Condition"
        params[f"itemFilter({item_filter_count}).value"] = condition
        item_filter_count += 1

    response = requests.get(base_url, params=params)

    return response.json()

if __name__ == '__main__':
    app.run()