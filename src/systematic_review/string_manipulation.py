"""Module: string_manipulation
This module contains functions related to string case change, preprocess, and removing some part of it.
"""

import unicodedata
from systematic_review import os_utils


def string_dict_to_lower(string_map: dict) -> dict:
    """
    this convert the values into lowercase. similar function for list is available as string_list_to_lower()

    Parameters
    ----------
    string_map : dict
        these are key:values pairs needed to be converted.

    Returns
    -------
    dict
         output by converting input to key: lowercase values.

    """
    lower_string_map = dict()
    for key, value in string_map.items():
        lower_string_map[key] = str(value).lower().replace("\n", " ")
    return lower_string_map


def string_list_to_lower(string_list: list) -> list:
    """
    this convert the values into lowercase. similar function for dict is available as string_dict_to_lower()

    Parameters
    ----------
    string_list : list
        this list contains input string need to be converted to lowercase.

    Returns
    -------
    list
        this is the output list which contains original input strings but in lowercase

    """
    lower_string_list = list()
    for string in string_list:
        lower_string_list.append(str(string).lower().replace("\n", " "))
    return lower_string_list


def string_to_space_separated_words(text: str) -> str:
    """takes text string and outputs space separated words.

    Parameters
    ----------
    text : str
        This text contains multiple spaces or trailing whitespaces

    Returns
    -------
    str
        This is space separated word string with no trailing whitespaces.

    """
    temp_text = text.split()
    return " ".join(temp_text)


def remove_non_ascii(string_list: list) -> list:
    """Remove non-ASCII characters from list of tokenized words

    Parameters
    ----------
    string_list : list
        this list contains the words which contains the non-ASCII characters

    Returns
    -------
    list
        this is modified list after removing the non-ASCII characters

    """
    new_words = []
    for word in string_list:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def split_words_remove_duplicates(string_list: list) -> list:
    """
    this function takes a list of words or sentences and split them to individual words. It also removes any repeating
    word in the list.

    Parameters
    ----------
    string_list : list
        this is the input list which contains words and group of words inside. Example - ['one', 'one two']

    Returns
    -------
    list
        this is the output list which contains only unique individual words using set(). Example - ['one', 'two']

    """
    temp_set = set()
    for string in string_list:
        for word in string.split():
            temp_set.add(word)
    modified_list = list(temp_set)
    return modified_list


def preprocess_string(string: str) -> str:
    """replace symbols in string with spaces and Lowercase the given input string. Example - 'Df%$df' -> 'df  df'

    Parameters
    ----------
    string : str
        This is input word string which contains unwanted symbols and might have uppercase characters in it.

    Returns
    -------
    str
        This is cleaned string from symbols and contains only alpha characters.

    """
    string = replace_symbols_with_space(string)
    string = convert_string_to_lowercase(string)
    return string


def preprocess_string_to_space_separated_words(string: str) -> str:
    """replace symbols in string with spaces and Lowercase the given input string. Example - 'Df%$df' -> 'df  df' and
    convert 'df  df' to single spaced 'df df'.

    Parameters
    ----------
    string : str
        This can contain string words mixed with spaces and symbols.

    Returns
    -------
    str
        remove the spaces and symbols and arrange the words single spaces.

    """
    string = preprocess_string(string)
    string = string_to_space_separated_words(string)
    return string


def replace_symbols_with_space(string: str) -> str:
    """replace symbols in string with spaces. Example - 'df%$df' -> 'df  df'

    Parameters
    ----------
    string : str
        This is input word string which contains unwanted symbols.

    Returns
    -------
    str
        This is cleaned string from symbols and contains only alpha characters and all lowercase character string.

    """
    alpha = ""
    for character in string:
        if character.isalpha():
            alpha += character
        elif character == " ":
            alpha += character
        else:
            alpha += " "
    return alpha


def convert_string_to_lowercase(string: str) -> str:
    """Lowercase the given input string.

    Parameters
    ----------
    string : str
        The string which might have uppercase characters in it.

    Returns
    -------
    str
        This is all lowercase character string.

    """
    return string.lower()


def split_preprocess_string(text: str) -> list:
    """This splits the words into list after applying preprocess function from string_manipulation module.

    Parameters
    ----------
    text : str
        This is input word string which contains unwanted symbols and might have uppercase characters in it.

    Returns
    -------
    list
        This is cleaned list of strings from symbols and contains only alpha characters.

    """
    clean_text = preprocess_string(text)
    text_list = clean_text.split()
    return text_list


def pdf_filename_from_filepath(article_path: str) -> str:
    """This takes the pdf path as input and clean the name of pdf by applying preprocess function from
    string_manipulation module.

    Parameters
    ----------
    article_path : str
        This is the path of the pdf file.

    Returns
    -------
    str
        This is the cleaned filename of the pdf.

    """
    article_filename = os_utils.get_filename_from_path(article_path)
    article_name = strip_string_from_right_side(article_filename)

    return article_name


def strip_string_from_right_side(string: str, value_to_be_stripped: str = ".pdf") -> str:
    """Function removes the substring from the right of string.

    Parameters
    ----------
    string : str
        This is the complete word or string. Example - 'monster.pdf'
    value_to_be_stripped : str
        This is the value which is needed to be removed from right side. Example - '.pdf'

    Returns
    -------
    str
        This is the trimmed string that contains the left part after some part removed from the right.
        Example - 'monster'

    """
    stripped_string = string.rstrip(value_to_be_stripped)
    return stripped_string
