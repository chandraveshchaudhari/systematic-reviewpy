"""Module: filter_sort
Description for filter: each searched keywords group can be used to filter using conditions such as 
searched keywords >= some count values and filter them until you have required number of articles that can be manually read and filter.

Description for sort: This converts the data into sorted manner so it is easier for humans to understand.
"""

import pandas as pd
from systematic_review import converter


def get_pd_df_columns_names_with_prefix_suffix(input_pandas_dataframe: pd.DataFrame, common_word: str = "_count",
                                               method: str = "suffix") -> list:
    """Provide the columns name from pandas dataframe which contains given prefix or suffix.

    Parameters
    ----------
    input_pandas_dataframe : pd.DataFrame
        This dataframe contains many columns some of which contains the common word we are looking for.
    common_word : str
        This is the similar word string in many column names.
    method : str
        This is to specify if we are looking for prefix or suffix in column names.

    Returns
    -------
    list
        This list contains the name of columns which follow above criteria.

    """
    if method.lower() == "prefix":
        columns_name_df_index = input_pandas_dataframe.loc[:,
                                input_pandas_dataframe.columns.str.startswith(common_word)]
    elif method.lower() == "suffix":
        columns_name_df_index = input_pandas_dataframe.loc[:, input_pandas_dataframe.columns.str.endswith(common_word)]
    else:
        columns_name_df_index = []
        print("method is not available. Please input 'prefix' or 'suffix'.")
    columns_name_list = [column_name for column_name in columns_name_df_index]
    return columns_name_list


def filter_dataframe_on_keywords_group_name_count(citations_grouped_keywords_counts_df: pd.DataFrame, min_limit: int,
                                                  common_word: str = "_count", method: str = "suffix"):
    """This function gets  columns name from pandas dataframe which contains given prefix or suffix. It then filter
    dataframe to the point where all prefix and suffix column name have values more than min_limit.

    Parameters
    ----------
    citations_grouped_keywords_counts_df : pd.DataFrame
        This is input dataframe which contains some columns which have prefix or suffix in names.
    min_limit : int
        This is the least value we want in all keywords group names.
    common_word : str
        This is the similar word string in many column names.
    method : str
        This is to specify if we are looking for prefix or suffix in column names.

    Returns
    -------
    list
        This is the filtered citations list based on min_limit of grouped_keywords_counts.

    """
    filtered_list_of_dict = []
    keyword_group_name_list = get_pd_df_columns_names_with_prefix_suffix(citations_grouped_keywords_counts_df,
                                                                         common_word, method)
    citations_grouped_keywords_count_list = converter.convert_dataframe_to_list_of_dicts(
        citations_grouped_keywords_counts_df)

    for citation_dict in citations_grouped_keywords_count_list:
        more = True
        for keyword_group_name in keyword_group_name_list:
            if more:
                if citation_dict[keyword_group_name] < min_limit:
                    more = False

                if more is True and (keyword_group_name == keyword_group_name_list[-1]):
                    filtered_list_of_dict.append(citation_dict)
    return filtered_list_of_dict


def finding_required_article_by_changing_min_limit_recursively(citations_grouped_keywords_counts_df: pd.DataFrame,
                                                               required_number_of_articles: int,
                                                               addition: int = 0, search: bool = True,
                                                               prev_lower_total_articles_rows: int = 0):
    """This function increases the min_limit value to reach up to required_number_of_articles. this function return the
    min_limit value of exact required_number_of_articles can be extracted from dataframe else it provide the lower and
    upper limit of min_limit

    Parameters
    ----------
    citations_grouped_keywords_counts_df : pd.DataFrame
        This is input dataframe which contains some columns which have prefix or suffix in names.
    required_number_of_articles : int
        This is the number of articles you want after filtration process.
    addition : int
        This is the number by which you want to increase the min_limit on grouped keyword count.
    search : bool
        This signify the status of searching for best value of min_limit
    prev_lower_total_articles_rows : int
        This is the previous lower total articles rows

    Returns
    -------
    bool
        This prints the values rather than returning the values. It return search which is of no use.

    """
    if search is False:
        return search
    iteration = 0
    min_limit = addition + iteration

    while search:
        prev_min_limit = min_limit
        min_limit += 2 ** iteration

        filtered_list_of_dict = filter_dataframe_on_keywords_group_name_count(citations_grouped_keywords_counts_df,
                                                                              min_limit, "_count", "suffix")

        total_articles_rows = len(filtered_list_of_dict)
        print("min_limit: ", min_limit, "total_articles_rows: ", total_articles_rows)
        iteration += 1
        if total_articles_rows == required_number_of_articles:
            search = False
            return search

        elif total_articles_rows > required_number_of_articles:
            upper_total_articles_rows = total_articles_rows
            print("upper_total_articles_rows: ", upper_total_articles_rows)

        else:
            addition = prev_min_limit

            lower_total_articles_rows = total_articles_rows
            if prev_lower_total_articles_rows == lower_total_articles_rows:
                print("lower_total_articles_rows: ", lower_total_articles_rows)
                search = False
                return search
            return finding_required_article_by_changing_min_limit_recursively(citations_grouped_keywords_counts_df,
                                                                              required_number_of_articles, addition,
                                                                              search, lower_total_articles_rows)


def return_finding_required_article_by_changing_min_limit_recursively(
        citations_grouped_keywords_counts_df: pd.DataFrame,
        required_number_of_articles: int,
        addition: int = 0, search: bool = True,
        prev_lower_total_articles_rows: int = 0,
        upper_info=[None, None]):
    """This function increases the min_limit value to reach unto required_number_of_articles. this function return the
    min_limit value of exact required_number_of_articles can be extracted from dataframe else it provide the lower and
    upper limit of min_limit

    Parameters
    ----------
    citations_grouped_keywords_counts_df : pd.DataFrame
        This is input dataframe which contains some columns which have prefix or suffix in names.
    required_number_of_articles : int
        This is the number of articles you want after filtration process.
    addition : int
        This is the number by which you want to increase the min_limit on grouped keyword count.
    search : bool
        This signify the status of searching for best value of min_limit
    prev_lower_total_articles_rows : int
        This is the previous lower total articles rows
    upper_info : list
        This is list consists of [min_limit, upper_total_articles_rows]

    Returns
    -------
    tuple
        This tuple consists of following values in same order
        searching flag: True or False
        exact match values: min_limit, total_articles_rows
        lower_info : min_limit, lower_total_articles_rows
        upper_info : min_limit, upper_total_articles_rows

    """
    if search is False:
        return search, None, None, None
    iteration = 0
    min_limit = addition + iteration

    while search:
        prev_min_limit = min_limit
        min_limit += 2 ** iteration
        filtered_list_of_dict = filter_dataframe_on_keywords_group_name_count(citations_grouped_keywords_counts_df,
                                                                              min_limit, "_count", "suffix")
        total_articles_rows = len(filtered_list_of_dict)
        print("min_limit: ", min_limit, "total_articles_rows: ", total_articles_rows)
        iteration += 1
        if total_articles_rows == required_number_of_articles:
            search = False
            exact_info = [min_limit, total_articles_rows]
            return search, exact_info, None, None

        elif total_articles_rows > required_number_of_articles:
            upper_total_articles_rows = total_articles_rows
            upper_info = [min_limit, upper_total_articles_rows]
            print("upper_total_articles_rows: ", upper_total_articles_rows)
        else:
            addition = prev_min_limit
            lower_total_articles_rows = total_articles_rows
            if prev_lower_total_articles_rows == lower_total_articles_rows:
                lower_info = [min_limit, lower_total_articles_rows]
                print("lower_total_articles_rows: ", lower_total_articles_rows)
                search = False
                return search, None, lower_info, upper_info
            return return_finding_required_article_by_changing_min_limit_recursively(
                citations_grouped_keywords_counts_df,
                required_number_of_articles,
                addition, search,
                lower_total_articles_rows,
                upper_info)


def manually_check_filter_by_min_limit_changes(citations_grouped_keywords_counts_df: pd.DataFrame,
                                               required_number_of_articles: int, min_limit: int = 1,
                                               iterations: int = 20, addition: int = 20):
    """

    Parameters
    ----------
    citations_grouped_keywords_counts_df : pd.DataFrame
        This is input dataframe which contains some columns which have prefix or suffix in names.
    required_number_of_articles : int
        This is the number of articles you want after filtration process.
    min_limit : int
        This is the least value we want in all keywords group names.
    iterations : int
        This is the number of iterations in for underling loop.
    addition : int
        This is the number by which you want to increase the min_limit on grouped keyword count.

    Returns
    -------
    None
        This prints the values rather than returning the values.

    """
    for _ in range(iterations):
        filtered_list_of_dict = filter_dataframe_on_keywords_group_name_count(citations_grouped_keywords_counts_df,
                                                                              min_limit, "_count", "suffix")
        total_articles_rows = len(filtered_list_of_dict)
        print("min_limit: ", min_limit, "total_articles_rows: ", total_articles_rows)
        if total_articles_rows <= required_number_of_articles:
            break
        else:
            min_limit += addition


def get_sorting_criterion_list(citations_grouped_keywords_counts_df, unique_preprocessed_clean_grouped_keywords_dict):
    """This sorting criteria list is based on the keywords got from the main input keywords. It contains total_keywords,
    group_keywords_counts, keywords_counts.

    Parameters
    ----------
    citations_grouped_keywords_counts_df : pd.DataFrame
        This dataframe contains all columns with counts of keywords.
    unique_preprocessed_clean_grouped_keywords_dict : dict
        his is the dictionary comprised of unique keywords in each keyword groups. It means keyword from first keyword
        group can not be found in any other keyword group.
        Example - {'keyword_group_1': ["management", "investing", "risk", "pre", "process"], 'keyword_group_2':
        ["corporate", "pricing"],...}.
        'risk' is removed from keyword_group_2.

    Returns
    -------
    list
        This is the sorting criterion list which contains column in logical manner we desire. It contains
        total_keywords, group_keywords_counts, and keywords_counts in the last.

    """
    sorting_criterion_list = ["total_keywords"]
    group_name_counter_list = get_pd_df_columns_names_with_prefix_suffix(citations_grouped_keywords_counts_df)
    sorting_criterion_list.append(group_name_counter_list)
    for keywords_list in unique_preprocessed_clean_grouped_keywords_dict.values():
        sorting_criterion_list.append(keywords_list)
    return sorting_criterion_list


def sort_citations_grouped_keywords_counts_df(citations_grouped_keywords_counts_df: pd.DataFrame,
                                              sorting_criterion_list: list) -> pd.DataFrame:
    """This function sort the dataframe based on the sorting criterion list.

    Parameters
    ----------
    citations_grouped_keywords_counts_df : pd.DataFrame
        This dataframe contains all columns with counts of keywords.
    sorting_criterion_list : list
        This is the sorting criterion list which contains column in logical manner we desire.It contains
        total_keywords, group_keywords_counts, and keywords_counts in the last.

    Returns
    -------
    pd.DataFrame
        This is the sorted dataframe which contains columns in this sequential manner. It contains total_keywords,
    group_keywords_counts, and keywords_counts in the last.

    """
    available_sorting_criterion_list = []
    for word in sorting_criterion_list:
        if word in citations_grouped_keywords_counts_df.columns:
            available_sorting_criterion_list.append(word)

    sorted_df = citations_grouped_keywords_counts_df.sort_values(by=available_sorting_criterion_list, ascending=False)
    print(available_sorting_criterion_list)
    arranged_df = sorted_df[available_sorting_criterion_list]
    print(arranged_df)

    return arranged_df
