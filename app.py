from flask import Flask, render_template, request, Response, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from math import ceil

app = Flask(__name__)

uri = "mongodb://localhost:27017"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.zomatoDB
restaurant_collection = db.restaurant

country_codes = {
    1: 'India',14: 'Australia',30: 'Brazil',37: 'Canada',94: 'Indonesia',148: 'New Zealand',162: 'Philippines',166: 'Qatar',184: 'Singapore',189: 'South Africa',191: 'Sri Lanka',208: 'Turkey',214: 'UAE',215: 'United Kingdom',
    216: 'United States'
}

@app.route('/')
def index():
    cuisine_filter = request.args.get('cuisine', '')
    search_query = request.args.get('search', '')
    cost_filter = request.args.get('cost', '')
    country_filter = request.args.get('country', '')
    cursor = restaurant_collection.find()
    restaurants = []

    for document in cursor:
        if 'restaurants' in document:
            restaurants_data = document['restaurants']
            # Extract 'restaurant' documents from each entry
            restaurants.extend([entry['restaurant'] for entry in restaurants_data if 'restaurant' in entry])

    if cuisine_filter:
        restaurants = [restaurant for restaurant in restaurants if cuisine_filter.lower() in restaurant['cuisines'].lower()]
    if cost_filter:
        restaurants = [restaurant for restaurant in restaurants if int(cost_filter) == restaurant['average_cost_for_two']]
    if search_query:
        restaurants = [restaurant for restaurant in restaurants if search_query.lower() in restaurant['name'].lower()]
    if country_filter:
        restaurants = [restaurant for restaurant in restaurants if restaurant['location']['country_id'] == int(country_filter)]

    page = int(request.args.get('page', 1))
    per_page = 6
    total = len(restaurants)
    pages = ceil(total / per_page)
    
    start = (page - 1) * per_page
    end = start + per_page
    restaurants_paginated = restaurants[start:end]
    rname=set()
    cuisines = set()
    for restaurant in restaurants:
        cuisines.update([cuisine.strip() for cuisine in restaurant['cuisines'].split(',')])
    costs = set()
    for restaurant in restaurants:
        costs.add(restaurant['average_cost_for_two'])
    costs = sorted(costs)
    response_data = []
    for restaurant in restaurants_paginated:
        response_data.append({
            'name': restaurant['name'],
            'image_url': restaurant['featured_image']
        })
    #return jsonify(response_data)
    return render_template('home.html', restaurants=restaurants_paginated, page=page, pages=pages, max=max, min=min, cuisine_filter=cuisine_filter, cuisines=cuisines, costs=costs, search_query=search_query, country_codes=country_codes, country_filter=country_filter)
    '''return jsonify({
            'restaurants': restaurants_paginated,
            'page': page,
            'pages': pages,
            'cuisine_filter': cuisine_filter,
            'cuisines': list(cuisines),
            'costs': list(costs),
            'search_query': search_query,
            'country_filter': country_filter
        })'''
@app.route('/restaurant/<string:res_id>')
def restaurant_detail(res_id):
    cursor = restaurant_collection.find()
    
    for document in cursor:
        if 'restaurants' in document:
            for entry in document['restaurants']:
                restaurant = entry.get('restaurant')
                if restaurant and restaurant['R']['res_id'] == int(res_id):
                    return render_template('restaurant_detail.html', restaurant=restaurant)
                    #return jsonify(restaurant['name'],res_id,restaurant['featured_image'],restaurant['location']['address'],restaurant['average_cost_for_two'],restaurant['user_rating']['aggregate_rating'])
    return "Restaurant not found", 404

if __name__ == '__main__':
    app.run(debug=True)
