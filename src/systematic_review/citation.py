"""Module: citation
This module contains functions which changes format or get details from citations. It also include functions to fix some
typos.
"""

import re
import pandas as pd
from systematic_review import string_manipulation
from systematic_review import converter


def csv_citations_to_ris_converter(input_file_path: str, output_filename: str = "output_ris_file.ris",
                                   input_file_type: str = "csv") -> None:
    """
    This asks for columns name from csv and then convert the csv to ris format.

    Parameters
    ----------
    input_file_path : str
        this is the path of input file
    output_filename : str
        this is the name of the output ris file with extension. output file path is also valid choice.
    input_file_type : str
        this function default is csv but excel is also supported by putting 'excel'

    Returns
    -------
    None

    """
    if input_file_type == 'excel':
        df = pd.read_excel(input_file_path)
    else:
        df = pd.read_csv(input_file_path)

    pd.set_option("display.max_columns", None)
    print(df.head())
    print("please specify columns of following in input file:")
    article_type = input("specify the type of given citations. if it's journal article, input :JOUR")
    authors = input("provide name of authors column")
    publication_year = input("provide name of Publication Year column")
    item_title = input("provide name of Item Title column")
    publication_title = input("provide name of Publication Title column")
    journal_volume = input("provide name of Journal Volume column")
    journal_issue = input("provide name of Journal Issue column")
    url = input("provide name of URL column")
    doi = input("provide name of Item DOI column")

    number_of_records = len(df)
    output_file = open(output_filename, "a")
    for index in range(number_of_records):
        output_file.write(f"TY  - {article_type}\n")
        output_file.write("AU  - " + str(df.iloc[index][authors]) + "\n")
        output_file.write("PY  - " + str(df.iloc[index][publication_year]) + "\n")
        output_file.write("TI  - " + str(df.iloc[index][item_title]) + "\n")
        output_file.write("JO  - " + str(df.iloc[index][publication_title]) + "\n")
        output_file.write("VL  - " + str(df.iloc[index][journal_volume]) + "\n")
        output_file.write("IS  - " + str(df.iloc[index][journal_issue]) + "\n")
        output_file.write("UR  - " + str(df.iloc[index][url]) + "\n")
        output_file.write("DO  - " + str(df.iloc[index][doi]) + "\n")
        output_file.write("ER -" + "\n")
        # \n is placed to indicate EOL (End of Line)
    output_file.close()
    print("ris file has been generated")


def remove_empty_lines(input_file_path: str, output_filename: str = "output_file.ris") -> None:
    """
    This function removes the blank lines from the input file and output new file.

    Parameters
    ----------
    input_file_path : str
        this is the path of input file
    output_filename : str
        this is the name of the output ris file with extension.

    Returns
    -------
    None

    """
    input_file = open(input_file_path, "r")
    output_file = open(output_filename, "a")
    for line in input_file:
        if line != "\n":
            output_file.write(line)
    input_file.close()
    output_file.close()


def edit_ris_citation_paste_values_after_regex_pattern(input_file_path: str, output_filename: str = "output_file.ris",
                                                       edit_line_regex: str = r'^DO ', paste_value: str = "ER  - ") \
        -> None:
    """
    This is created to edit ris files which doesn't specify ER for 'end of citations' and paste ER after end point of
    citation, replace 'DO' with other ris classifiers such as TY, JO etc.

    Parameters
    ----------
    input_file_path : str
        this is the path of input file
    output_filename : str
        this is the name of the output ris file with extension.
    edit_line_regex : str
        this is the regex to find ris classifiers lines such as DO, TY, JO etc.
    paste_value : str
        this is value to be pasted, most helpful is ER ris classifier which signify citation end.

    Returns
    -------
    None

    """
    input_file = open(input_file_path, "r")
    output_file = open(output_filename, "a")
    for line in input_file:
        output_file.write(line)
        if re.match(edit_line_regex, line):
            output_file.write(f"{paste_value}\n")

    input_file.close()
    output_file.close()


def add_citation_text_column(dataframe_object: pd.DataFrame, title_column_name: str = "title",
                             abstract_column_name: str = "abstract",
                             keyword_column_name: str = "keywords") -> pd.DataFrame:
    """This takes dataframe of citations and return the full text comprises of "title", "abstract", "keywords"

    Parameters
    ----------
    dataframe_object : pandas.DataFrame object
        this is the object of famous python library pandas. for more lemma_info: https://pandas.pydata.org/docs/
    title_column_name : str
        This is the name of column which contain citation title
    abstract_column_name : str
        This is the name of column which contain citation abstract
    keyword_column_name : str
        This is the name of column which contain citation keywords

    Returns
    -------
    pd.DataFrame
        this is dataframe_object comprises of full text column.

    """
    dataframe_object["full_text"] = dataframe_object[title_column_name].astype(str) + " " + dataframe_object[
        abstract_column_name].astype(str) + " " + dataframe_object[keyword_column_name].astype(str)

    return dataframe_object


def get_details_via_article_name_from_citations(article_name: str, sources_name_citations_path_list_of_dict: list,
                                                doi_url: bool = False, title_column_name: str = "title") -> dict:
    """Iterate through citations and find article_name and put source_name in column, with doi and url being optional

    Parameters
    ----------
    article_name : str
        This is the primary title of the citation or name of the article.
    sources_name_citations_path_list_of_dict : list
        This is the list of all the sources names and it's citations at dir_path.
        Examples - {'sources_name': 'all source articles citations', ...}
    doi_url : bool
        This signify if we want to get the value of url and doi from citation
    title_column_name : str
        This is the name of column which contain citation title

    Returns
    -------
    dict
        This dict contains the article_name, source_name and optional url and doi

    """
    for citations in sources_name_citations_path_list_of_dict[1]:
        if article_name == string_manipulation.preprocess_string(citations[title_column_name]):
            article_title_source_name_dict = {"article_name": article_name,
                                              "source_name": sources_name_citations_path_list_of_dict[0]}
            if doi_url:
                # optional block if you want url and doi
                try:
                    article_title_source_name_dict["doi"] = citations["doi"]
                    article_title_source_name_dict["url"] = citations["url"]
                except KeyError:
                    print("doi or url not present")
                    pass

            return article_title_source_name_dict


def get_details_of_all_article_name_from_citations(filtered_list_of_dict: list,
                                                   sources_name_citations_path_list_of_dict: list,
                                                   doi_url: bool = False, title_column_name: str = "title"):
    """This function searches source names, doi, and url for all articles in filtered_list_of_dict.

    Parameters
    ----------
    filtered_list_of_dict : list
        This is the list of article citations dict after filtering it using min_limit on grouped_keywords_count
    sources_name_citations_path_list_of_dict : list
        This is the list of all the sources names and it's citations at dir_path.
        Examples - {'sources_name': 'all source articles citations', ...}
    doi_url : bool
        This signify if we want to get the value of url and doi from citation
    title_column_name : str
        This is the name of column which contain citation title

    Returns
    -------
    list
        This list contains all article names with source names. (optional url and doi)

    """
    all_articles_title_source_name_list_of_dict = []

    for article_details in filtered_list_of_dict:
        article_name = article_details[title_column_name]
        print("article: ", article_name)
        articles_title_source_name_dict = get_details_via_article_name_from_citations(
            article_name, sources_name_citations_path_list_of_dict, doi_url)
        all_articles_title_source_name_list_of_dict.append(articles_title_source_name_dict)

    return all_articles_title_source_name_list_of_dict


def get_missed_articles_source_names(missed_articles_list: list, all_articles_title_source_name_list_of_dict: list,
                                     article_column_name: str = "article_name",
                                     source_column_name: str = "source_name") -> list:
    """

    Parameters
    ----------
    missed_articles_list : list
        This contains the list of articles that got missed while downloading.
    all_articles_title_source_name_list_of_dict : list
        This list contains all article names with source names. (optional url and doi)
    article_column_name : str
        This is the name of article column in the all_articles_title_source_name_list_of_dict.
    source_column_name : str
        This is the name of source column in the all_articles_title_source_name_list_of_dict.

    Returns
    -------
    list
        This list contains articles_name and sources name.

    """
    missed_article_name_and_source_name_list = []

    for dict_element in all_articles_title_source_name_list_of_dict:
        if dict_element[article_column_name] in set(missed_articles_list):
            missed_article_name_and_source_name_list.append(
                {"article_name": dict_element[article_column_name], "source_name": dict_element[source_column_name]})

    return missed_article_name_and_source_name_list


def drop_duplicates_citations(citation_dataframe: pd.DataFrame, subset: list = ['title', 'year'], keep: str = 'last',
                              index_reset: bool = True):
    """Return DataFrame with duplicate rows removed. Considering certain columns is optional. Indexes, including time
    indexes are ignored.

    Parameters
    ----------
    index_reset : bool
        It
    citation_dataframe : pandas.DataFrame object
        Input dataset which contains duplicate rows
    subset : list
        column label or sequence of labels, optional Only consider certain columns for identifying duplicates, by
        default use all of the columns.
    keep : str
        options includes {'first', 'last', False}, default 'first'. Determines which duplicates (if any) to keep.
        - ``first`` : Drop duplicates except for the first occurrence.
        - ``last`` : Drop duplicates except for the last occurrence.
        - False : Drop all duplicates.

    Returns
    -------
    pandas.DataFrame object
        DataFrame with duplicates removed

    """

    clean_df = citation_dataframe.drop_duplicates(subset=subset, keep=keep).reset_index(drop=index_reset)
    return clean_df


def add_multiple_sources_column(citation_dataframe: pd.DataFrame, group_by: list = ['title', 'year']):
    """This function check if citations or article title is available at more than one sources and add column named
    'multiple_sources' to the dataframe with list of name of sources names.

    Parameters
    ----------
    citation_dataframe : pandas.DataFrame object
        Input dataset which contains citations or article title with sources more than one.
    group_by : list
        column label or sequence of labels, optional Only consider certain columns for citations or article title with
        sources more than one, by default use all of the columns.

    Returns
    -------
    pandas.DataFrame object
        DataFrame with additional column with list of sources names

    """
    df = citation_dataframe.groupby(group_by)['source'].apply(list).reset_index()
    df = df.rename(columns={"source": "multiple_sources"})
    citation_dataframe_with_multiple_sources_column = citation_dataframe.merge(df, how='left', on=group_by)
    return citation_dataframe_with_multiple_sources_column


def complete_citations_dataframe(citations_files_parent_folder_path):
    """Executes citation step.
    This function load all the citations from path, add required columns for next steps, and remove duplicates.

    Parameters
    ----------
    citations_files_parent_folder_path : str
        this is the path of parent folder of where citations files exists.

    Returns
    -------
    pandas.DataFrame object
        DataFrame with additional columns needed for next steps of systematic review and duplicates are removed

    """
    full_list = converter.load_multiple_ris_citations_files(citations_files_parent_folder_path)
    full_list_df = converter.list_of_dicts_to_dataframe(full_list)
    complete_df = add_multiple_sources_column(full_list_df)
    complete_df = add_citation_text_column(complete_df)
    complete_citations_df = drop_duplicates_citations(complete_df)
    return complete_citations_df

