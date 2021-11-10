"""Module: analysis
This module contain code for generating info, diagrams and tables.
"""
import pandas as pd


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


