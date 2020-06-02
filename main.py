import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/B15OWJ0eg1Pq.html')
def root():
    return app.send_static_file('B15OWJ0eg1Pq.html')

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
        sort_order = request.args.get('sort_order')

        request_response = {}

        request_response = get_find_items_advanced( 
            keywords=keywords, 
            price_from=price_from, 
            price_to=price_to, 
            returns_accepted=returns_accepted, 
            free_shipping=free_shipping, 
            expedited_shipping=expedited_shipping, 
            new=new,
            used=used,
            very_good=very_good,
            good=good,
            acceptable=acceptable,
            sort_order=sort_order)
        
        return jsonify(request_response)


def get_find_items_advanced(
    keywords: str, price_from: float, price_to: float, returns_accepted: bool, free_shipping: bool, expedited_shipping: bool, 
    new: int, used: int, very_good: int, good: int, acceptable: int, sort_order: str) -> dict:

    base_url = "https://svcs.eBay.com/services/search/FindingService/v1"

    params = {
        "OPERATION-NAME": "findItemsAdvanced", 
        "SERVICE-VERSION": "1.0.0", 
        "SECURITY-APPNAME": "MatthewW-mjwong-PRD-02eb4905c-0b11768c",
        "RESPONSE-DATA-FORMAT": "JSON", 
        "REST-PAYLOAD": True,
        "paginationInput.entriesPerPage": 25,  
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

    if sort_order:
        params["sortOrder"] = sort_order
        
    response = requests.get(base_url, params=params)

    return response.json()

if __name__ == '__main__':
    app.run()