"""Module: converter
This module contains functions related to files and data type conversion. such as list to txt file, pandas df to list of
dicts and many more.
"""
from collections import defaultdict
from typing import Union, List

import pandas as pd
import rispy

from systematic_review import os_utils


def ris_file_to_pandas_dataframe(ris_file_path: str) -> pd.DataFrame:
    """
    This needs 'rispy' to read ris to list of dicts. It then convert list of dicts to pandas.DataFrame

    Parameters
    ----------
    ris_file_path : str
        This is the path of ris citations file

    Returns
    -------
    pd.DataFrame
        dataframe object from pandas

    """
    with open(ris_file_path, 'r') as bibliography_file:
        entries = rispy.load(bibliography_file)
        df = pd.DataFrame.from_dict(entries)
        return df


def dataframe_to_csv_file(dataframe_object: pd.DataFrame, output_filename: str = "output.csv", index: bool = True):
    """
    This function saves pandas.DataFrame to csv file.

    Parameters
    ----------
    dataframe_object : pandas.DataFrame object
        this is the object of famous python library pandas. for more lemma_info: https://pandas.pydata.org/docs/
    output_filename : str
        This is the name of output file which should contains .csv extension
    index : bool
        Define if index is needed in output csv file or not.

    Returns
    -------

    """
    dataframe_object.to_csv(output_filename, index)


def dataframe_to_list_of_dicts(dataframe: pd.DataFrame) -> list:
    """converts pandas dataframe to the list of dictionaries.

    Parameters
    ----------
    pd.DataFrame
        This is the pandas dataframe consisted of all data from dictionaries converted into respective rows.

    Returns
    -------
    list
        This list contains the dictionaries inside as elements. Example - [{'primary_title' : "this is the title"}]

    """
    list_of_dicts = dataframe.to_dict('records')
    return list_of_dicts


def try_convert_dataframe_column_elements_to_list(dataframe: pd.DataFrame, column_name: str) -> list:
    """try statement for converting each element of dataframe column to list object.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The dataframe with column to convert into list
    column_name : str
        Name of column for conversion

    Returns
    -------
    list
        This is list with each element of type list.

    """
    keyword_list_of_list = []

    for keyword_list in dataframe[column_name]:
        try:
            keyword_list_of_list.append(list(keyword_list))
        except TypeError:
            print(f"'{keyword_list}' can not be converted to list")
    return keyword_list_of_list


def unpack_list_of_lists_with_optional_apply_custom_function(list_of_lists: List[list], custom_function=None) -> list:
    """unpack lists inside of list to new list containing all the elements from list_of_lists with optional
    custom_function applied on all elements. example- [[1,2,3], [3,4,5]] to [1,2,3,3,4,5]

    Parameters
    ----------
    list_of_lists : List[list]
        This list contains lists as elements which might contains other elements.
    custom_function
        This is optional function to be applied on each element of list_of_lists

    Returns
    -------
    list
        list containing all the elements with any optional transformation using custom_function.

    """
    unpacked_list = []
    for element_list in list_of_lists:
        if custom_function:
            temp_list = [custom_function(i) for i in element_list]
            unpacked_list.extend(temp_list)
        else:
            unpacked_list.extend(element_list)
    return unpacked_list


def dict_key_value_to_records(dictionary: dict, key_column_name: str, value_column_name: str):
    """converts {'key':value, key1: value1},etc to record = [{'key_column_name': key, value_column_name: value}, etc].
    that is used to convert to pd.DataFrame

    Parameters
    ----------
    dictionary : dict
        hash map or dictionary that contains key and value pairs.
    key_column_name : str
        name of records column
    value_column_name : str
        name of records column

    Returns
    -------
    list
        This list is in records format.

    """
    keywords_list_of_dicts = []
    for key, value in dictionary.items():
        keywords_list_of_dicts.append({key_column_name: key, value_column_name: value})
    return keywords_list_of_dicts


def list_of_dicts_to_dataframe(list_of_dicts: list) -> pd.DataFrame:
    """converts the list of dictionaries to pandas dataframe.

    Parameters
    ----------
    list_of_dicts : list
        This list contains the dictionaries inside as elements. Example - [{'primary_title' : "this is the title"}]

    Returns
    -------
    pd.DataFrame
        This is the pandas dataframe consisted of all data from dictionaries converted into respective rows.

    """
    dataframe = pd.DataFrame.from_records(list_of_dicts)
    return dataframe


def get_text_from_pdf_pdftotext(pdf_file_path: str, pages: str = "all") -> str:
    """Extract the text from pdf file via pdftotext. for more lemma_info, visit: https://pypi.org/project/pdftotext/

    Parameters
    ----------
    pdf_file_path : str
        This is the path of the pdf file.
    pages : str
        This could be 'all' to get full text of pdf and 'first' for first page of pdf.

    Returns
    -------
    str
        This is the required text from pdf file.

    """
    pdf_object = get_pdf_object_from_pdf_path(pdf_file_path)
    if pages == "first":
        text = pdf_object[0]
    elif pages == "all":
        text = ""
        for pages in pdf_object:
            text += pages
    else:
        text = pdf_object[pages]
    return text


def get_pdf_object_from_pdf_path(pdf_file_path: str) -> object:
    """Extract text as pdf object from the pdf file where loop and indexing can show text per pages.

    Parameters
    ----------
    pdf_file_path : str
        This is the path of pdf file.

    Returns
    -------
    object
        This is pdf object with Extracted text.

    """
    try:
        import pdftotext
    except ImportError:
        print("""This function requires pdftotext library to read pdfs.
        
        step 1. install OS Dependencies:
        These instructions assume you're using Python 3 on a recent OS.
        - Debian, Ubuntu, and friends
        sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev
        - Fedora, Red Hat, and friends
        sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python3-devel
        - macOS
        brew install pkg-config poppler python
        - Windows (Install poppler through conda)
        conda install -c conda-forge poppler
        
        step 2. Install pdftotext
        pip install pdftotext
        
        for more info, please visit https://pypi.org/project/pdftotext/""")
        return ""

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_text_object = pdftotext.PDF(pdf_file)
    return pdf_text_object


def get_text_from_pdf_pymupdf(pdf_file_path: str, pages: str = 'all') -> str:
    """Extract the text from pdf file via fitz(PyMuPDF). for more lemma_info, visit: https://pypi.org/project/PyMuPDF/

    Parameters
    ----------
    pages : str
        This could be 'all' to get full text of pdf and 'first' for first page of pdf.
    pdf_file_path : str
        This is the path of pdf file.

    Returns
    -------
    str
        This is the required text from pdf file.

    """
    try:
        import fitz
    except ImportError:
        print("""This function requires pymupdf library to read pdfs.

        Install pymupdf using: 
        python -m pip install --upgrade pip
        python -m pip install --upgrade pymupdf

        for more info, please visit https://pypi.org/project/PyMuPDF/""")
        return ""

    with fitz.open(pdf_file_path) as doc:
        text = ""
        if pages == "first":
            for page in doc:
                text += page.getText()
                return text
        elif pages == "all":
            for page in doc:
                text += page.getText()
    return text


def get_text_from_pdf(pdf_file_path: str, pages: str = 'all', pdf_reader: str = 'pdftotext') -> Union[str, bool]:
    """This Function get text from pdf files using either pdftotext or pymupdf.

    Parameters
    ----------
    pdf_reader : str
        This is python pdf reader package which convert pdf to text.
    pdf_file_path : str
        This is the path of pdf file.
    pages : str
        This could be 'all' to get full text of pdf and 'first' for first page of pdf.

    Returns
    -------
    str
        This is the required text from pdf file.

    """
    try:
        if pdf_reader == 'pdftotext':
            pdf_text = get_text_from_pdf_pdftotext(pdf_file_path, pages)
            return pdf_text
        elif pdf_reader == 'pymupdf':
            pdf_text = get_text_from_pdf_pymupdf(pdf_file_path, pages)
            return pdf_text
        else:
            print("Not Implemented")
    except Exception:
        return ""


def apply_custom_function_on_dataframe_column(dataframe: pd.DataFrame, column_name: str, custom_function,
                                              new_column_name: str = None) -> pd.DataFrame:
    """This apply custom function to all element of dataframe column.

    Parameters
    ----------
    new_column_name : str
        This is the new name you want to give your modified column and new column will be added to dataframe without
        modifying original column.
    dataframe : pd.DataFrame
        This is the pandas dataframe consisting of column name with elements capable to be transformed with custom
        function.
    column_name : str
        name of dataframe column whose elements are needed to be transformed
    custom_function
        This is custom function to be applied on each elements of the pandas column elements.

    Returns
    -------
    pd.DataFrame
        This is transformed dataframe.

    """
    if new_column_name:
        dataframe[new_column_name] = dataframe[column_name].apply(lambda x: custom_function(x))
    else:
        dataframe[column_name] = dataframe[column_name].apply(lambda x: custom_function(x))
    return dataframe


def get_text_from_multiple_pdf_reader(pdf_file_path: str, pages: str = 'all') -> Union[str, bool]:
    """This Function get text from pdf files using pdftotext. if failed then text comes from pymupdf.

    Parameters
    ----------
    pdf_file_path : str
        This is the path of pdf file.
    pages : str
        This could be 'all' to get full text of pdf and 'first' for first page of pdf.

    Returns
    -------
    str
        This is the required text from pdf file.

    """
    pdf_text = ""
    try:
        pdf_text = get_text_from_pdf_pdftotext(pdf_file_path, pages)
    except Exception:
        pass
    if pdf_text == "":
        try:
            pdf_text = get_text_from_pdf_pymupdf(pdf_file_path, pages)
        except Exception:
            pass
    return pdf_text


def extract_pandas_df_column1_row_values_based_on_column2_value(pandas_dataframe, column2_value,
                                                                column2name="source_name", column1name="article_name"):
    """extract the values of pandas dataframe column1's row_values based on values of column2 value

    Parameters
    ----------
    pandas_dataframe : pd.DataFrame
        This is the pandas dataframe containing at least two columns with values.
    column2_value : object
        This should be str in normal cases but can be any object type supported in pandas for column value.
    column2name : str
        This is the name of the column by which we are extracting the column1 values.
    column1name : str
        This is the name of the column whose values we require.

    Returns
    -------
    list
        This is the list of the resultant values from column1 rows.

    """
    pandas_dataframe = pandas_dataframe.loc[pandas_dataframe[column2name] == column2_value]
    dataframe_dict = pandas_dataframe.to_dict('records')
    article_name_list = []
    for i in dataframe_dict:
        article_name_list.append(i[column1name])
    print(article_name_list)
    return article_name_list


def ris_to_dict_list(ris_file_path):
    """Converts .ris file to list of dictionaries of citations using rispy(https://pypi.org/project/rispy/).
    For more lemma_info on ris format, visit: https://en.wikipedia.org/wiki/RIS_(file_format)

    Parameters
    ----------
    ris_file_path : str
        This is the filepath of the ris file.

    Returns
    -------
    list
        This list contains dictionaries of citations in records format, same as in pandas.

    """
    with open(ris_file_path, 'r') as bibliography_file:
        ris_list_of_dict = rispy.load(bibliography_file)
        source_name = os_utils.get_filename_from_path(ris_file_path)
        for dictionary in ris_list_of_dict:
            dictionary["source"] = source_name

    return ris_list_of_dict


def load_multiple_ris_citations_files(citations_files_parent_folder_path: str) -> list:
    """This function loads all ris citations files from folder

    Parameters
    ----------
    citations_files_parent_folder_path : str
        this is the path of parent folder of where citations files exists.

    Returns
    -------
    list
        this is list of citations dicts inclusive of all citation files.

    """
    citations_path_lists = os_utils.extract_files_path_from_directories_or_subdirectories(
        citations_files_parent_folder_path)
    citations_list = []
    for path in citations_path_lists:
        if path.endswith(".ris"):
            citations_list += ris_to_dict_list(path)
    return citations_list


def load_multiple_ris_citations_files_to_dataframe(citations_files_parent_folder_path: str) -> list:
    """This function loads all ris citations files from folder

    Parameters
    ----------
    citations_files_parent_folder_path : str
        this is the path of parent folder of where citations files exists.

    Returns
    -------
    pd.DataFrame
        this is dataframe of citations dicts inclusive of all citation files.

    """
    full_list = load_multiple_ris_citations_files(citations_files_parent_folder_path)
    full_list_df = list_of_dicts_to_dataframe(full_list)

    return full_list_df


def list_to_text_file(filename: str, list_name: str, permission: str = "w"):
    """This converts list to text file and put each element in new line.

    Parameters
    ----------
    filename : str
        This is the name to be given for text file.
    list_name : list
        This is the python data structure list which contains some data.
    permission : str
        These are the os permissions given for the file. check more lemma_info on python library 'os'.

    Returns
    -------
    None

    """
    with open(filename, permission) as file:
        for i in list_name:
            file.write(str(i))
            file.write("\n")


def load_text_file_to_list(file_path: str, permission: str = "r"):
    """This converts text file to list and put each line in list as single element. get first line of text file by
    list[0].

    Parameters
    ----------
    file_path : str
        This is the name to be given for text file.
    permission : str
        These are the os permissions given for the file. check more lemma_info on python library 'os'.

    Returns
    -------
    list
        This contains all lines loaded into list with one line per list element. [first line, second line,.... ]

    """
    with open(file_path, permission) as file:
        file_object = file.read()

    return file_object.split("\n")


def list_to_string(list_name):
    """This converts list to text_string and put each element in new line.

    Parameters
    ----------
    list_name : list
        This is the python data structure list which contains some data.

    Returns
    -------
    str
        This is the text string comprises of all data of list.

    """
    text_string = ""
    for item in list_name:
        text_string += str(item)
        text_string += "\n"
    return text_string


def unpack_list_of_lists(list_of_lists):
    """unpack list consisting of other list to output list which will include all elements from other lists.

    Parameters
    ----------
    list_of_lists : list
        this is list consisting of elements and lists. example ["first_element", ["second_element"]]

    Returns
    -------
    list
        This is the resultant list consisting of only elements. example ["first_element", "second_element"]

    """
    unpacked_list = []
    for element in list_of_lists:
        if type(element) is list:
            unpacked_list += element
        else:
            unpacked_list.append(element)
    return unpacked_list


def data_type_of_dict_values(dictionary):
    """This provide the data type of dictionary values by outputting dictionary.

    Parameters
    ----------
    dictionary : dict
        This is the dictionary which contains different types of object in values. Example - {"first": [2, 5], "sec": 3}

    Returns
    -------
    dict
        This will output {"<class 'list'>": ["first"], "<class 'int'>": ["sec"]}

    """
    dictionary_info = defaultdict(list)
    for key, value in dictionary.items():
        dictionary_info[str(type(value))].append(key)
    return dictionary_info
