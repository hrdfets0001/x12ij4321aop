from TLSAdapters.TLSAdapter import TLSAdapter
import requests
import json
import os

class MarvelApiHandler():
    """Represents the HTTP client for the Marvel API.
    """
    
    def __init__(self, marvel_api_config):
        """Represents the constructor.

        Args:
            marvel_api_config (string): Represents the path to the JSON configuration of the Marvel API.
        """
        
        self.__set_api_connection_data(marvel_api_config)
    
    def get_all_characters(self, total_hero_count):
        """Fetches all characters from the Marvel API.
        The fetching is done using offset due to the fact that the API returns only limited amount of data for one call.

        Args:
            total_hero_count (int): The total amount of characters (has to be calculated beforehand).

        Raises:
            TypeError: Is thrown if the total count of characters is not integer.
            ValueError: Is thrown if the total amount of characters comprises zero or less.
            e: The raised exception.

        Returns:
            any: The returned JSON object representing an array of the characters..
        """
        try:
            if type(total_hero_count) != int:
                raise TypeError("total_hero_count must be an integer!")
            if (total_hero_count <= 0):
                raise ValueError("total_hero_count must be greater than 0!")

            result = '[]'
            offset = 0
            iteration_count = (total_hero_count // self.__data_max) + (total_hero_count % self.__data_max)
            result_json = json.loads(result)
            rows_max_limit = self.__data_max
            session = requests.session()
            session.mount('https://', TLSAdapter())

            for iter in range(iteration_count):
                params = {'apikey': self.__api_key, 'hash': self.__hash, 'ts': self.__ts, 'limit': rows_max_limit, 'offset': offset}
                resp = session.get(self.__url + '/characters', params=params)
                resp_json = resp.json()
                characters_json_array = resp_json['data']['results']
                result_json.extend(characters_json_array)
                offset += rows_max_limit
            
            return result_json
                
        except Exception as e:
            raise e
        
    def get_total_entity_count(self, entity_type):
        """Gets the total count of the given entity (e.g. how many comics are there?).

        Args:
            entity_type (str): The requested entity (comics, series, stories, events, characters).

        Raises:
            TypeError: Is thrown if the entity_type is not string.
            ValueError: Is thrown if an unknown entity type is passed.

        Returns:
            int: The total amount of the requested entity type.
        """
        if type(entity_type) != str:
            raise TypeError("entity_type must be a string!")  
        if not(entity_type in ['comics', 'series', 'stories', 'events', 'characters']):
            raise ValueError("entity_type was invalid!")
        rows_max_limit = self.__data_max
        session = requests.session()
        session.mount('https://', TLSAdapter())
        params = {'apikey': self.__api_key, 'hash': self.__hash, 'ts': self.__ts, 'limit': rows_max_limit}
        resp = session.get(self.__url + f'/{entity_type}', params=params)
        resp_json = resp.json()
        return resp_json['data']['total']

    def __set_api_connection_data(self, marvel_api_config):
        """Sets the connection data for the Marvel API.

        Args:
            marvel_api_config (str): The path leading to the JSON configuration of the Marvel API configuration.

        Raises:
            FileNotFoundError: Is thrown if the configuration at the given path does not exist.
        """
        if not(os.path.isfile(marvel_api_config)):
            raise FileNotFoundError('Could not find the config file!')

        json_config = open(marvel_api_config)
        data = json.load(json_config)
        self.__url = data['url']
        self.__api_key = data['apiKey']
        self.__hash = data['hash']
        self.__ts = data['ts']
        self.__data_max = data['dataMax']



