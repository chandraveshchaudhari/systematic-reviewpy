"""Module: os_utils
This module contains functions related to getting directories, files, and filenames from os paths.
"""

import ntpath
import os
from systematic_review import converter


def extract_files_path_from_directories_or_subdirectories(directory_path: str) -> list:
    """Getting all files paths from the directory and its subdirectories.

    Parameters
    ----------
    directory_path : str
        This is the directory path of files we require.

    Returns
    -------
    list
        This list contains path of all the files contained in directory_path.

    """
    list_of_downloaded_articles_path = []
    for path, sub_dirs, files in os.walk(directory_path):
        for name in files:
            list_of_downloaded_articles_path.append(os.path.join(path, name))
    return list_of_downloaded_articles_path


def extract_subdirectories_path_from_directory(directory_path: str) -> list:
    """Getting all sub directories paths from the directory.

    Parameters
    ----------
    directory_path : str
        This is the directory path of sub directories we require.

    Returns
    -------
    list
        This list contains path of all the sub directories contained in directory_path.

    """
    list_of_downloaded_articles_path = []
    for path, sub_dirs, files in os.walk(directory_path):
        for name in sub_dirs:
            list_of_downloaded_articles_path.append(os.path.join(path, name))
    return list_of_downloaded_articles_path


def get_path_leaf(file_path: str) -> str:
    """Extract file name from path.
    for more details visit: https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format

    Parameters
    ----------
    file_path : str
        This is the path of file.

    Returns
    -------
    str
        This is name of file.

    """
    head, tail = ntpath.split(file_path)
    return tail or ntpath.basename(head)


def get_filename_from_path(file_path: str) -> str:
    """Returns the filename from pdf filepath.

    Parameters
    ----------
    file_path : str
        A path is a string of characters used to uniquely identify a location in a directory structure. for more info
        visit- https://en.wikipedia.org/wiki/Path_(computing)

    Returns
    -------
    str
        A filename or file name is a name used to uniquely identify a computer file in a directory structure. for more info
        visit- https://en.wikipedia.org/wiki/Filename

    """
    file_name = get_path_leaf(file_path)
    file_name = file_name.split(".")[0]
    return file_name


def get_file_extension_from_path(file_path: str) -> str:
    """Returns the file extension from pdf filepath.

    Parameters
    ----------
    file_path : str
        A path is a string of characters used to uniquely identify a location in a directory structure. for more info
        visit- https://en.wikipedia.org/wiki/Path_(computing)

    Returns
    -------
    str
        A filename extension, file extension or file type is an identifier specified as a suffix to the name of a
        computer file. for more info visit- https://en.wikipedia.org/wiki/Filename_extension

    """
    file_name = get_path_leaf(file_path)
    file_name = file_name.split(".")[1]
    return file_name


def get_all_filenames_in_dir(dir_path: str) -> list:
    """This provides all the names of files at dir_path.

    Parameters
    ----------
    dir_path : str
        This is the path of folder we are searching files in.

    Returns
    -------
    list
        This is the list of all the names of files at dir_path.

    """
    # Get the list of all files and directories
    dir_files_list = os.listdir(dir_path)
    print("Files and directories in '", dir_path, "' :")
    # prints all files
    print("sources_file_list: ", dir_files_list)
    # prints all source names
    files_name = [f.replace(".ris", "") for f in dir_files_list]
    print("\n", files_name)
    return files_name


def get_sources_name_citations_mapping(dir_path: str) -> list:
    """This makes the list of {'sources_name': 'all source articles citations', ...} from mentioning the dir path of ris
    files.

    Parameters
    ----------
    dir_path : str
        This is the path of folder we are searching ris files in.

    Returns
    -------
    list
        This is the list of all the sources names and it's citations at dir_path.

    """
    sources_name_citations_path_list_of_dict = []
    sources_name = get_all_filenames_in_dir(dir_path)
    index = 0
    for file in sources_name:
        file_path = os.path.join(dir_path, file)
        print(file_path)
        source_citations = converter.ris_to_dict_list(file_path)
        print(file)
        sources_name_citations_path_list_of_dict.append([sources_name[index], source_citations])
        index += 1

    return sources_name_citations_path_list_of_dict


def get_directory_file_name_and_path(dir_path: str) -> tuple:
    """Get file names and file paths from directory path.

    Parameters
    ----------
    dir_path : str
        This is the path of the directory.

    Returns
    -------
    tuple
        This tuple contains list of downloaded_articles_name_list and downloaded_articles_path_list.

    """
    counter = 0
    downloaded_articles_name_list = []
    downloaded_articles_path_list = []
    # directory_path, directory_names, filenames
    for root, directories, files in os.walk(dir_path):
        print(f"number of directories {len(directories)}, number of files{len(files)}")
        print(f"root: {root}, directories: {directories}, files: {files}")
        for file_name in files:
            downloaded_articles_name_list.append(file_name)
            article_path = os.path.join(dir_path, file_name)
            downloaded_articles_path_list.append(article_path)
            counter += 1
    return downloaded_articles_name_list, downloaded_articles_path_list
