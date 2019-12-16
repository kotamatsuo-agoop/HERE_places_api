
#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd


def request_api(URL, apiKey, max_items):
    """Make HTTP Get request to Here Places API.

    Example:
        apiKey = 'yourApiKey'
        URL = HerePlacesAPI.in_circle(
            lat=37.7942,
            lon=-122.4070,
            radius=500,
            apiKey=apiKey)
        df_items = request_api(URL, apiKey, max_items=100)
    """
    # Request URL
    results = _request_api(URL)
    # Get next_page_URL if contained in the results
    next_page_URL = _next_page(results, apiKey)
    # Store dict of items into a list
    list_of_dict_of_items = results.get('items')
    # While next page exists, keep requesting
    while next_page_URL:
        next_results = _request_api(next_page_URL)
        if next_results:
            next_page_URL = _next_page(next_results, apiKey)
            next_items = next_results.get('items')
            list_of_dict_of_items.extend(next_items)
        else:
            next_page_URL = None
        # Just for safety
        if len(list_of_dict_of_items) >= max_items:
            break
    if list_of_dict_of_items == None:
        df_items = pd.DataFrame()
    else:
        df_items = _format_items(list_of_dict_of_items)
    return df_items


def _request_api(URL):
    """Make a single HTTP Get request."""
    # Request
    headers = {'Accept': 'application/json'}
    response = requests.get(URL, headers=headers)
    # Decode into str
    decoded_response = response.content.decode('utf8')
    # Convert to json
    json_response = json.loads(decoded_response)
    # Parse response (into results & search_meta_info)
    if 'results' in json_response.keys():
        # Dict contains dict_keys(['results', 'search'])
        results = json_response.get('results')
    else:
        # If next page URL is requested, the dict contains
        # dict_keys(['items', 'next', 'previous', 'offset'])
        results = json_response
    #search_meta_info = json_response.get('search')
    return results


def _next_page(results, apiKey):
    """Check if the response contains next page token"""
    # Check if next page exists
    next_page_URL = None
    if 'next' in results.keys():
        next_page_URL = results.get('next')
    # If the next pge exists
    if next_page_URL:
        # Attach apiKey to the end
        next_page_URL = next_page_URL+'&apiKey={}'.format(apiKey)
    return next_page_URL


def _format_items(list_of_dict_of_items):
    """Format json response into a dataframe"""
    if len(list_of_dict_of_items) == 0:
        return pd.DataFrame()
    # Columns to save in the dataframe
    keys = ['title', 'category_id', 'address', 'lat', 'lon', 'distance']
    # Values to save in the dataframe
    list_formatted_items = []
    for item in list_of_dict_of_items:
        # Take out values from the dict
        category_id = item['category']['id']
        distance = item['distance']
        lat = item['position'][0]
        lon = item['position'][1]
        title = item['title']
        address = item['vicinity']
        # Store in a new dict
        values = [title, category_id, address, lat, lon, distance]
        dict_this_item = dict(zip(keys, values))
        # Store the new dict in list
        list_formatted_items.append(dict_this_item)
    # Convert list of dicts into DataFrame
    df_items = pd.DataFrame().from_dict(list_formatted_items)
    # Order columns
    df_items = df_items[keys]
    # Sort by distance
    df_items.sort_values(by='distance', ascending=True, inplace=True)

    return df_items
