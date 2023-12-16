import os
import json
import importlib
from Helpers.Helper import HelperClass
import pandas as pd
import os
from itertools import combinations

class RelationShipCalculator:
    """Represents the calculator of relationships between the characters.
    """
    def __init__(self, characters_config_path):
        """Represents the constructor.

        Args:
            characters_config_path (str): Path to the JSON file containing the array of characters (JSON objects).

        Raises:
            FileNotFoundError: Is thrown if the JSON file does not exist.
        """
        
        if not(os.path.isfile(characters_config_path)):
           raise FileNotFoundError('Could not find the JSON file!')
        heroes_json = open(characters_config_path)
        self.__characters_config_json = json.load(heroes_json)
        self.__allowed_entities = ['comics', 'series', 'events', 'stories']
        self.__helper = HelperClass()

    def get_relationships_frame_key_based_on_entity_type(self, entity_type):
        """Returns a data frame key.
        This key is used to retrieve specific columns from the data frame representing the amount of entities of certain entity type
        shared by two characters.

        Args:
            entity_type (str): The requested entity type (comics, series, stories or events).

        Raises:
            TypeError: Is thrown if the entity_type is no string.
            ValueError: Is thrown if the entity_type is unknown.

        Returns:
            str: The data frame key corresponding to the relevant column. 
        """
        if type(entity_type) != str:
            raise TypeError("entity_type has to be a string!")
        if entity_type not in self.__allowed_entities:
            raise ValueError("entity_type must be one of 'comics', 'series', 'stories', 'events")
        
        result = ''

        if entity_type == 'comics':
            result = 'CommonComicsAmount'
        if entity_type == 'series':
            result = 'CommonSeriesAmount'
        if entity_type == 'stories':
            result = 'CommonStoriesAmount'
        if entity_type == 'events':
            result = 'CommonEventsAmount'
        
        return result
    
    def get_hero_names(self):
        """Returns a list of all character names present in the JSON file representing a JSON array containing the characters (JSOn objects).

        Returns:
            list: A list representing the names of the characters.
        """
        names = [el['name'] for el in self.__characters_config_json]
        return names
    
    def get_hero_object(self, hero_name):
        """Returns a JSON object representing data about a character under the given name.

        Args:
            hero_name (str): The name of the character.

        Raises:
            TypeError: Is thrown if the name of the character is no string.

        Returns:
            any: The JSON object encapsulating the information about the character.
        """
        if type(hero_name) != str:
            raise TypeError("hero_name must be a string!")
        hero_object = [el for el in self.__characters_config_json if el['name'] == hero_name][0]
        return hero_object
    
    def get_entity_urls_for_hero(self, hero_name, entity):
        """Returns the URLs of entities in which the character under the given name appears (e.g. comics).

        Args:
            hero_name (str): The name of the character.
            entity (str): The requested entity type (comics, series, stories or events).

        Raises:
            TypeError:  Is thrown if the name of the character is no string.
            TypeError: Is thrown if the entity type is no string.
            ValueError: Is thrown if the entity type is not in the allowed entities.

        Returns:
            list: A list containing the URLs of the entities.
        """
        if type(hero_name) != str:
            raise TypeError("hero_name must be a string!")
        if type(entity) != str:
            raise TypeError("entity must be a string!")
        if not(entity in self.__allowed_entities):
            raise ValueError("entity had an invalid value (must be comics, series, events or stories)!")

        hero_object = self.get_hero_object(hero_name)
        result = []
        entities = hero_object[entity]['items']

        if len(entities) != 0:
                result = [entity['resourceURI'] for entity in entities]
        return result
    
    def get_hero_entities_dict(self, name, entity):
        """Returns a dictionary representing the names (keys) of the characters with the URLs of the corresponding entity (values).
        E.g.: {'Spider-Man (Peter Parker)' : ['http://aaa, 'http://aaa2,...]}

        Args:
            name (str): The name of the character.
            entity (str): The requested entity type (comics, series, stories or events).

        Raises:
            TypeError: Is thrown if the name of the character is no string.
            TypeError: Is thrown if the entity type is no string.
            ValueError: Is thrown if the entity type is not in the allowed entities.
            ValueError: Is thrown if the name of the character does not exist.

        Returns:
            dict: The result dictionary.
        """
        if type(name) != str:
            raise TypeError("name must be a string!")
        if type(entity) != str:
            raise TypeError("entity must be a string!")
        if not(entity in self.__allowed_entities):
            raise ValueError("entity had an invalid value (must be comics, series, events or stories)!")
        
        names = self.get_hero_names()

        if name not in names:
            raise ValueError("hero_name does not exist!")
        
        urls = self.get_entity_urls_for_hero(name, entity)
        dict_to_add = dict()
        dict_to_add[name] = urls
        return dict_to_add
    
    def get_entity_urls_for_heroes(self, hero_names, entity):
        """Returns a list of dictionaries representing the names (keys) of the characters with the URLs of the corresponding entity (values).
        E.g.: [{'Spider-Man (Peter Parker)' : ['http://aaa, 'http://aaa2,...]}, {'Beast' : ['http://aaa, 'http://aaa2,...]}, ...]

        Args:
            hero_names (list): Names of the characters.
            entity (str): The requested entity type (comics, series, stories or events).

        Raises:
            TypeError: Is thrown if the names of the characters is no list.
            TypeError: Is thrown if the entity type is no string.
            ValueError: Is thrown if the entity type is not in the allowed entities.
            TypeError: Is thrown if the names of the characters are no strings.
            ValueError: Is thrown if some names of the characters do not exist.

        Returns:
            list: List of the dictionaries.
        """
        if type(hero_names) != list:
            raise TypeError("hero_names must be a list!")
        if type(entity) != str:
            raise TypeError("entity must be a string!")
        if not(entity in self.__allowed_entities):
            raise ValueError("entity had an invalid value (must be comics, series, events or stories)!")
        if not(all([type(el) == str for el in hero_names])):
            raise TypeError("All elements in hero_names must be strings!")
        
        names = self.get_hero_names()

        names_set = set(names)
        hero_names_set = set(hero_names)
        set_intersect = names_set & hero_names_set

        if set_intersect != hero_names_set:
            raise ValueError("Non-existent values present in hero_names!")
        
        names_list = list(hero_names_set)
        result = [self.get_hero_entities_dict(name, entity) for name in names_list]
        return result
    
    def get_common_entity_urls(self, hero_names, entity):
        """Returns  URLs of the entities shared by the names of the given characters.

        Args:
            hero_names (list): Names of the characters.
            entity (str): The requested entity type (comics, series, stories or events).

        Raises:
            TypeError: Is thrown if the names of the characters is no list.
            TypeError: Is thrown if the entity type is no string.
            ValueError: Is thrown if the entity type is not in the allowed entities.
            TypeError: Is thrown if the names of the characters are no strings.
            ValueError: Is thrown if some names of the characters do not exist.

        Returns:
            list: The list of the common entity URLs.
        """
        if type(hero_names) != list:
            raise TypeError("hero_names must be a list!")
        if type(entity) != str:
            raise TypeError("entity must be a string!")
        if not(entity in self.__allowed_entities):
            raise ValueError("entity had an invalid value (must be comics, series, events or stories)!")
        if not(all([type(el) == str for el in hero_names])):
            raise TypeError("All elements in hero_names must be strings!")
        
        names = [el['name'] for el in self.__characters_config_json]

        names_set = set(names)
        hero_names_set = set(hero_names)
        set_intersect = names_set & hero_names_set

        if set_intersect != hero_names_set:
            raise ValueError("Non-existent values present in hero_names!")
        
        entity_urls_mappings = self.get_entity_urls_for_heroes(list(hero_names_set), entity)
        mapping_tuples = [self.__helper.get_dict_value(el, 0) for el in entity_urls_mappings]
        urls_sets = [set(el[1]) for el in mapping_tuples]
        result_set = set.intersection(*urls_sets)
        return list(result_set)

    def get_amount_of_common_entities_data_frame(self, hero_names, entity_type):
        """Creates a data frame consisting of the amount of common entities of the given type
        for each combination of pairs for the given character names.
        Format: Character1 | Character2 | Common<EntityName>Amount

        Args:
            hero_names (list): Names of the characters.
            entity_type (str): The requested entity type (comics, series, stories or events).

        Returns:
            DataFrame: The data frame representing the description above.
        """
        frame_key = self.get_relationships_frame_key_based_on_entity_type(entity_type)
        relationships_in_entities_frame = pd.DataFrame()
        relationships_in_entities_frame['Character1'] = []
        relationships_in_entities_frame['Character2'] = []
        relationships_in_entities_frame[frame_key] = []
        relationships_in_entities_frame.astype({frame_key: 'int32'}).dtypes
        relationships_in_entities_frame[frame_key] = pd.to_numeric(relationships_in_entities_frame[frame_key], downcast='integer')
        name_relationships = [list(el) for el in list(combinations(hero_names, 2))]
        names_first = [el[0] for el in name_relationships]
        names_second = [el[1] for el in name_relationships]
        names_first_series = pd.Series(names_first)
        names_second_series = pd.Series(names_second)
        relationships_in_entities_frame['Character1'] = names_first_series
        relationships_in_entities_frame['Character2'] = names_second_series
        entities_amount = pd.Series([len(self.get_common_entity_urls(el, entity_type)) for el in name_relationships])
        relationships_in_entities_frame[frame_key] = entities_amount
        
        return relationships_in_entities_frame

