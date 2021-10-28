"""Module: validation
This module contains functions related validating our downloaded articles if they're same as ones we require. It also
contains functions to get articles source name and create list of missed or duplicate articles.
"""

from difflib import SequenceMatcher
import pandas as pd
import pdftotext

from systematic_review import string_manipulation
from systematic_review import converter
from systematic_review import os_utils


def get_dataframe_column_as_list(dataframe: pd.DataFrame, column_name: str = 'primary_title'):
    """Get pandas dataframe column values as list.

    Parameters
    ----------
    dataframe : pd.DataFrame
        This is the dataframe which contains column whose details we want as list.
    column_name : str
        This is the name of the column.

    Returns
    -------
    list
        This is the list containing the dataframe one column values.

    """
    column_values_list = dataframe[column_name].to_list()
    return column_values_list


def get_missed_articles_list(original_article_list: list, downloaded_article_list: list) -> list:
    missed_articles_list = []
    for article_name in original_article_list:
        if article_name in set(downloaded_article_list):
            pass
        else:
            missed_articles_list.append(article_name)

    return missed_articles_list


def similarity_sequence_matcher(string_a: str, string_b: str) -> float:
    """Shows the percentage similarity between two strings like 0.9836065573770492 that means 98.35%

    Parameters
    ----------
    string_a : str
        This is first string
    string_b : str
        This is second string

    Returns
    -------
    float
        This is the result of SequenceMatcher Example 0.9836065573770492 that means 98.35%

    """
    return SequenceMatcher(None, string_a, string_b).ratio()


def calculate_percentage(value: float, total: float) -> float:
    """calculate percentage of value in total.

    Parameters
    ----------
    value : float
        It is input number, normally smaller than total.
    total : float
        It is the larger number from which we want to know percentage

    Returns
    -------
    float
        This is calculated percentage. Example 98.36065573770492 that means 98.35%

    """
    percentage = (value / total) * 100
    return percentage


def add_dict_element_with_count(dictionary: dict, key: str) -> dict:
    """It increase the value by checking the key of dictionary or initialise new key with value 1. Works as collections
    module default dict with value 1.

    Parameters
    ----------
    dictionary : dict
        This is the dictionary where we want to add element.
    key : str
        This is the key of dictionary {key: value}

    Returns
    -------
    dict
        This is the edited dict with new elements counts.

    """
    if key in dictionary.keys():
        dictionary[key] += 1
    else:
        dictionary[key] = 1
    return dictionary


def dict_from_list_with_element_count(input_list):
    """Put input list elements into dictionary with count.

    Parameters
    ----------
    input_list : list
        This is the list with elements with some duplicates present.

    Returns
    -------
    dict
        This is dictionary key as list elements and value as list each element count

    """
    output_dict = dict()
    for key in input_list:
        add_dict_element_with_count(output_dict, key)

    return output_dict


def compare_two_dict_members_via_percent_similarity(first_dict: dict, second_dict: dict) -> float:
    """Compare elements in 2 dictionaries and return percentage similarity.

    Parameters
    ----------
    first_dict : dict
        Example - first_dict = {'mixed':1, 'modified':1, 'fruit':1, 'fly':1, 'optimization':1}
    second_dict : dict
        Example - second_dict = {'mixed':1, 'modified':1, 'fruit':1, 'fly':1, 'optimization':1, 'algorithm': 1}

    Returns
    -------
    float
        This is percentage represented as decimal number. Example 98.36065573770492 that means 98.35%

    """
    similar_dict_keys_count = 0
    total_dict_keys_count = 0
    all_dict_keys = {**first_dict, **second_dict}
    for key, value in all_dict_keys.items():
        if key in first_dict and key in second_dict:
            if first_dict[key] == second_dict[key]:
                same_values_in_dict = (2 * first_dict[key])
                similar_dict_keys_count += same_values_in_dict
                total_dict_keys_count += same_values_in_dict
            else:
                diff = abs(first_dict[key] - second_dict[key])
                same_values_in_dict = first_dict[key] if first_dict[key] < second_dict[key] else second_dict[key]
                similar_dict_keys_count += same_values_in_dict
                total_dict_keys_count += (diff + same_values_in_dict)
        else:
            total_dict_keys_count += all_dict_keys[key]

    percent_similarity = calculate_percentage(similar_dict_keys_count, total_dict_keys_count)

    return percent_similarity


def compare_two_list_members_via_percent_similarity(words_list: list, boolean_membership_list: list) -> float:
    """Compare elements in 2 lists and return percentage similarity.

    Parameters
    ----------
    words_list : list
        This contains elements whose elements to be checked for similarity.
    boolean_membership_list : list
        This list contains True and False values.

    Returns
    -------
    float
        This is percentage represented as decimal number. Example 98.36065573770492 that means 98.35%

    """
    words_found_in_boolean_membership_list = 0
    length_of_words_list = len(words_list)

    for word_indicator in boolean_membership_list:
        if word_indicator:
            words_found_in_boolean_membership_list += 1

    percent_similarity = calculate_percentage(words_found_in_boolean_membership_list, length_of_words_list)
    return percent_similarity


def exact_words_checker_in_text(words_string: str, text_string: str) -> bool:
    """This checks for exact match of substring in string and return True or False based on success.

    Parameters
    ----------
    words_string : str
        This is the word we are searching for.
    text_string : str
        This is query string or lengthy text.

    Returns
    -------
    bool
        This returns True if exact words_string found in text_string else False.

    """
    words_list = string_manipulation.split_preprocess_string(words_string)
    words_list_length = len(words_list)
    words_list_end_element_index = words_list_length - 1

    words_set = set(words_list)
    # words_dict_membership = dict_from_list_with_element_count(words_list)

    text_list = string_manipulation.split_preprocess_string(text_string)

    validation_bool = False
    searching_flag = False

    for word_of_text in text_list:
        if searching_flag:
            if word_of_text == words_list[searching_index]:
                if searching_index == words_list_end_element_index:
                    validation_bool = True
                    return validation_bool
                searching_index += 1
            else:
                searching_flag = False

        if word_of_text in words_set:
            if word_of_text == words_list[0]:
                # starting_index = words_list.index(word_of_text)
                searching_flag = True
                searching_index = 1

    return validation_bool


def words_percentage_checker_in_text(words_string: str, text_string: str, validation_limit: float = 70) -> tuple:
    """This  checks for exact match of substring in string and return True or False based on success. It also returns
    matched word percentage.
    Limit: this doesn't work properly if words_string have duplicate words.

    Parameters
    ----------
    words_string : str
        This is the word we are searching for.
    text_string : str
        This is query string or lengthy text.
    validation_limit : float
        This is the limit on similarity of checked substring. Example - 0.5 will return true if half of word found same.

    Returns
    -------
    tuple
        This returns True if exact words_string found in text_string else False.
        This also returns matched substring percentage.

    """
    words_list = string_manipulation.split_preprocess_string(words_string)
    words_list_length = len(words_list)
    # words_list_end_element_index = words_list_length - 1

    words_set = set(words_list)
    # words_dict_membership = dict_from_list_with_element_count(words_list)

    text_list = string_manipulation.split_preprocess_string(text_string)

    temp_list = [False] * words_list_length
    validation_bool = False
    # searching_flag = False
    word_list_element_index = -1
    percentage_matched = 0

    for word_of_text in text_list:
        if word_of_text in words_set:
            word_of_text_index_in_words_list = words_list.index(word_of_text)

            if word_of_text_index_in_words_list > word_list_element_index:
                word_list_element_index = word_of_text_index_in_words_list
                temp_list[word_of_text_index_in_words_list] = True

                percentage_matched = compare_two_list_members_via_percent_similarity(words_list, temp_list)
                validation_bool = True if percentage_matched > validation_limit else False
                if validation_bool:
                    return validation_bool, percentage_matched

            else:
                temp_list = [False] * words_list_length
                temp_list[word_of_text_index_in_words_list] = True
        else:
            temp_list = [False] * words_list_length
            word_list_element_index = -1

    return validation_bool, percentage_matched


def jumbled_words_percentage_checker_in_text(words_string: str, text_string: str, validation_limit: float = 70,
                                             wrong_word_limit: int = 2) -> tuple:
    """start calculating percentage if half of words are found in sequence. This also takes in consideration of words
    which got jumbled up due to pdf reading operation.

    Parameters
    ----------
    words_string : str
        This is the word we are searching for.
    text_string : str
        This is query string or lengthy text.
    validation_limit : float
        This is the limit on similarity of checked substring. Example - 0.5 will return true if half of word found same.
    wrong_word_limit : int
        This is the limit unto which algorithm ignore the wrong word in sequence.

    Returns
    -------
    tuple
        This returns True if exact words_string found in text_string else False.
        This also returns matched substring percentage.

    """
    words_list = string_manipulation.split_preprocess_string(words_string)
    # words_list_length = len(words_list)
    # words_list_end_element_index = words_list_length - 1

    words_set = set(words_list)
    words_dict_membership = dict_from_list_with_element_count(words_list)

    text_list = string_manipulation.split_preprocess_string(text_string)

    validation_bool = False
    percentage_matched = 0
    skipped_words = 0

    temp_dict = dict()
    for word_of_text in text_list:
        if word_of_text in words_set:
            skipped_words = 0
            add_dict_element_with_count(temp_dict, word_of_text)
        else:
            skipped_words += 1
            if skipped_words >= wrong_word_limit:
                temp_dict = dict()
                continue
            percentage_matched = compare_two_dict_members_via_percent_similarity(words_dict_membership, temp_dict)
            validation_bool = True if percentage_matched > validation_limit else False
            if validation_bool:
                return validation_bool, percentage_matched
            temp_dict = dict()

    return validation_bool, percentage_matched


def validating_pdf_via_filename(pdf_file_path: str, pages: str = "first", method: str = "exact_words") -> bool:
    """This function checks name of file and find the name in the text of pdf file. if it become successful then pdf is
    validated as downloaded else not downloaded. Example - pdf file name -> check in -> text of pdf file. pdf_reader
    options are pdftotext or pymupdf.

    Parameters
    ----------
    pdf_file_path : str
        the path of the pdf file.
    pages : str
        This could be 'all' to get full text of pdf and 'first' for first page of pdf.
    method : str
        This is the switch option to select method from exact_words, words_percentage, jumbled_words_percentage.

    Returns
    -------
    bool
        True and False value depicting validated article with True value.

    """
    text = converter.get_text_from_pdf(pdf_file_path, pages)
    # print(text)
    pdf_filename = os_utils.get_filename_from_path(pdf_file_path)
    pdf_filename = string_manipulation.strip_string_from_right_side(pdf_filename)

    if method == "exact_words":
        validation_bool = exact_words_checker_in_text(pdf_filename, text)
    elif method == "words_percentage":
        validation_bool, percentage_matched = words_percentage_checker_in_text(pdf_filename, text)
    elif method == "jumbled_words_percentage":
        validation_bool, percentage_matched = jumbled_words_percentage_checker_in_text(pdf_filename, text)
    else:
        validation_bool = False
        print("Please properly write the method name, as method name is not available")

    return validation_bool


def multiple_methods_validating_pdf_via_filename(pdf_file_path: str, pages: str = "first",
                                                 pdf_reader: str = 'pdftotext') -> tuple:
    """This function checks name of file and find the name in the text of pdf file. if it become successful then pdf is
    validated as downloaded else not downloaded. Example - pdf file name -> check in -> text of pdf file. pdf_reader
    options are pdftotext or pymupdf.

    Parameters
    ----------
    pdf_reader : str
        This is python pdf reader package which convert pdf to text.
    pdf_file_path : str
        the path of the pdf file.
    pages : str
        This could be 'all' to get full text of pdf and 'first' for first page of pdf.

    Returns
    -------
    tuple
        True and False value depicting validated article with True value.
        This also shows percentage matched
        Last it shows the method used. like exact_words, words_percentage, jumbled_words_percentage, all if every method
        is executed to validate.

    """
    # percentage_matched = 0
    text = converter.get_text_from_pdf(pdf_file_path, pages, pdf_reader)
    # print(text)
    pdf_filename = os_utils.get_filename_from_path(pdf_file_path)

    validation_bool = exact_words_checker_in_text(pdf_filename, text)
    if validation_bool:
        return validation_bool, 1, "exact_words"
    validation_bool, percentage_matched = words_percentage_checker_in_text(pdf_filename, text)
    if validation_bool:
        return validation_bool, percentage_matched, "words_percentage"
    validation_bool, percentage_matched = jumbled_words_percentage_checker_in_text(pdf_filename, text)
    if validation_bool:
        return validation_bool, percentage_matched, "jumbled_words_percentage"

    # print(validation_bool)
    return False, percentage_matched, "all"


def validating_multiple_pdfs_via_filenames(list_of_pdf_files_path: list, pages: str = "first",
                                           pdf_reader: str = 'pdftotext') -> tuple:
    """This function checks pdf files in list_of_pdf_files_path and validate them with function named
    'validating_pdf_via_filename'. Example - multiple pdf file name -> check in -> text of pdf file.
    pdf_reader options are pdftotext or pymupdf.

    Parameters
    ----------
    pages : str
        This could be 'all' to get full text of pdf and 'first' for first page of pdf.
    pdf_reader : str
        This is python pdf reader package which convert pdf to text.
    list_of_pdf_files_path : list
        the list of the path of the pdf file.

    Returns
    -------
    tuple
        validated_pdf_list - contains name of pdf files whose filename is in the pdf text
        invalidated_pdf_list - list of name of files which can't be included in validated_pdf_list

    """
    validated_pdf_list = []
    invalidated_pdf_list = []
    manual_pdf_list = []

    for article_name_path in list_of_pdf_files_path:
        try:
            value, percentage_matched, methods = multiple_methods_validating_pdf_via_filename(article_name_path,
                                                                                              pages, pdf_reader)
            if value:
                # print("validated")
                validated_pdf_list.append([article_name_path, percentage_matched, methods])
            elif not value:
                # print("invalidated")
                invalidated_pdf_list.append([article_name_path, percentage_matched, methods])
        except pdftotext.Error:
            manual_pdf_list.append(article_name_path)

    return validated_pdf_list, invalidated_pdf_list, manual_pdf_list


def multiple_methods_validating_words_string_in_text(article_name: str, text: str) -> tuple:
    """This method uses different methods to validate the article_name(substring) in text. Example - exact_words,
    words_percentage, jumbled_words_percentage.

    Parameters
    ----------
    article_name : str
        This is input string which we want to validate in text.
    text : str
        This is query string or lengthy text.

    Returns
    -------
    tuple
        True and False value depicting validated article with True value.
        This also shows percentage matched
        Last it shows the method used. like exact_words, words_percentage, jumbled_words_percentage, all if every method
        is executed to validate.

    """
    # percentage_matched = 0
    validation_bool = exact_words_checker_in_text(article_name, text)
    if validation_bool:
        return validation_bool, 1, "exact_words"
    validation_bool, percentage_matched = words_percentage_checker_in_text(article_name, text)
    if validation_bool:
        return validation_bool, percentage_matched, "words_percentage"
    validation_bool, percentage_matched = jumbled_words_percentage_checker_in_text(article_name, text)
    if validation_bool:
        return validation_bool, percentage_matched, "jumbled_words_percentage"

    return validation_bool, percentage_matched, "all"


def finding_missed_articles_from_downloading(validated_pdf_list: list, original_articles_list: list) -> tuple:
    """Checks how many articles are not downloaded yet from original list of articles.

    Parameters
    ----------
    validated_pdf_list : list
        Contains name of pdf files whose filename is in the pdf text.
    original_articles_list : list
        This is original list from where we started downloading the articles.

    Returns
    -------
    tuple
        Missing_articles - these are the articles which are missed from downloading.
        Validated_articles - This is list of validated downloaded articles list.

    """
    validated_pdf_text = converter.list_to_string(validated_pdf_list)
    original_articles_set = set(original_articles_list)

    missing_articles = []
    downloaded_articles = []
    for article_name in original_articles_set:
        validation_bool, percentage_matched, methods = multiple_methods_validating_words_string_in_text(
            article_name, validated_pdf_text)
        if not validation_bool:
            missing_articles.append(article_name)
        elif validation_bool:
            downloaded_articles.append(article_name)
    return missing_articles, downloaded_articles


def manual_validating_of_pdf(articles_path_list: list, manual_index: int) -> tuple:
    """This is mostly a manually used function to validate some pdfs at the end of validation process. It makes it easy
    to search and validate pdf and store in a list.
    Advice: convert these lists as text file using function in converter module to avoid data loss.

    Parameters
    ----------
    articles_path_list : list
        These are the list of articles which skipped our automated screening and validation algorithms. mostly due to
        pdf to text conversions errors.
    manual_index : list
        This is the index from where you will start checking in article_path_list. Normally in many tries.

    Returns
    -------
    tuple
        external_validation_list - This is the list to be saved externally for validated articles.
        external_invalidated_list - This is the list to be saved externally for invalidated articles.

    """
    external_validation_list = []
    external_invalidated_list = []
    article_path = articles_path_list[manual_index]
    print(article_path)
    instructions = "Please provide 'y' to validate or 'n' to invalidate"
    manual_input = input(instructions).lower()
    if manual_input.lower() == "y":
        external_validation_list.append(article_path)
    elif manual_input.lower() == "n":
        external_invalidated_list.append(article_path)
    else:
        print("input should be 'y' or 'n'")
    manual_index += 1
    return external_validation_list, external_invalidated_list
