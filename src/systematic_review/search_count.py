"""Module: search_count
This module contains all necessary functions for searching the citations, articles text and count number of search_words_object
present.
"""

import pandas as pd
import json

from typing import List, Union

from systematic_review import string_manipulation, citation, filter_sort, validation, nlp
from systematic_review import converter


class SearchWords:
    sample_dict = {'keywords_finance': 'Management investing corporate pricing risk',
                   'keywords_machine_learning': 'neural fuzzy inference system artificial intelligence artificial '
                                                'computational neural networks',
                   'keywords_common_words': 'accuracy classification cross sectional cross-section expected metrics '
                                            'prediction predict expert system'}

    def __init__(self, search_words,
                 text_manipulation_method_name: str = "preprocess_string", custom_text_manipulation_function=None,
                 default_search_words_group_name: str = "search_words_group_", all_unique_keywords: bool = False,
                 unique_keywords: bool = True, *args, **kwargs):
        if args:
            self.args = args
        if kwargs:
            self.kwargs = kwargs
        self.all_unique_keywords = all_unique_keywords
        self.default_search_words_group_name = default_search_words_group_name
        self.custom_text_manipulation_function = custom_text_manipulation_function
        self.unique_keywords = unique_keywords
        self.text_manipulation_method_name = text_manipulation_method_name
        if type(search_words) == str:
            self.search_words_path = search_words
            self.value = self.preprocess_searched_keywords(converter.json_file_to_dict(self.search_words_path))
        elif type(search_words) == list:
            self.search_word_list = search_words
            self.value = self.preprocess_searched_keywords(self.construct_search_words_from_list())
        elif type(search_words) == dict:
            self.search_word_dict = search_words
            self.value = self.preprocess_searched_keywords(self.search_word_dict)
        else:
            print(f"search_words type {type(search_words)} is incorrect, It must be str, list, or dict.")

    def get_sample_search_words_json(self, output_file_path: str = "sample_search_words_template.json") -> None:
        """Outputs the json sample search_words_object file template as example which can be edited by user to upload search_words_object.

        Parameters
        ----------
        output_file_path : str
            this is optional output file path for json template

        Returns
        -------
        None
            function create the file on the root folder unless specified in output_file_path

        """

        converter.write_json_file_with_dict(output_file_path, self.sample_dict)

    def unique_keywords_in_preprocessed_clean_keywords_dict(self) -> set:
        """Return set of unique search_words_object from the preprocessed_clean_keywords_dict.

        Parameters
        ----------
        preprocessed_clean_grouped_keywords_dict : dict
            This is output dictionary which contains processed non-duplicate search_words_object dict.
            Example - {'keyword_group_name': ["management", "investing", "corporate", "pricing", "risk", "pre",
            "process"],...}

        Returns
        -------
        set
            This is set of unique search_words_object from all of search_words_object groups.

        """
        unique_keywords = set()
        for keywords_list in self.value.values():
            for keywords in keywords_list:
                unique_keywords.add(keywords)
        return unique_keywords

    def construct_search_words_from_list(self) -> dict:
        """
        This takes keywords_list which contains search_words_object as ['keyword1 keyword2 keyword3', 'keyword1 keyword2']
        and function construct dict as {'keyword_group_1': 'keyword1 keyword2 keyword3',
        'keyword_group_2': 'keyword1 keyword2'}

        Parameters
        ----------
        keywords_list : list
            this is the list of search_words_object you want to be searched in the citations which can also be grouped based on
            similarities. Example - ['keyword1 keyword2 keyword3', 'keyword1 keyword2']
        default_search_words_group_name : str
            this is the default name of your search_words_object group which later changes by adding number suffix.
            Examples - keyword_group_1, keyword_group_2

        Returns
        -------
        dict
            the dictionary contains the group name and search_words_object paired as value
            Examples - {'keyword_group_1': 'keyword1 keyword2 keyword3', 'keyword_group_2': 'keyword1 keyword2'}

        """
        suffix = 1
        grouped_keywords_dictionary = {}
        for keywords in self.search_word_list:
            dictionary_key = self.default_search_words_group_name + str(suffix)
            grouped_keywords_dictionary[dictionary_key] = keywords

            suffix += 1
        return grouped_keywords_dictionary

    def preprocess_search_keywords_dictionary(self, grouped_keywords_dictionary: dict) -> dict:
        """
        This takes search_words_object from {keyword_group_name: search_words_object,...} dict and remove symbols with spaces. it then convert
        them to lowercase and remove any duplicate keyword inside of search_words_object. outputs the {keyword_group_name:
        [clean_keywords],...}

        Parameters
        ----------
        custom_text_manipulation_function : function
            This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
            take text as parameter with no default preprocess_string operation.
        text_manipulation_method_name : str
            provides the options to use any text manipulation function.
            preprocess_string (default and applied before all other implemented functions)
            custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
            nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
            nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
        unique_keywords : bool
            provide option to make search_words_object in each groups unique.
        grouped_keywords_dictionary : dict
            This is the input dictionary of search_words_object used for systematic review.
            Example - {'keyword_group_name': "Management investing corporate pricing risk Risk Pre-process",...}

        Returns
        -------
        dict
            This is output dictionary which contains processed non-duplicate search_words_object dict.
            Example - {'keyword_group_name': ["management", "investing", "corporate", "pricing", "risk", "pre",
            "process"],...}

        """
        preprocessed_clean_grouped_keywords_dictionary = {}
        for keyword_group_name, keywords in grouped_keywords_dictionary.items():
            preprocessed_string = string_manipulation.text_manipulation_methods(keywords,
                                                                                self.text_manipulation_method_name,
                                                                                self.custom_text_manipulation_function,
                                                                                self.args, self.kwargs)
            preprocessed_clean_keywords = string_manipulation.split_words_remove_duplicates(
                preprocessed_string.split()) if \
                self.unique_keywords else preprocessed_string.split()
            preprocessed_clean_grouped_keywords_dictionary[keyword_group_name] = preprocessed_clean_keywords
        return preprocessed_clean_grouped_keywords_dictionary

    def preprocess_searched_keywords(self, grouped_keywords_dictionary: dict) -> dict:
        """Remove duplicate instances of search_words_object in other search_words_object groups.

        Parameters
        ----------
        custom : function
            This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
            take text as parameter with no default preprocess_string operation.
        text_manipulation_method_name : str
            provides the options to use any text manipulation function.
            preprocess_string (default and applied before all other implemented functions)
            custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
            nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
            nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma
        all_unique_keywords : bool
            provide option to make search_words_object in all groups unique.
        grouped_keywords_dictionary : dict
            This is the input dictionary of search_words_object used for systematic review.
            Example - {'keyword_group_name': "Management investing corporate pricing risk Risk Pre-process",...}

        Returns
        -------
        dict
            This is the dictionary comprised of unique search_words_object in each keyword groups. It means keyword from first keyword
            group can not be found in any other keyword group.
            Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
            ["corporate", "pricing"],...}
            'risk' is removed from keyword_group_2.

        """
        preprocessed_keywords = self.preprocess_search_keywords_dictionary(grouped_keywords_dictionary)
        preprocessed_clean_grouped_keywords_dict = self.remove_duplicates_keywords_from_next_groups(
            preprocessed_keywords) if \
            self.all_unique_keywords else preprocessed_keywords
        return preprocessed_clean_grouped_keywords_dict

    def remove_duplicates_keywords_from_next_groups(self, preprocessed_clean_grouped_keywords_dict: dict) -> dict:
        """Execute search_words_object step.
        This takes search_words_object from {keyword_group_name: search_words_object,...} dict and remove symbols with spaces. it then convert
        them to lowercase and remove any duplicate keyword inside of search_words_object. outputs the {keyword_group_name:
        [clean_keywords],...} and then Remove duplicate instances of search_words_object in other search_words_object groups.

        Parameters
        ----------
        preprocessed_clean_grouped_keywords_dict : dict
            This is output dictionary which contains processed non-duplicate search_words_object dict.
            Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
            ["corporate", "pricing", "risk"],...}

        Returns
        -------
        dict
            This is the dictionary comprised of unique search_words_object in each keyword groups. It means keyword from first keyword
            group can not be found in any other keyword group.
            Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
            ["corporate", "pricing"],...}
            'risk' is removed from keyword_group_2.

        """
        temp_set = set()
        temp_preprocessed_clean_grouped_keywords_dict = preprocessed_clean_grouped_keywords_dict.copy()
        for keyword_group_name, grouped_unique_keywords in preprocessed_clean_grouped_keywords_dict.items():
            # appending new search_words_object in temp_set
            for keywords in grouped_unique_keywords:
                if keywords not in temp_set:
                    temp_set.add(keywords)
                else:
                    temp_preprocessed_clean_grouped_keywords_dict[keyword_group_name].remove(keywords)
        return temp_preprocessed_clean_grouped_keywords_dict

    def creating_default_keyword_count_dict(self):
        """Initialise keyword count dict with value 0 for every keyword.

        Parameters
        ----------
        unique_preprocessed_clean_grouped_keywords_dict : dict
            looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                      'keyword_group_2': ["corporate", "pricing"],...}

        Returns
        -------
        dict
            This contains key as keyword and value as 0.

        """
        keyword_count_dict = {"total_keywords": 0}
        for group_name, keywords_list in self.value.items():
            group_name_count = str(group_name) + "_count"
            keyword_count_dict.update({group_name_count: 0})
            for keyword in keywords_list:
                keyword_count_dict.update({keyword: 0})
        return keyword_count_dict

    def get_sorting_keywords_criterion_list(self) -> List[str]:
        """This sorting criteria list is based on the search_words_object got from the main input search_words_object. It contains total_keywords,
        group_keywords_counts, keywords_counts.

        Parameters
        ----------
        unique_preprocessed_clean_grouped_keywords_dict : dict
            his is the dictionary comprised of unique search_words_object in each keyword groups. It means keyword from first keyword
            group can not be found in any other keyword group.
            Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
            ["corporate", "pricing"],...}.
            'risk' is removed from keyword_group_2.

        Returns
        -------
        List[str]
            This is the sorting criterion list which contains column in logical manner we desire. It contains
            total_keywords, group_keywords_counts, and search_words_object in the last.

        """
        sorting_keywords_criterion_list = ["total_keywords"]
        for keyword_group_name in self.value.keys():
            group_name_count = str(keyword_group_name) + "_count"
            sorting_keywords_criterion_list.append(group_name_count)

        for keywords_list in self.value.values():
            for keyword in keywords_list:
                sorting_keywords_criterion_list.append(keyword)
        return sorting_keywords_criterion_list

    def generate_keywords_count_dictionary(self, text):
        empty_keyword_count_dict = self.creating_default_keyword_count_dict()

        total_keywords_counts = 0
        for searched_word in text.split():
            # checking the word in grouped search_words_object and add to full_keywords_count_dict.
            for keyword_group_name, unique_keywords in self.value.items():
                if searched_word in unique_keywords:
                    total_keywords_counts += 1
                    group_name_count = str(keyword_group_name) + "_count"
                    empty_keyword_count_dict[group_name_count] += 1
                    empty_keyword_count_dict[searched_word] += 1

        empty_keyword_count_dict["total_keywords"] = total_keywords_counts

        return empty_keyword_count_dict


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


def count_words_in_list_of_lists(list_of_lists: list) -> dict:
    """count words in list containing other lists with words.

    Parameters
    ----------
    list_of_lists : list
        This list contains each element of type list.

    Returns
    -------
    dict
        dictionary with key as words and value as counts

    """
    dict_with_words_count = {}
    for keyword_list in list_of_lists:
        for keyword in keyword_list:
            clean_keyword = string_manipulation.preprocess_string(keyword)
            dict_with_words_count = adding_dict_key_or_increasing_value(dict_with_words_count, clean_keyword)

    return dict_with_words_count


def count_keywords_in_citations_text(dataframe_citations_with_fulltext: pd.DataFrame,
                                     unique_preprocessed_clean_grouped_keywords_dict: dict,
                                     title_column_name: str = "title",
                                     method: str = "preprocess_string", custom=None) -> list:
    """Loop over articles to calculate search_words_object counts

    Parameters
    ----------
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as
        custom_text_manipulation_function = function_name. it will take text as parameter with no default
        preprocess_string operation.
    method : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
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
        This is the list of all citations search result which contains our all search_words_object count.
        Examples - [{'primary_title': 'name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    final_list_of_full_keywords_counts_citations_dict = []
    keyword_count_dict = creating_default_keyword_count_dict(unique_preprocessed_clean_grouped_keywords_dict)
    # iterating through each citation details one by one.
    for _, row in dataframe_citations_with_fulltext.iterrows():
        print(f"article: {row[title_column_name]}")
        full_keywords_counts_dict = {title_column_name: str(row[title_column_name])}
        full_keywords_counts_dict.update(keyword_count_dict)

        total_keywords_counts = 0
        citation_full_text = text_manipulation_methods(row['full_text'], method, custom).split()
        # taking words one by one from full_text of citation.
        for searched_word in citation_full_text:
            # checking the word in grouped search_words_object and add to full_keywords_count_dict.
            for keyword_group_name, unique_keywords in unique_preprocessed_clean_grouped_keywords_dict.items():
                if searched_word in unique_keywords:
                    total_keywords_counts += 1
                    group_name_count = str(keyword_group_name) + "_count"
                    full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                    group_name_count)
                    full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                    searched_word)

        full_keywords_counts_dict.update({"total_keywords": total_keywords_counts})
        final_list_of_full_keywords_counts_citations_dict.append(full_keywords_counts_dict)

    return final_list_of_full_keywords_counts_citations_dict


def count_keywords_in_citations_full_text_list(citations_with_fulltext_list: list,
                                               unique_preprocessed_clean_grouped_keywords_dict: dict,
                                               title_column_name: str = "title",
                                               method: str = "preprocess_string", custom=None) -> list:
    """Loop over articles to calculate search_words_object counts

    Parameters
    ----------
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
        take text as parameter with no default preprocess_string operation.
    method : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
    citations_with_fulltext_list : list
        This list contains all the citations details with column named 'full_text' containing full text like
        article name, abstract and keyword.
    unique_preprocessed_clean_grouped_keywords_dict : dict
        looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                  'keyword_group_2': ["corporate", "pricing"],...}
    title_column_name : str
        This is the name of column which contain citation title

    Returns
    -------
    list
        This is the list of all citations search result which contains our all search_words_object count.
        Examples - [{'primary_title': 'name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    final_list_of_full_keywords_counts_citations_dict = []
    keyword_count_dict = creating_default_keyword_count_dict(unique_preprocessed_clean_grouped_keywords_dict)
    # iterating through each citation details one by one.
    for citation_dict in citations_with_fulltext_list:
        print(f"article: {citation_dict[title_column_name]}")
        full_keywords_counts_dict = citation_dict
        full_keywords_counts_dict.update(keyword_count_dict)

        total_keywords_counts = 0
        citation_full_text = text_manipulation_methods(citation_dict['citation_text'], method, custom).split()
        # taking words one by one from full_text of citation.
        for searched_word in citation_full_text:
            # checking the word in grouped search_words_object and add to full_keywords_count_dict.
            for keyword_group_name, unique_keywords in unique_preprocessed_clean_grouped_keywords_dict.items():
                if searched_word in unique_keywords:
                    total_keywords_counts += 1
                    group_name_count = str(keyword_group_name) + "_count"
                    full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                    group_name_count)
                    full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                    searched_word)

        full_keywords_counts_dict.update({"total_keywords": total_keywords_counts})
        final_list_of_full_keywords_counts_citations_dict.append(full_keywords_counts_dict)

    return final_list_of_full_keywords_counts_citations_dict


def count_search_words_in_citations_text(citations_with_fulltext_list: list,
                                         search_words_object: SearchWords,
                                         text_column_name: str = "'citation_text'",
                                         text_manipulation_method_name: str = "preprocess_string", custom=None,
                                         custom_text_manipulation_function=None, *args, **kwargs) -> list:
    """Loop over articles to calculate search_words_object counts

    Parameters
    ----------
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
        take text as parameter with no default preprocess_string operation.
    text_manipulation_method_name : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
    citations_with_fulltext_list : list
        This list contains all the citations details with column named 'full_text' containing full text like
        article name, abstract and keyword.
    search_words_object : object
        looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                  'keyword_group_2': ["corporate", "pricing"],...}
    text_column_name : str
        This is the name of column which contain citation text

    Returns
    -------
    list
        This is the list of all citations search result which contains our all search_words_object count.
        Examples - [{'primary_title': 'name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    final_list_of_full_search_words_counts_citations_dict = []

    # iterating through each citation details one by one.
    for citation_dict in citations_with_fulltext_list:
        # changing the text string based on text manipulation text_manipulation_method_name name
        text = string_manipulation.text_manipulation_methods(citation_dict[text_column_name],
                                                             text_manipulation_method_name,
                                                             custom_text_manipulation_function,
                                                             args, kwargs)

        # taking words one by one from full_text of citation.
        search_words_counts_dict = search_words_object.generate_keywords_count_dictionary(text)
        # adding citations with search_words_counts
        full_search_words_counts_dict = {**citation_dict, **search_words_counts_dict}
        # putting citation record in final_list_of_full_search_words_counts_citations_dict
        final_list_of_full_search_words_counts_citations_dict.append(full_search_words_counts_dict)

    return final_list_of_full_search_words_counts_citations_dict


def citation_list_of_dict_search_count_to_df(citations_list: list, keywords: dict, title_column_name: str = "title",
                                             method: str = "preprocess_string", custom=None) -> pd.DataFrame:
    """Loop over articles to calculate search_words_object counts and return dataframe.

    Parameters
    ----------
    title_column_name : str
        This is the name of column which contain citation title
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
        take text as parameter with no default preprocess_string operation.
    method : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
    citations_list : list
        list with additional columns needed for next steps of systematic review and duplicates are removed
    keywords : dict
        This is output dictionary which contains processed non-duplicate search_words_object dict.
        Example - {'keyword_group_name': ["management", "investing", "corporate", "pricing", "risk", "pre",
        "process"],...}

    Returns
    -------
    pandas.DataFrame object
        This is pandas object of all citations search result which contains our all search_words_object count.
        Examples - [{'primary_title': 'name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    citations_keywords_count_list = count_keywords_in_citations_full_text_list(citations_list, keywords,
                                                                               title_column_name, method, custom)
    citation_search_count_df = converter.list_of_dicts_to_dataframe(citations_keywords_count_list)
    return citation_search_count_df


def citation_search_count_dataframe(citations_df: pd.DataFrame, keywords: dict, title_column_name: str = "title",
                                    method: str = "preprocess_string", custom=None) -> pd.DataFrame:
    """Loop over articles to calculate search_words_object counts and return dataframe.

    Parameters
    ----------
    title_column_name : str
        This is the name of column which contain citation title
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
        take text as parameter with no default preprocess_string operation.
    method : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
    citations_df : pandas.DataFrame object
        DataFrame with additional columns needed for next steps of systematic review and duplicates are removed
    keywords : dict
        This is output dictionary which contains processed non-duplicate search_words_object dict.
        Example - {'keyword_group_name': ["management", "investing", "corporate", "pricing", "risk", "pre",
        "process"],...}

    Returns
    -------
    pandas.DataFrame object
        This is pandas object of all citations search result which contains our all search_words_object count.
        Examples - [{'primary_title': 'name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    citations_keywords_count_list = count_keywords_in_citations_text(citations_df, keywords, title_column_name,
                                                                     method, custom)
    citation_search_count_df = converter.list_of_dicts_to_dataframe(citations_keywords_count_list)
    return citation_search_count_df


def count_keywords_in_research_papers_text(list_of_downloaded_articles_path: list,
                                           unique_preprocessed_clean_grouped_keywords_dict: dict,
                                           title_column_name: str = "cleaned_title_pdf",
                                           method: str = "preprocess_string", custom=None) -> list:
    """Loop over articles pdf files to calculate search_words_object counts.

    Parameters
    ----------
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
        take text as parameter with no default preprocess_string operation.
    method : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
    title_column_name : str
        This is the name of column which contain citation title
    list_of_downloaded_articles_path : list
        This list contains path of all the pdf files contained in directory_path.
    unique_preprocessed_clean_grouped_keywords_dict : dict
        looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                  'keyword_group_2': ["corporate", "pricing"],...}

    Returns
    -------
    list
        This is the list of all citations search result which contains our all search_words_object count.
        Examples - [{'article': 'article_name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    final_list_of_full_keywords_counts_pdf_text_dict = []
    keyword_count_dict = creating_default_keyword_count_dict(unique_preprocessed_clean_grouped_keywords_dict)
    # iterating through each pdf path one by one.
    for pdf_path in list_of_downloaded_articles_path:
        article_name = string_manipulation.preprocess_string_to_space_separated_words(
            string_manipulation.pdf_filename_from_filepath(pdf_path))
        print("article: ", article_name)
        full_keywords_counts_dict = {title_column_name: str(article_name)}
        full_keywords_counts_dict.update(keyword_count_dict)
        total_keywords_counts = 0

        try:
            pdf_text = converter.get_text_from_multiple_pdf_reader(pdf_path)
        except FileNotFoundError:
            continue

        pdf_full_text = text_manipulation_methods(pdf_text, method, custom).split()
        # taking words one by one from full_text of pdf file.
        for searched_word in pdf_full_text:
            # checking the word in grouped search_words_object and add to full_keywords_count_dict.
            for keyword_group_name, unique_keywords in unique_preprocessed_clean_grouped_keywords_dict.items():
                if searched_word in unique_keywords:
                    total_keywords_counts += 1
                    group_name_count = str(keyword_group_name) + "_count"
                    full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                    group_name_count)
                    full_keywords_counts_dict = adding_dict_key_or_increasing_value(full_keywords_counts_dict,
                                                                                    searched_word)

        full_keywords_counts_dict.update({"total_keywords": total_keywords_counts})
        final_list_of_full_keywords_counts_pdf_text_dict.append(full_keywords_counts_dict)

    return final_list_of_full_keywords_counts_pdf_text_dict


def count_search_words_in_research_paper_text(list_of_downloaded_articles_path: list,
                                              unique_preprocessed_clean_grouped_keywords_dict: dict,
                                              title_column_name: str = "cleaned_title_pdf",
                                              method: str = "preprocess_string", custom=None) -> list:
    """Loop over articles pdf files to calculate search_words_object counts.

    Parameters
    ----------
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
        take text as parameter with no default preprocess_string operation.
    method : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
    title_column_name : str
        This is the name of column which contain citation title
    list_of_downloaded_articles_path : list
        This list contains path of all the pdf files contained in directory_path.
    unique_preprocessed_clean_grouped_keywords_dict : dict
        looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                  'keyword_group_2': ["corporate", "pricing"],...}

    Returns
    -------
    list
        This is the list of all citations search result which contains our all search_words_object count.
        Examples - [{'article': 'article_name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    final_list_of_full_keywords_counts_pdf_text_dict = []
    keyword_count_dict = creating_default_keyword_count_dict(unique_preprocessed_clean_grouped_keywords_dict)

    # iterating through each research paper file path one by one.
    for pdf_path in list_of_downloaded_articles_path:
        article_name = string_manipulation.preprocess_string_to_space_separated_words(
            string_manipulation.pdf_filename_from_filepath(pdf_path))

        try:
            text = converter.get_text_from_multiple_pdf_reader(pdf_path)
        except FileNotFoundError:
            final_list_of_full_keywords_counts_pdf_text_dict.append(keyword_count_dict)
            continue

        text = text_manipulation_methods(text, method, custom)
        # taking words one by one from text of research paper file and building count dictionary.
        full_keywords_counts_dict = generate_keywords_count_dictionary(unique_preprocessed_clean_grouped_keywords_dict,
                                                                       text)
        final_list_of_full_keywords_counts_pdf_text_dict.append(full_keywords_counts_dict)

    return final_list_of_full_keywords_counts_pdf_text_dict


def pdf_full_text_search_count_dataframe(list_of_downloaded_articles_path: list,
                                         unique_preprocessed_clean_grouped_keywords_dict: dict,
                                         title_column_name: str = "cleaned_title",
                                         method: str = "preprocess_string", custom=None
                                         ) -> pd.DataFrame:
    """Loop over articles pdf files to calculate search_words_object counts.

    Parameters
    ----------
    custom : function
        This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
        take text as parameter with no default preprocess_string operation.
    method : str
        provides the options to use any text manipulation function.
        preprocess_string (default and applied before all other implemented functions)
        custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
        nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
        nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
    title_column_name : str
        This is the name of column which contain citation title
    list_of_downloaded_articles_path : list
        This list contains path of all the pdf files contained in directory_path.
    unique_preprocessed_clean_grouped_keywords_dict : dict
        looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                  'keyword_group_2': ["corporate", "pricing"],...}

    Returns
    -------
    pandas.DataFrame object
        This is the dataframe of all citations search result which contains our all search_words_object count.
        Examples - [{'article': 'article_name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]

    """
    pdf_full_text_keywords_count_list = count_keywords_in_research_paper_text(list_of_downloaded_articles_path,
                                                                              unique_preprocessed_clean_grouped_keywords_dict,
                                                                              title_column_name, method, custom)
    pdf_full_text_search_count_df = converter.list_of_dicts_to_dataframe(pdf_full_text_keywords_count_list)
    return pdf_full_text_search_count_df


def adding_citation_details_with_keywords_count_in_pdf_full_text(filter_sorted_citations_df: pd.DataFrame,
                                                                 pdf_full_text_search_count: list,
                                                                 unique_preprocessed_clean_grouped_keywords_dict: dict,
                                                                 first_column_name: str = "cleaned_title",
                                                                 second_column_name: str =
                                                                 'cleaned_title_pdf') -> pd.DataFrame:
    """Combining the pdf search_words_object counts with the citation details from filtered and sorted citation full text
    dataframe.

    Parameters
    ----------
    second_column_name : str
        This is the name of column which contain pdf article title.
    first_column_name : str
        This is the name of column which contain citation title.
    filter_sorted_citations_df : pandas.DataFrame object
        This is the sorted dataframe which contains columns in this sequential manner. It contains citation df,
         total_keywords, group_keywords_counts, and keywords_counts in the last.
    pdf_full_text_search_count : list
        This is the list of all citations search result which contains our all search_words_object count.
        Examples - [{'article': 'article_name', 'total_keywords': count, 'keyword_group_1_count': count,
        "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
        "pricing": count,...}]
    unique_preprocessed_clean_grouped_keywords_dict : dict
        This is the dictionary comprised of unique search_words_object in each keyword groups. It means keyword from first keyword
        group can not be found in any other keyword group.
        Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
        ["corporate", "pricing"],...}.
        'risk' is removed from keyword_group_2.

    Returns
    -------
    pandas.DataFrame object
        This dataframe contains citations details from filtered and sorted citation full text dataframe and search_words_object
        counts from searching in pdf file text.

    """
    criteria_list = filter_sort.get_sorting_keywords_criterion_list(unique_preprocessed_clean_grouped_keywords_dict)
    filter_sorted_citations_details = filter_sorted_citations_df.drop(columns=criteria_list)

    citations_list = converter.dataframe_to_records_list(filter_sorted_citations_details)
    matched_list, unmatched_list = deep_validate_column_details_between_two_record_list(citations_list,
                                                                                        pdf_full_text_search_count,
                                                                                        first_column_name,
                                                                                        second_column_name)
    final_review_df = converter.list_of_dicts_to_dataframe(matched_list)

    return final_review_df


class SearchCount:
    def __init__(self, data: Union[List[dict], pd.DataFrame], search_words_object: SearchWords,
                 text_manipulation_method_name: str = "preprocess_string"):

        self.data = converter.dataframe_to_records_list(data) if type(data) == pd.DataFrame else data
        self.text_manipulation_method_name = text_manipulation_method_name
        self.search_words_object = search_words_object

    def check_data(self):
        if self.data:


    def count_search_words_in_research_paper_text(self, list_of_downloaded_articles_path: list,
                                                  unique_preprocessed_clean_grouped_keywords_dict: dict,
                                                  title_column_name: str = "cleaned_title_pdf",
                                                  method: str = "preprocess_string", custom=None) -> list:
        """Loop over articles pdf files to calculate search_words_object counts.

        Parameters
        ----------
        custom : function
            This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
            take text as parameter with no default preprocess_string operation.
        method : str
            provides the options to use any text manipulation function.
            preprocess_string (default and applied before all other implemented functions)
            custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
            nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
            nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
        title_column_name : str
            This is the name of column which contain citation title
        list_of_downloaded_articles_path : list
            This list contains path of all the pdf files contained in directory_path.
        unique_preprocessed_clean_grouped_keywords_dict : dict
            looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                      'keyword_group_2': ["corporate", "pricing"],...}

        Returns
        -------
        list
            This is the list of all citations search result which contains our all search_words_object count.
            Examples - [{'article': 'article_name', 'total_keywords': count, 'keyword_group_1_count': count,
            "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
            "pricing": count,...}]

        """
        final_list_of_full_keywords_counts_pdf_text_dict = []
        keyword_count_dict = creating_default_keyword_count_dict(unique_preprocessed_clean_grouped_keywords_dict)

        # iterating through each research paper file path one by one.
        for pdf_path in list_of_downloaded_articles_path:
            article_name = string_manipulation.preprocess_string_to_space_separated_words(
                string_manipulation.pdf_filename_from_filepath(pdf_path))

            try:
                text = converter.get_text_from_multiple_pdf_reader(pdf_path)
            except FileNotFoundError:
                final_list_of_full_keywords_counts_pdf_text_dict.append(keyword_count_dict)
                continue

            text = string_manipulation.text_manipulation_methods(text, method, custom)
            # taking words one by one from text of research paper file and building count dictionary.
            full_keywords_counts_dict = generate_keywords_count_dictionary(
                unique_preprocessed_clean_grouped_keywords_dict,
                text)
            final_list_of_full_keywords_counts_pdf_text_dict.append(full_keywords_counts_dict)

        return final_list_of_full_keywords_counts_pdf_text_dict

    def count_search_words_in_citations_text(self, citations_with_fulltext_list: list,
                                             search_words_object: SearchWords,
                                             text_column_name: str = "'citation_text'",
                                             text_manipulation_method_name: str = "preprocess_string", custom=None,
                                             custom_text_manipulation_function=None, *args, **kwargs) -> list:
        """Loop over articles to calculate search_words_object counts

        Parameters
        ----------
        custom : function
            This is optional custom_text_manipulation_function function if you want to implement this yourself. pass as custom_text_manipulation_function = function_name. it will
            take text as parameter with no default preprocess_string operation.
        text_manipulation_method_name : str
            provides the options to use any text manipulation function.
            preprocess_string (default and applied before all other implemented functions)
            custom_text_manipulation_function - for putting your custom_text_manipulation_function function to preprocess the text
            nltk_remove_stopwords, pattern_lemma_or_lemmatize_text, nltk_word_net_lemmatizer, nltk_porter_stemmer,
            nltk_lancaster_stemmer, spacy_lemma, nltk_remove_stopwords_spacy_lemma, convert_string_to_lowercase
        citations_with_fulltext_list : list
            This list contains all the citations details with column named 'full_text' containing full text like
            article name, abstract and keyword.
        search_words_object : object
            looks like this {'keyword_group_1': ["management", "investing", "risk", "pre", "process"],
                      'keyword_group_2': ["corporate", "pricing"],...}
        text_column_name : str
            This is the name of column which contain citation text

        Returns
        -------
        list
            This is the list of all citations search result which contains our all search_words_object count.
            Examples - [{'primary_title': 'name', 'total_keywords': count, 'keyword_group_1_count': count,
            "management": count, "investing: count", "risk: count", 'keyword_group_2_count': count, "corporate": count,
            "pricing": count,...}]

        """
        final_list_of_full_search_words_counts_citations_dict = []

        # iterating through each citation details one by one.
        for citation_dict in citations_with_fulltext_list:
            # changing the text string based on text manipulation text_manipulation_method_name name
            text = string_manipulation.text_manipulation_methods(citation_dict[text_column_name],
                                                                 text_manipulation_method_name,
                                                                 custom_text_manipulation_function,
                                                                 args, kwargs)

            # taking words one by one from full_text of citation.
            search_words_counts_dict = search_words_object.generate_keywords_count_dictionary(text)
            # adding citations with search_words_counts
            full_search_words_counts_dict = {**citation_dict, **search_words_counts_dict}
            # putting citation record in final_list_of_full_search_words_counts_citations_dict
            final_list_of_full_search_words_counts_citations_dict.append(full_search_words_counts_dict)

        return final_list_of_full_search_words_counts_citations_dict

    def get_records_list(self):
        pass

    def get_dataframe(self):
        pass
