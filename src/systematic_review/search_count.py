"""Module: search_count
This module contains all necessary functions for searching the citations, articles text and count number of keywords
present.
"""

import pandas as pd
import json
from systematic_review import string_manipulation
from systematic_review import converter


def write_json_file_with_dict(output_file_path: str, input_dict: dict) -> None:
    """Write json file at output_file_path with the help of input dictionary.

    Parameters
    ----------
    output_file_path : str
        This is the path of output file we want, if only name is provided then it will export json to the script path.
    input_dict : dict
        This is the python dictionary which we want to be saved in json file format.

    Returns
    -------
    None
        Function doesn't return anything but write a json file at output_file_path.

    """
    with open(output_file_path, "w") as outfile:
        json.dump(input_dict, outfile)


def read_json_file_from_path(json_file_path: str) -> None:
    """Read the json file from the path given. Convert json file data to the python dictionary.

    Parameters
    ----------
    json_file_path : str
        This is the json file path which is needed to be converted.

    Returns
    -------
    dict
        This is the data in dict format converted from json file.

    """
    with open(json_file_path, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        return json_object


def get_sample_keywords_json(output_file_path: str = "sample_keywords_template.json") -> None:
    """Outputs the json sample keywords file template as example which can be edited by user to upload keywords.

    Parameters
    ----------
    output_file_path : str
        this is optional output file path for json template

    Returns
    -------
    None
        function create the file on the root folder unless specified in output_file_path

    """
    sample_dict = {'keywords_finance': 'Management investing corporate pricing risk', 'keywords_machine_learning':
                   'neural fuzzy inference system artificial intelligence artificial computational neural networks',
                   'keywords_common_words': 'accuracy classification cross sectional cross-section expected metrics '
                                            'prediction predict expert system'}
    write_json_file_with_dict(output_file_path, sample_dict)


def construct_search_keywords_dictionary(keywords_list: list, default_string: str = "keyword_group_") -> dict:
    """
    This takes keywords_list which contains keywords as ['keyword1 keyword2 keyword3', 'keyword1 keyword2']
    and function construct dict as {'keyword_group_1': 'keyword1 keyword2 keyword3',
    'keyword_group_2': 'keyword1 keyword2'}

    Parameters
    ----------
    keywords_list : list
        this is the list of keywords you want to be searched in the citations which can also be grouped based on
        similarities. Example - ['keyword1 keyword2 keyword3', 'keyword1 keyword2']
    default_string : str
        this is the default name of your keywords group which later changes by adding number suffix.
        Examples - keyword_group_1, keyword_group_2

    Returns
    -------
    dict
        the dictionary contains the group name and keywords paired as value
        Examples - {'keyword_group_1': 'keyword1 keyword2 keyword3', 'keyword_group_2': 'keyword1 keyword2'}

    """
    suffix = 1
    grouped_keywords_dictionary = {}
    for keywords in keywords_list:
        dictionary_key = default_string + str(suffix)
        grouped_keywords_dictionary[dictionary_key] = keywords

        suffix += 1
    return grouped_keywords_dictionary


def preprocess_search_keywords_dictionary(grouped_keywords_dictionary: dict) -> dict:
    """
    This takes keywords from {keyword_group_name: keywords,...} dict and remove symbols with spaces. it then convert
    them to lowercase and remove any duplicate keyword inside of keywords. outputs the {keyword_group_name:
    [clean_keywords],...}

    Parameters
    ----------
    grouped_keywords_dictionary : dict
        This is the input dictionary of keywords used for systematic review.
        Example - {'keyword_group_name': "Management investing corporate pricing risk Risk Pre-process",...}

    Returns
    -------
    dict
        This is output dictionary which contains processed non-duplicate keywords dict.
        Example - {'keyword_group_name': ["management", "investing", "corporate", "pricing", "risk", "pre",
        "process"],...}

    """
    preprocessed_clean_grouped_keywords_dictionary = {}
    for keyword_group_name, keywords in grouped_keywords_dictionary.items():
        preprocessed_string = string_manipulation.preprocess_string(keywords)
        preprocessed_clean_keywords = string_manipulation.split_words_remove_duplicates(preprocessed_string.split())
        preprocessed_clean_grouped_keywords_dictionary[keyword_group_name] = preprocessed_clean_keywords
    return preprocessed_clean_grouped_keywords_dictionary


def unique_keywords_in_preprocessed_clean_keywords_dict(preprocessed_clean_grouped_keywords_dict: dict) -> set:
    """Return set of unique keywords from the preprocessed_clean_keywords_dict.

    Parameters
    ----------
    preprocessed_clean_grouped_keywords_dict : dict
        This is output dictionary which contains processed non-duplicate keywords dict.
        Example - {'keyword_group_name': ["management", "investing", "corporate", "pricing", "risk", "pre",
        "process"],...}

    Returns
    -------
    set
        This is set of unique keywords from all of keywords groups.

    """
    unique_keywords = set()
    for keywords_list in preprocessed_clean_grouped_keywords_dict.values():
        for keywords in keywords_list:
            unique_keywords.add(keywords)
    return unique_keywords


def remove_duplicates_keywords_from_next_groups(preprocessed_clean_grouped_keywords_dict: dict) -> dict:
    """Remove duplicate instances of keywords in other keywords groups.

    Parameters
    ----------
    preprocessed_clean_grouped_keywords_dict : dict
        This is output dictionary which contains processed non-duplicate keywords dict.
        Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
        ["corporate", "pricing", "risk"],...}

    Returns
    -------
    dict
        This is the dictionary comprised of unique keywords in each keyword groups. It means keyword from first keyword
        group can not be found in any other keyword group.
        Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
        ["corporate", "pricing"],...}
        'risk' is removed from keyword_group_2.

    """
    unique_preprocessed_clean_grouped_keywords_dict = preprocessed_clean_grouped_keywords_dict
    temp_set = set()

    for keyword_group_name, grouped_unique_keywords in unique_preprocessed_clean_grouped_keywords_dict.items():
        # appending new keywords in temp_set
        for keywords in grouped_unique_keywords:
            if keywords not in temp_set:
                temp_set.add(keywords)
            else:
                unique_preprocessed_clean_grouped_keywords_dict[keyword_group_name].remove(keywords)
    return unique_preprocessed_clean_grouped_keywords_dict


def adding_dict_key_or_increasing_value(input_dict: dict, dict_key: str, step: int = 1, default_dict_value: int = 1):
    """Increase the value of dict(key:value) by step using key. If key not present then it get initialised with default
    dict value

    Parameters
    ----------
    input_dict : dict
        This is the dictionary which we want to modify.
    dict_key : str
        This is the key of dictionary
    step : int
        This is the addition number by which value of dictionary needed to be increased.
    default_dict_value : int
        If key is not available in dictionary then this default value is used to add new key.

    Returns
    -------
    dict
        This is the modified dictionary

    """
    if dict_key in input_dict.keys():
        input_dict[dict_key] += step
    else:
        input_dict[dict_key] = default_dict_value
    return input_dict


def count_keywords_in_citations_full_text(dataframe_citations_with_fulltext: pd.DataFrame,
                                          unique_preprocessed_clean_grouped_keywords_dict: dict,
                                          title_column_name: str = "title") -> list:
    """Loop over articles to calculate keywords counts

    Parameters
    ----------
    dataframe_citations_with_fulltext : pd.DataFrame
        This dataframe contains all the citations details with column named 'full_text' containing full text like
        article name, abstract and keyword.
    unique_preprocessed_clean_grouped_keywords_dict : dict
        looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                  'keyword_group_2': ["corporate", "pricing"],...}
    title_column_name : str
        This is the name of column which contain citation title

    Returns
    -------
    list
        This is the list of all citations search result which contains our all keywords count.
        Examples - [{'primary_title': 'name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    final_list_of_full_keywords_counts_citations_dict = []
    # iterating through each citation details one by one.
    for _, row in dataframe_citations_with_fulltext.iterrows():
        print(f"article: {row[title_column_name]}")
        full_keywords_counts_dict = {title_column_name: str(row[title_column_name])}
        total_keywords_counts = 0
        # taking words one by one from full_text of citation.
        for searched_word in string_manipulation.split_preprocess_string(row['full_text']):
            # checking the word in grouped keywords and add to full_keywords_count_dict.
            for keyword_group_name, unique_keywords in unique_preprocessed_clean_grouped_keywords_dict.items():
                for keyword in unique_keywords:
                    if searched_word == keyword:
                        total_keywords_counts += 1
                        group_name_count = str(keyword_group_name) + "_count"
                        full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                        group_name_count)
                        full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                        searched_word)

        full_keywords_counts_dict.update({"total_keywords": total_keywords_counts})
        final_list_of_full_keywords_counts_citations_dict.append(full_keywords_counts_dict)

    return final_list_of_full_keywords_counts_citations_dict


def count_keywords_in_pdf_full_text(list_of_downloaded_articles_path: list,
                                    unique_preprocessed_clean_grouped_keywords_dict: dict) -> list:
    """Loop over articles pdf files to calculate keywords counts.

    Parameters
    ----------
    list_of_downloaded_articles_path : list
        This list contains path of all the pdf files contained in directory_path.
    unique_preprocessed_clean_grouped_keywords_dict : dict
        looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                  'keyword_group_2': ["corporate", "pricing"],...}

    Returns
    -------
    list
        This is the list of all citations search result which contains our all keywords count.
        Examples - [{'article': 'article_name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    final_list_of_full_keywords_counts_pdf_text_dict = []
    # iterating through each pdf path one by one.
    for pdf_path in list_of_downloaded_articles_path:
        article_name = string_manipulation.cleaned_pdf_filename_from_filepath(pdf_path)
        print("article: ", article_name)
        full_keywords_counts_dict = {'article': str(article_name)}
        total_keywords_counts = 0

        try:
            pdf_text = converter.get_text_from_pdf(pdf_path)
        except FileNotFoundError:
            continue

        # taking words one by one from full_text of pdf file.
        for searched_word in string_manipulation.split_preprocess_string(pdf_text):
            # checking the word in grouped keywords and add to full_keywords_count_dict.
            for keyword_group_name, unique_keywords in unique_preprocessed_clean_grouped_keywords_dict.items():
                for keyword in unique_keywords:
                    if searched_word == keyword:
                        total_keywords_counts += 1
                        group_name_count = str(keyword_group_name) + "_count"
                        full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                        group_name_count)
                        full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                        searched_word)

        full_keywords_counts_dict.update({"total_keywords": total_keywords_counts})
        final_list_of_full_keywords_counts_pdf_text_dict.append(full_keywords_counts_dict)

    return final_list_of_full_keywords_counts_pdf_text_dict
