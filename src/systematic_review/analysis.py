"""Module: analysis
This module contain code for generating info, diagrams and tables. It can be used to generate systematic review flow
and citations information.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from systematic_review import os_utils, converter, citation, string_manipulation, validation, search_count


def creating_sample_review_file(selected_citation_df):
    """This function outputs dataframe with including columns to make literature review easier.

    Parameters
    ----------
    selected_citation_df : pandas.DataFrame object
        This dataframe is the result of last step of systematic-reviewpy. This contains records for manual literature
        review.

    Returns
    -------
    pandas.DataFrame object
        This is dataframe with additional columns for helping in adding details of literature review.

    """
    # add additional columns
    literature_review_cols = ['Main Topic', 'Sub Topic', 'source', 'Aim of the Study(objectives)', 'data sources',
                              'Data period', 'Input Variables', 'methodology', 'Findings', 'Research Gap/ Limitations',
                              'Results / Conclusions', 'place_published', 'Notes, Special Considerations', 'Email ID']
    selected_citation_review = pd.concat([selected_citation_df, pd.DataFrame(columns=literature_review_cols)])
    return selected_citation_review


def analysis_of_multiple_ris_citations_files(citations_files_parent_folder_path: str) -> dict:
    """This function loads all ris citations files from folder and return the databases names and collected number of
    citations from the databases to dict.

    Parameters
    ----------
    citations_files_parent_folder_path : str
        this is the path of parent folder of where citations files exists.

    Returns
    -------
    dict
        this is dict of databases name and number of records in ris files.

    """
    citations_path_lists = os_utils.extract_files_path_from_directories_or_subdirectories(
        citations_files_parent_folder_path)
    details = {"total": 0}
    for path in citations_path_lists:
        if path.endswith(".ris"):
            length = len(converter.ris_to_dict_list(path))
            details[os_utils.get_filename_from_path(path)] = length
            details["total"] += length
    return details


def vertical_dict_view(dictionary: dict) -> str:
    """convert dict to string with each element in new line.

    Parameters
    ----------
    dictionary : dict
        Contains key and value which we want to print vertically.

    Returns
    -------
    str
        This prints key1 : value1
        and         key2 : value2 ... in vertical format

    """
    output_string = ""
    for key, value in dictionary.items():
        output_string += f"{key} : {value}\n"

    return output_string


def duplicate_count(dataframe: pd.DataFrame) -> int:
    """return count of the duplicate articles.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Input pandas dataframe where we want to check numbers of duplicates.

    Returns
    -------
    int
        number of duplicates records.

    """
    complete_citations_df = citation.drop_duplicates_citations(dataframe)
    count_of_duplicates = len(dataframe) - len(complete_citations_df)

    return count_of_duplicates


def missed_article_count(filter_sorted_citations_df: pd.DataFrame, downloaded_articles_path: str,
                         title_column_name: str = "cleaned_title"):
    """return count of missed articles from downloading by checking original list of articles from
    filter_sorted_citations_df using downloaded articles path.

    Parameters
    ----------
    title_column_name : str
        contains name of column which contain the name of article.
    filter_sorted_citations_df : pd.DataFrame
        This dataframe contains records of selected articles including name of articles.
    downloaded_articles_path : str
        contains parent folder of all the downloaded articles files.

    Returns
    -------
    int
        count of the missed articles from downloading.

    """
    original_list = [i for i in filter_sorted_citations_df[title_column_name]]
    validated_articles_list, invalidated_list, manual_list = validation.validating_pdfs_using_multiple_pdf_reader(
        downloaded_articles_path)
    articles_list = validation.getting_article_paths_from_validation_detail(validated_articles_list)
    downloaded_list = [
        string_manipulation.preprocess_string(os_utils.get_filename_from_path(k))
        for k in articles_list]
    missed_articles = validation.finding_missed_articles_from_downloading(downloaded_list, original_list)
    return len(missed_articles[0])


def text_padding_for_visualise(text: str, front_padding_space_multiple: int = 4,
                               top_bottom_line_padding_multiple: int = 1):
    """This add required space on all four side of text for better look.

    Parameters
    ----------
    text : str
        This is the input word.
    front_padding_space_multiple : int
        This multiply the left and right side of spaces for increased padding.
    top_bottom_line_padding_multiple : int
        This multiply the top and down side of spaces for increased padding.

    Returns
    -------
    tuple
        str - text with spaces on all four sides.
        int - height that is number of lines.
        int - width that is number of char in longest line.

    """
    top_bottom_line_padding = "\n" * top_bottom_line_padding_multiple
    output_text = top_bottom_line_padding
    height = top_bottom_line_padding_multiple * 2
    width = front_padding_space_multiple * 2
    max_width = 0

    for t in text.split("\n"):
        padding = " " * front_padding_space_multiple + t + " " * front_padding_space_multiple
        output_text += padding + "\n"
        max_width = max(len(t), max_width)

    width += max_width
    height += len(text.split("\n"))
    output_text += "\n" * (top_bottom_line_padding_multiple - 1)

    return output_text, height, width


def custom_box(**kwargs) -> dict:
    """This is the option for matplotlib text in box.

    Parameters
    ----------
    kwargs : dict
        Contains key word arguments

    Returns
    -------
    dict
        contains options

    """
    custom_options = {"bbox": {"boxstyle": "square", "facecolor": "white"}, "horizontalalignment": "center",
                      "verticalalignment": "center", "color": "midnightblue"}

    if kwargs:
        for key, value in kwargs.items():
            custom_options[key] = value

    return custom_options


class TextInBox:
    """This is matplotlib text in box class to make it easier to use text boxes.

    """

    def __init__(self, figure_axes, x_coordinate, y_coordinate, text=""):
        """It needs pyplot figure axes to add boxes, and x and y coordinate with any text to put into box.

        Parameters
        ----------
        figure_axes : matplotlib.pyplot.axes
            This is the axes of the figure where we want to add text box.
        x_coordinate : float
            This is the x coordinate usually 0 at left bottom side of figure in this module.
        y_coordinate : float
            This is the y coordinate usually 0 at left bottom side of figure in this module.
        text : str
            This is text to be written inside of box.
        """
        self.figure_axes = figure_axes
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width_of_one_char = 0.067
        self.width_of_one_line = 0.165
        self.text = text_padding_for_visualise(text)[0]
        self.left = (
            self.x_coordinate - ((text_padding_for_visualise(text)[2] / 2) * self.width_of_one_char), self.y_coordinate)
        self.right = (
            self.x_coordinate + ((text_padding_for_visualise(text)[2] / 2) * self.width_of_one_char), self.y_coordinate)
        self.top = (
            self.x_coordinate, self.y_coordinate + ((text_padding_for_visualise(text)[1] / 2) * self.width_of_one_line))
        self.bottom = (
            self.x_coordinate, self.y_coordinate - ((text_padding_for_visualise(text)[1] / 2) * self.width_of_one_line))

    def add_box(self, **kwargs):
        """It put the box on the matplotlib.pyplot.axes figure

        Parameters
        ----------
        kwargs : dict
            This taken any custom options to be set into box.

        Returns
        -------

        """
        self.figure_axes.text(self.x_coordinate, self.y_coordinate, self.text, custom_box(**kwargs))


class Annotate:
    """This class makes it easier to draw arrows into matplotlib.pyplot.axes figure

    """

    def __init__(self, figure_axes, start_coordinate, end_coordinate, arrow_style="<|-"):
        """This takes matplotlib.pyplot.axes and location of x and y coordinate for both start and end point. end point
        is the arrow head target.

        Parameters
        ----------
        figure_axes : matplotlib.pyplot.axes
            This is the axes of the figure where we want to add text box.
        start_coordinate : tuple
            this is tuple containing x and y coordinates of the point, 0, 0 is left bottom in this module figure. start
             point is the arrow handle.
        end_coordinate : tuple
            this is tuple containing x and y coordinates of the point, 0, 0 is left bottom in this module figure. end
            point is the arrow head target.
        arrow_style : str
            This contains symbol for different type of arrows in matplotlib.
        """
        self.figure_axes = figure_axes
        self.start_coordinate = start_coordinate
        self.end_coordinate = end_coordinate
        self.arrowstyle = arrow_style

    def add_arrow(self, text=""):
        """This draw the arrow on matplotlib.pyplot.axes.

        Parameters
        ----------
        text : str
            This takes test to put on the arrow.

        Returns
        -------

        """
        self.figure_axes.annotate(
            text,
            self.start_coordinate,
            self.end_coordinate,
            arrowprops=dict(arrowstyle=self.arrowstyle))


class SystematicReviewInfo:
    """This analyse whole systematic review process and takes all produced file to generate tables, figure.

    """

    def __init__(self, citations_files_parent_folder_path: str = None, filter_sorted_citations_df: pd.DataFrame = None,
                 sorted_final_df: pd.DataFrame = None, downloaded_articles_path: str = None):
        """This class contains all necessary information for systematic review flow.

        Parameters
        ----------
        citations_files_parent_folder_path : str
            this is the path of parent folder of where citations files exists.
        filter_sorted_citations_df : pd.DataFrame
            This is screened dataframe containing records for downloading full text.
        sorted_final_df : pd.DataFrame
            This dataframe contains records for manual literature review.
        downloaded_articles_path : str
            This is the location of all articles full text folder.
        """
        self.citations_files_parent_folder_path = citations_files_parent_folder_path if \
            citations_files_parent_folder_path is not None else ""

        self.sources = analysis_of_multiple_ris_citations_files(citations_files_parent_folder_path) if \
            citations_files_parent_folder_path is not None else ""
        self.duplicates = duplicate_count(
            converter.load_multiple_ris_citations_files_to_dataframe(citations_files_parent_folder_path)) if \
            citations_files_parent_folder_path is not None else ""

        self.screened = int(self.sources["total"]) - int(self.duplicates) if (self.sources is not None) and (
                self.duplicates is not None) else ""
        self.for_retrieval = len(filter_sorted_citations_df) if filter_sorted_citations_df is not None else ""
        self.screened_out = self.screened - self.for_retrieval if (self.screened is not None) and (
                self.for_retrieval is not None) else ""

        self.not_retrieved = missed_article_count(filter_sorted_citations_df, downloaded_articles_path) if \
            (filter_sorted_citations_df is not None) and (downloaded_articles_path is not None) else ""

        self.eligible = len(sorted_final_df) if sorted_final_df is not None else ""
        self.manually_excluded = ""
        self.manually_excluded_reasons = ""

        self.included = ""

    def get_text_list(self):
        """This produces the list of all analysis done in this class.

        Returns
        -------
        list
            This contains systematic review information in sentences.

        """
        text_list = [f"Records identified from:\n{vertical_dict_view(self.sources)}",
                     f"Records screened\n(n = {self.screened})",
                     f"Reports sought for retrieval\n(n = {self.for_retrieval})",
                     f"Reports assessed for eligibility\n(n = {self.eligible})",
                     f"Total studies included in review\n(n = {self.included})",
                     f"Records removed before screening:\nDuplicate records removed\n (n = {self.duplicates})",
                     f"Records screened out\n(n = {self.screened_out})",
                     f"Reports not retrieved\n(n = {self.not_retrieved})",
                     f"Reports excluded:\n{self.manually_excluded}\n{self.manually_excluded_reasons}"]

        return text_list

    def info(self):
        """This takes systematic review text list and create proper order to print.

        Returns
        -------

        """
        temp_text = self.get_text_list()
        order = [0, 5, 1, 6, 2, 7, 3, 8, 4]
        for index in order:
            print(temp_text[index], "\n")

    def systematic_review_diagram(self, fig_width=10, fig_height=10):
        """This outputs the systematic review diagram resembling PRISMA guidelines.

        Parameters
        ----------
        fig_width : float
            This is width of figure in inches.
        fig_height : float
            This is height of figure in inches.

        Returns
        -------

        """
        fig = plt.figure(figsize=(fig_width, fig_height))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(0, fig_width)
        ax.set_ylim(0, fig_height)

        ax.tick_params(bottom=False, top=False,
                       left=False, right=False)
        ax.tick_params(labelbottom=False, labeltop=False,
                       labelleft=False, labelright=False)

        text_list = self.get_text_list()

        # draw rectangles with text in the center
        # box 0 to 8

        all_boxes = [
            TextInBox(ax, validation.amount_by_percentage(fig_width, 30),
                      validation.amount_by_percentage(fig_height, 85), text_list[0]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 30),
                      validation.amount_by_percentage(fig_height, 70), text_list[1]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 30),
                      validation.amount_by_percentage(fig_height, 50), text_list[2]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 30),
                      validation.amount_by_percentage(fig_height, 30), text_list[3]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 30),
                      validation.amount_by_percentage(fig_height, 15), text_list[4]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 70),
                      validation.amount_by_percentage(fig_height, 85), text_list[5]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 70),
                      validation.amount_by_percentage(fig_height, 70), text_list[6]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 70),
                      validation.amount_by_percentage(fig_height, 50), text_list[7]),
            TextInBox(ax, validation.amount_by_percentage(fig_width, 70),
                      validation.amount_by_percentage(fig_height, 30), text_list[8])]

        for box in all_boxes:
            box.add_box()

        # Draw arrows
        all_arrows = [Annotate(ax, all_boxes[0].bottom, all_boxes[1].top),
                      Annotate(ax, all_boxes[1].bottom, all_boxes[2].top),
                      Annotate(ax, all_boxes[2].bottom, all_boxes[3].top),
                      Annotate(ax, all_boxes[3].bottom, all_boxes[4].top),
                      Annotate(ax, all_boxes[0].right, all_boxes[5].left),
                      Annotate(ax, all_boxes[1].right, all_boxes[6].left),
                      Annotate(ax, all_boxes[2].right, all_boxes[7].left),
                      Annotate(ax, all_boxes[3].right, all_boxes[8].left)]

        # vertical arrows

        # Horizontal arrows

        for arrow in all_arrows:
            arrow.add_arrow()

        plt.show()


def dataframe_column_counts(dataframe, column_name):
    """Equivalent to pandas.DataFrame.value_counts(), It return list with count of unique element in column

    Parameters
    ----------
    dataframe : pd.DataFrame
        dataframe which contains column that is to be counted
    column_name : str
        Name of pandas column elements are supposed to be counted.

    Returns
    -------
    object
        unique column elements with counts

    """
    return dataframe[column_name].value_counts()


def seaborn_countplot_with_pandas_dataframe_column(dataframe, column_name, theme_style="darkgrid",
                                                   xaxis_label_rotation=90, top_result=None):
    """generate seaborn count bar chart using dataframe column.

    Parameters
    ----------
    dataframe : pd.DataFrame
        dataframe which contains column whose value counts to be shown.
    column_name : str
        Name of pandas column elements are supposed to be counted.
    theme_style : str
        name of the bar chart theme
    xaxis_label_rotation : float
        rotate the column elements shown on x axis or horizontally.
    top_result : int
        This limits the number of column unique elements to be shown

    Returns
    -------
    object
            show the bar chart

    """
    ax = sns.countplot(x=column_name, data=dataframe, order=dataframe.value_counts(column_name).iloc[:top_result].index)
    sns.set_theme(style=theme_style)
    plt.xticks(rotation=xaxis_label_rotation)
    ax.bar_label(ax.containers[0])
    plt.show()


class CitationAnalysis:
    """This takes any pandas dataframe containing citation details and produces analyses on various columns.

    """

    def __init__(self, dataframe):
        """This requires citation dataframe.

        Parameters
        ----------
        dataframe : pd.DataFrame
            This dataframe is checked for columns for analyses, please change column name for analyses if not same as
            implemented.

        """
        self.dataframe = dataframe

    def publication_year_info(self, column_name: str = "year"):
        """shows how many articles are published each year.

        Parameters
        ----------
        column_name : str
            column name of publication year detail in citation dataframe

        Returns
        -------
        object
            contains year and count of publications

        """
        return dataframe_column_counts(self.dataframe, column_name)

    def publication_year_diagram(self, column_name: str = "year",
                                 top_result=None, method: str = "seaborn", theme_style="darkgrid",
                                 xaxis_label_rotation=90, pandas_bar_kind: str = "bar"):
        """generates chart showing how many articles are published each year.

        Parameters
        ----------
        pandas_bar_kind : str
            pandas plot option of kind of chart needed. defaults to 'bar' in this implementation
        column_name : str
            column name of publication year detail in citation dataframe
        theme_style : str
            name of the bar chart theme
        xaxis_label_rotation : float
            rotate the column elements shown on x axis or horizontally.
        top_result : int
            This limits the number of column unique elements to be shown
        method : str
            provide option to plot chart using either 'seaborn' or 'pandas'

        Returns
        -------

        """
        if method.lower() == "seaborn":
            seaborn_countplot_with_pandas_dataframe_column(self.dataframe, column_name, theme_style=theme_style,
                                                           xaxis_label_rotation=xaxis_label_rotation,
                                                           top_result=top_result)
        elif method.lower() == "pandas":
            self.dataframe[column_name].value_counts()[:top_result].plot(kind=pandas_bar_kind)
            plt.show()
        else:
            print("Please provide method value as 'seaborn' or 'pandas'.")

    def authors_analysis(self, authors_column_name="authors"):
        """generates the details based on pandas dataframe column of article authors. example- Number of authors,
        Articles with single authors, Articles per authors, Authors per articles

        Parameters
        ----------
        authors_column_name : str
            Name of column containing authors details.

        Returns
        -------
        tuple
            contains Number of authors, Articles with single authors, Articles per authors, Authors per articles

        """
        number_of_articles = len(self.dataframe)
        unique_author_names = set()
        articles_with_single_authors = 0

        for authors_list in self.dataframe[authors_column_name]:
            if len(authors_list) == 1:
                articles_with_single_authors += 1
            for authors in authors_list:
                unique_author_names.add(authors)

        number_of_authors = len(unique_author_names)
        articles_per_authors = number_of_articles / number_of_authors
        authors_per_articles = number_of_authors / number_of_articles

        return number_of_authors, articles_with_single_authors, articles_per_authors, authors_per_articles

    def authors_info(self):
        """prints the authors analysis details in nice format

        Returns
        -------

        """
        number_of_authors, articles_with_single_authors, articles_per_authors, authors_per_articles = self.authors_analysis()
        print(f"Number of authors = {number_of_authors}")
        print(f"Articles with single authors = {articles_with_single_authors}")
        print(f"Articles per authors = {articles_per_authors}")
        print(f"Authors per articles = {authors_per_articles}")

    def publication_place_info(self, column_name: str = "place_published"):
        """shows how many articles are published from different places or countries.

        Parameters
        ----------
        column_name : str
            column name of publication place detail in citation dataframe

        Returns
        -------
        object
            contains publication place and count of publications

        """
        return dataframe_column_counts(self.dataframe, column_name)

    def publication_place_diagram(self, column_name: str = "place_published",
                                  top_result=None, method: str = "seaborn", theme_style="darkgrid",
                                  xaxis_label_rotation=90, pandas_bar_kind: str = "bar"):
        """generates chart showing how many articles are published from different places or countries.

        Parameters
        ----------
        pandas_bar_kind : str
            pandas plot option of kind of chart needed. defaults to 'bar' in this implementation
        column_name : str
            column name of publication place detail in citation dataframe
        theme_style : str
            name of the bar chart theme
        xaxis_label_rotation : float
            rotate the column elements shown on x axis or horizontally.
        top_result : int
            This limits the number of column unique elements to be shown
        method : str
            provide option to plot chart using either 'seaborn' or 'pandas'

        Returns
        -------

        """
        if method.lower() == "seaborn":
            seaborn_countplot_with_pandas_dataframe_column(self.dataframe, column_name, theme_style=theme_style,
                                                           xaxis_label_rotation=xaxis_label_rotation,
                                                           top_result=top_result)
        elif method.lower() == "pandas":
            self.dataframe[column_name].value_counts()[:top_result].plot(kind=pandas_bar_kind)
            plt.show()
        else:
            print("Please provide method value as 'seaborn' or 'pandas'.")

    def publisher_info(self, column_name: str = "publisher"):
        """shows how many articles are published by different publishers.

        Parameters
        ----------
        column_name : str
            column name of publisher detail in citation dataframe

        Returns
        -------
        object
            contains publisher name and count of publications

        """
        return dataframe_column_counts(self.dataframe, column_name)

    def publisher_diagram(self, column_name: str = "publisher",
                          top_result=None, method: str = "seaborn", theme_style="darkgrid",
                          xaxis_label_rotation=90, pandas_bar_kind: str = "bar"):
        """generates chart showing how many articles are published by different publishers.

        Parameters
        ----------
        pandas_bar_kind : str
            pandas plot option of kind of chart needed. defaults to 'bar' in this implementation
        column_name : str
            column name of publisher detail in citation dataframe
        theme_style : str
            name of the bar chart theme
        xaxis_label_rotation : float
            rotate the column elements shown on x axis or horizontally.
        top_result : int
            This limits the number of column unique elements to be shown
        method : str
            provide option to plot chart using either 'seaborn' or 'pandas'

        Returns
        -------

        """
        if method.lower() == "seaborn":
            seaborn_countplot_with_pandas_dataframe_column(self.dataframe, column_name, theme_style=theme_style,
                                                           xaxis_label_rotation=xaxis_label_rotation,
                                                           top_result=top_result)
        elif method.lower() == "pandas":
            self.dataframe[column_name].value_counts()[:top_result].plot(kind=pandas_bar_kind)
            plt.show()
        else:
            print("Please provide method value as 'seaborn' or 'pandas'.")

    def extract_keywords(self, column_name: str = "keywords"):
        """return dataframe with keywords column containing single keyword in row that are used in the articles.

        Parameters
        ----------
        column_name : str
            column name of keywords detail in citation dataframe

        Returns
        -------

        """
        keywords_list_of_lists = converter.try_convert_dataframe_column_elements_to_list(
            self.dataframe, column_name)
        keywords_list = converter.unpack_list_of_lists_with_optional_apply_custom_function(keywords_list_of_lists,
                                                                                           string_manipulation.string_to_space_separated_words)

        keywords_pandas_df = pd.DataFrame(data={column_name: keywords_list})

        return keywords_pandas_df

    def keywords_info(self, column_name: str = "keywords"):
        """return keywords and number of times they are used in the articles

        Parameters
        ----------
        column_name : str
            column name of keywords detail in citation dataframe

        Returns
        -------

        """
        return dataframe_column_counts(self.extract_keywords(), column_name)

    def keyword_diagram(self, column_name: str = "keywords",
                        top_result=None, method: str = "seaborn", theme_style="darkgrid",
                        xaxis_label_rotation=90, pandas_bar_kind: str = "bar"):
        """generates chart showing how many articles are published by different publishers.

        Parameters
        ----------
        pandas_bar_kind : str
            pandas plot option of kind of chart needed. defaults to 'bar' in this implementation
        column_name : str
            column name of keywords detail in citation dataframe
        theme_style : str
            name of the bar chart theme
        xaxis_label_rotation : float
            rotate the column elements shown on x axis or horizontally.
        top_result : int
            This limits the number of column unique elements to be shown
        method : str
            provide option to plot chart using either 'seaborn' or 'pandas'

        Returns
        -------

        """
        if method.lower() == "seaborn":
            seaborn_countplot_with_pandas_dataframe_column(self.extract_keywords(), column_name,
                                                           theme_style=theme_style,
                                                           xaxis_label_rotation=xaxis_label_rotation,
                                                           top_result=top_result)
        elif method.lower() == "pandas":
            self.extract_keywords()[column_name].value_counts()[:top_result].plot(kind=pandas_bar_kind)
            plt.show()
        else:
            print("Please provide method value as 'seaborn' or 'pandas'.")
