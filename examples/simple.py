#!/usr/bin/python
# -*- coding: utf-8 -*-

### Import modules
from here_api import HerePlacesAPI # For generating URLs
from here_api import request_api # For making HTTP requests using the URLs

### Define your API key generated on your account on HERE Developers website
apiKey = ''

### Generate Here Places (Search) API endpoint
# # for querying POIs that lie within 500m radius
# URL = HerePlacesAPI.in_circle(
#     lat=37.7942,
#     lon=-122.4070,
#     radius=500,
#     apiKey=apiKey)

# # for querying POIs that lie within a bounding box
# URL = HerePlacesAPI.in_box(
#     south_lat=37.793,
#     west_lon=-122.408,
#     north_lat=37.7942,
#     east_lon=-122.4070,
#     apiKey=apiKey)

# # for querying POIs around the area with specific string match
# URL = HerePlacesAPI.query_string(
#     query='hotel',
#     lat=37.7942,
#     lon=-122.4070,
#     apiKey=apiKey)

# # for querying popular POIs around the area
# URL = HerePlacesAPI.popular(
#     lat=37.7942,
#     lon=-122.4070,
#     category='hotel',
#     apiKey=apiKey)

# for querying nearby POIs around the area
URL = HerePlacesAPI.nearby(
    lat=37.7942,
    lon=-122.4070,
    apiKey=apiKey)

# Make HTTP GET request to the URL
df_items = request_api(URL, apiKey, max_items=100)
df_items
