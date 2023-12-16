from itertools import permutations
import json
import os

class HelperClass:
    """Represents the helper class.
    """
    
    def load_json_data(self, json_path):
        """Reads JSON data from the file on the given path.

        Args:
            json_path (str): The path of the file.

        Raises:
            FileNotFoundError: Is raised if the file on the given path does not exist.

        Returns:
            any: The JSON object representing the content of the file on the given path.
        """
        if not(os.path.isfile(json_path)):
            raise FileNotFoundError("The path of the json file could not be found!")
        content = open(json_path)
        data = json.load(content)
        return data

    def get_dict_value(self, input_value : dict, index):
        """Returns the value in dictionary at the given index.
        E.g.: get_dict_value({'a': 'b', 'c':'d', 'e':'f'}, 1) -> ('c', 'd')

        Args:
            input_value (dict): The input dictionary.
            index (int): The index of the element to return.

        Raises:
            TypeError: Is thrown if the input parameters have incorrect types. 
            ValueError: Is thrown if the index is out of range.

        Returns:
            tuple: A tuple representing the element at the index.
        """
        if type(input_value) != dict:
            raise TypeError("input_value must be a dict!")
        if type(index) != int:
            raise TypeError("index must be an integer!")
        items = list(input_value.items())
        if not(index >= 0 and index <= len(items) - 1):
            raise ValueError("index must be in range!")
        return items[index]
    
    def join_lists(self, lists):
        """Joins the lists.

        Args:
            lists (list): Represents a list of lists.

        Raises:
            TypeError: Is thrown if the input list has incorrect container type.
            TypeError: Is thrown if the elements of the list are not lists.

        Returns:
            list: The joined lists.
        """
        if type(lists) != list:
            raise TypeError("lists must be a list!")
        if not(all([type(el) == list for el in lists])):
            raise TypeError("lists must consits of lists!")
        
        result = []

        for el in lists:
            result.extend(el)
        
        return result
    
    def is_within_range(self, value, min, max):
        """Determines whether the input value is within the valid range (>= min and <= max).

        Args:
            value (int): The input value.
            min (int): The lower boundary.
            max (int): The upper boundary.

        Raises:
            TypeError: Is thrown if value has incorrect type.
            TypeError: Is thrown if min has incorrect type.
            TypeError: Is thrown if max has incorrect type.

        Returns:
            bool: A boolean indicating whether the input value is within the valid range.
        """
        if type(value) != int:
            raise TypeError("value has to be an int!")
        if type(min) != int:
            raise TypeError("min has to be an int!")
        if type(max) != int:
            raise TypeError("max has to be an int!")
        return value >= min and value <= max
    


        

    

