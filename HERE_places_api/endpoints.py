#!/usr/bin/python
# -*- coding: utf-8 -*-

# %%
import json
import urllib
import requests


class HerePlacesAPI(object):
    """A python interface for generating Here Places API Endpoint (i.e. URL).

    Returns:
        Str: Here API Endpoint / URL.

    Example:
        >> # Search nearby places around a location.
        >> URL = HerePlacesAPI.nearby(
        >>    lat=37.7942,
        >>    lon=-122.4070,
        >>    apiKey='yourApiKey'
        >>    )
        >> print(URL)
        https://places.ls.hereapi.com/places/v1/discover/here\
            ?apiKey=yourApiKey\
            &at=37.7942%2C-122.407

    """

    def __init__(self):
        return

    @classmethod
    def __url_maker(cls, endpoint: str, dict_of_params: dict):
        """Base function for making URL for a specific API endpoint

       Args:
            endpoint (str): HERE API endpoint. 
            dict_of_params (dict): Parameters for the endpoint.
                e.g. lat, lon, apiKey, etc...

        Returns:
            str: URL for a specific API endpoint
        """
        # API endppoint
        base_url = "https://places.ls.hereapi.com/places/v1"
        # Encode urls
        escaped_params = urllib.parse.urlencode(
            dict_of_params, doseq=True
            )  # .encode("utf-8")
        # Construct url
        url = '{0}/{1}?{2}'.format(
            base_url, endpoint, escaped_params
            )
        return url

    @classmethod
    def get_all_categories(cls, apiKey: str):
        """Get URL for requesting the full list of all POI categories.

        Args:
            apiKey (str): API key generated on your account
                on the HERE Developers Website.

        Returns:
            str: URL of API endpoint
        """
        endpoint = 'categories/places'
        dict_of_params = {
            'apiKey': apiKey,
            }
        return cls.__url_maker(endpoint, dict_of_params)

    @classmethod
    def popular(cls, lat: float, lon: float, apiKey: str, category: str=''):
        """Get URL for requesting a list of popular places around a location.

        Args:
            lat (float|str): Latitude of the location.
            lon (float|str): Longitude of the location.
            apiKey (str): API key generated on your account
                on the HERE Developers Website.
            category (str): POI category.
                You can get full list using the
                "get_all_categories" method.

        Returns:
            str: URL of API endpoint

        Example:
            >> # Search nearby places around a location.
            >> URL = HerePlacesAPI.popular(
            >>    lat=37.7942,
            >>    lon=-122.4070,
            >>    apiKey='yourApiKey'
            >>    )
            >> print(URL)
            https://places.ls.hereapi.com/places/v1/discover/here\
                ?apiKey=yourApiKey\
                &at=37.7942%2C-122.407
        """
        endpoint = 'discover/explore'
        dict_of_params = {
            'at': "{},{}".format(lat, lon),
            'cat': category,
            'apiKey': apiKey,
            'size':100
            }
        return cls.__url_maker(endpoint, dict_of_params)

    @classmethod
    def nearby(cls, lat: float, lon: float, apiKey: str):
        """Get URL for requesting nearby places around a location.

        HERE makes POIs from yellow page, so the accuracy of data is unknown.
        For example, a hotel agency called "Cheapest Hotels" is categorized as a hotel.
        https://www.yellowpages.com/san-francisco-ca/mip/cheapest-hotels-473547373
        I recommend you to use the "popular" method instead,
        as that seems to return more reliable results.

        Args:
            lat (float|str): Latitude of the location.
            lon (float|str): Longitude of the location.
            apiKey (str): API key generated on your account
                on the HERE Developers Website.

        Returns:
            str: URL of API endpoint

        Example:
            >> # Search nearby places around a location.
            >> URL = HerePlacesAPI.nearby(
            >>    lat=37.7942,
            >>    lon=-122.4070,
            >>    apiKey='yourApiKey'
            >>    )
            >> print(URL)
            https://places.ls.hereapi.com/places/v1/discover/here\
                ?apiKey=yourApiKey\
                &at=37.7942%2C-122.407
        """
        endpoint = 'discover/here'
        dict_of_params = {
            'at': "{},{}".format(lat, lon),
            'apiKey': apiKey,
            'size': 100
            }
        return cls.__url_maker(endpoint, dict_of_params)

    @classmethod
    def query_string(cls, query: str, lat: float, lon: float, apiKey: str):
        """Get URL for requesting a list of nearby places based on a query string.

        HERE makes POIs from yellow page, so the accuracy of data is unknown.
        For example, a hotel agency called "Cheapest Hotels" is categorized as a hotel.
        https://www.yellowpages.com/san-francisco-ca/mip/cheapest-hotels-473547373
        I recommend you to use the "popular" method instead,
        as that seems to return more reliable results.

        Args:
            query (str): Any query string.
                E.g. restaurant, McDonalds, OYO Hotel
            lat (float|str): Latitude of the location.
            lon (float|str): Longitude of the location.
            apiKey (str): API key generated on your account
                on the HERE Developers Website.

        Returns:
            str: URL of API endpoint
        """
        endpoint = 'discover/search'
        dict_of_params = {
            'at': "{},{}".format(lat, lon),
            'apiKey': apiKey,
            'q': query,
            'size': 100
            }
        return cls.__url_maker(endpoint, dict_of_params)

    @classmethod
    def in_box(cls, south_lat: float, west_lon: float,
               north_lat: float, east_lon: float,
               apiKey: str, category: str = ''):
        """Get URL for requesting a list of places within a bounding box.

        Args:
            south_lat (float|str): Latitude of the bottom end
                of the bounding box to search.
            west_lon (float|str): Longitude of the left end
                of the bounding box to search.
            north_lat (float|str): Latitude of the top end
                of the bounding box to search.
            east_lon (float|str): Longitude of the right end
                of the bounding box to search.
            apiKey (str): API key generated on your account
                on the HERE Developers Website.
            category (str): POI category.
                You can get full list using the
                "get_all_categories" method.

        Returns:
            str: URL of API endpoint

        Example:
            >> URL = HerePlacesAPI.in_box(
            >>     south_lat=37.793,
            >>     west_lon=-122.408,
            >>     north_lat=37.7942,
            >>     east_lon=-122.4070,
            >>     apiKey='yourApiKey'
            >>     )
            >> print(URL)
            https://places.ls.hereapi.com/places/v1/discover/explore\
                ?apiKey=yourApiKey
                &in=-122.408%2C37.793%2C-122.407%2C37.7942
        """
        endpoint = 'discover/explore'
        dict_of_params = {
            'in': "{},{},{},{}".format(
                west_lon, south_lat,
                east_lon, north_lat
                ),
            'cat': category,
            'apiKey': apiKey,
            'size': 100
            }
        return cls.__url_maker(endpoint, dict_of_params)

    @classmethod
    def in_circle(cls, lat: float, lon: float, radius: int, apiKey: str, category: str = '')):
        """Get URL for requesting a list of popular places within a circle.

        Args:
            lat (float|str): Latitude of the location.
            lon (float|str): Longitude of the location.
            radius (float|str): Radius in meters.
            apiKey (str): API key generated on your account
                on the HERE Developers Website.
            category (str): POI category.
                You can get full list using the
                "get_all_categories" method.

        Returns:
            str: URL of API endpoint

        Example:
            >> URL = HerePlacesAPI.in_circle(
            >>     lat=-122.408,
            >>     lon=37.793,
            >>     radius=10,
            >>     apiKey='yourApiKey'
            >>     )
            >> print(URL)
            https://places.ls.hereapi.com/places/v1/discover/explore\
                ?apiKey=yourApiKey
                &in=-122.408%2C37.793%2C-122.407%2C37.7942
        """
        endpoint = 'discover/explore'
        dict_of_params = {
            'in': "{},{};r={}".format(lat, lon, radius),
            'cat': category,
            'apiKey': apiKey,
            'size': 100
            }
        return cls.__url_maker(endpoint, dict_of_params)
