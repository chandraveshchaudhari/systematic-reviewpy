#!/usr/bin/env python
# coding: utf-8

# # Quick Tutorial

# ### Installation

# #### Required Dependencies

# In[1]:


get_ipython().system('pip install rispy')
get_ipython().system('pip install pandas')
get_ipython().system('pip install matplotlib')
get_ipython().system('pip install seaborn')


# #### installing the systematic-reviewpy

# In[2]:


get_ipython().system('python3 -m pip install systematic-reviewpy')


# google colab Jupyter notebook Instruction :     
# `Ctrl m m` will convert a code cell to a text cell.       
#  `Ctrl m y` will convert a text cell to a code cell.       

# ##### install pdftotext dependencies: Installing needed python pdf readers for validation and search count of pdf text.

# <font color="#F7B905" size="3">Please run cell based on your OS and keep other cells as markdown.</font>

# In[3]:


##### Debian, Ubuntu, and friends
get_ipython().system('sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev')


# ##### Fedora, Red Hat, and friends
# !sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python3-devel

# ##### macOS
# !brew install pkg-config poppler python

# ##### Windows using conda
# !conda install -c conda-forge poppler

# #### Install python pdf readers

# In[ ]:


## https://pypi.org/project/PyMuPDF/
get_ipython().system('python -m pip install --upgrade pip')
get_ipython().system('python -m pip install --upgrade pymupdf')
## https://pypi.org/project/pdftotext/
get_ipython().system('pip install pdftotext')


# #### importing the systematic-reviewpy

# In[ ]:


import systematic_review


# Most of the object contains methods like to_csv and to_excel to output files

# Check documentation for more string manipulation methods : 
# - preprocess_string (default and applied before all other implemented functions)
# - custom_text_manipulation_function : for putting your custom_text_manipulation_function function to preprocess the text
# - nltk_remove_stopwords
# - pattern_lemma_or_lemmatize_text 
# - nltk_word_net_lemmatizer 
# - nltk_porter_stemmer
# - nltk_lancaster_stemmer 
# - spacy_lemma 
# - nltk_remove_stopwords_spacy_lemma 
# - convert_string_to_lowercase
# - preprocess_string_to_space_separated_words

# <font color="#F7B905" size="3">Please provide name of string manipulation method.</font>

# In[ ]:


string_manipulation_method = 'convert_string_to_lowercase'


# ## Optional Converting and wrangling citation files

# wrangling or modification of the citation files is required if there is format error while uploading files into reference manager.

# In[ ]:


#citation.csv_citations_to_ris_converter("./Data files and Python Code/Downloaded files/springer.csv", "./Data files and Python Code/Modified files/springer.ris")


# In[ ]:


#citation.remove_empty_lines("./Data files and Python Code/Downloaded files/entropy-v12-i12_20210610.ris", "./Data files and Python Code/Modified files/MDPI.ris")


# In[ ]:


#citation.edit_ris_citation_paste_values_after_regex_pattern("./Data files and Python Code/Modified files/MDPI.ris", "./Data files and Python Code/Modified files/mdpi.ris")


# In[ ]:


#import os
#os.remove("./Data files and Python Code/Modified files/MDPI.ris")


# ## Citations

# ### All files are uploaded to mendeley reference manager, updated using mendeley database, and downloaded in ris format.

# <font color="#F7B905" size="3">Please provide the path of the folder that contains all citations ris files.</font>

# In[ ]:


CITATIONS_FILES_PARENT_DIR_PATH = "./Data files and Python Code/Articles_by_sources"


# In[ ]:


citations = systematic_review.citation.Citations(CITATIONS_FILES_PARENT_DIR_PATH)


# In[ ]:


citations_df = citations.get_dataframe()
citations_df


# ### Search Words

# <span style="color:green">Please provide the path of search_words.json or make keyword dictionary.</span>

# In[ ]:


systematic_review.search_count.SearchWords().get_sample_keywords_json()


# <font color="#F7B905" size="3">Edit the template based on your need and provide the file path in cell below. if filename and location is not changed no need to change anything.</font>

# In[ ]:


#KEYWORDS_JSON_FILE_PATH = "./Data files and Python Code/keywords.json"
SEARCH_WORDS_JSON_FILE_PATH = "./sample_search_words_template.json"


# In[ ]:


search_words = systematic_review.search_count.SearchWords(SEARCH_WORDS_JSON_FILE_PATH, string_manipulation_method)


# In[ ]:


print(search_words.value)


# ### Search and count words in citations

# In[ ]:


citations_search_words_count = systematic_review.search_count.SearchCount(citations_df, search_words, string_manipulation_method)


# In[ ]:


citations_search_words_count_df = citations_search_words_count.get_dataframe()
citations_search_words_count_df


# citations_search_words_count.to_csv("./Data files and Python Code/OutputFiles/citations_keywords_count_df.csv")

# ### Sort and Filter the citations

# <font color="#F7B905" size="3">Please provide how many research papers needed.</font>

# In[ ]:


# Filter the citations to required number
required_citations_number = 500


# In[ ]:


filter_sorted_citations = systematic_review.filter_sort.FilterSort(citations_search_words_count_df, search_words, required_citations_number)


# In[ ]:


filter_sorted_citations_df = filter_sorted_citations.get_dataframe()


# In[ ]:


print(len(filter_sorted_citations_df))


# filter_sorted_citations.to_csv("./Data files and Python Code/OutputFiles/filter_sorted_citations_df.csv")

# ## Research paper files

# ### Downloading above selected pdf from databases.

# This is completed with [browser-automationpy](https://github.com/chandraveshchaudhari/browser-automationpy)

# ### Validating the downloaded articles

# <font color="#F7B905" size="3">Please provide parent directory path of all downloaded research papers.</font>

# In[ ]:


DOWNLOADED_ARTICLES_PATH = "./Data files and Python Code/downloadedArticles"


# <font color="#F7B905" size="3">Please provide path of text file containing names of research papers separated by new line OR write None.</font>

# In[ ]:


IN_ACCESSIBLE_ARTICLES_TEXT_FILE_PATH = "./Data files and Python Code/not_accessible_articles.txt"


# In[ ]:


validation = systematic_review.validation.Validation(filter_sorted_citations_df, DOWNLOADED_ARTICLES_PATH, IN_ACCESSIBLE_ARTICLES_TEXT_FILE_PATH)


# In[ ]:


validated_research_papers = validation.get_dataframe()


# In[ ]:


validation.info()


# validation.to_csv("validation.csv")

# ### Search and count the research papers files.

# In[ ]:


research_paper_search_words_count = systematic_review.search_count.SearchCount(validated_research_papers, search_words, string_manipulation_method)


# In[ ]:


research_paper_search_words_count_df = research_paper_search_words_count.get_dataframe()


# research_paper_search_words_count.to_csv("./Data files and Python Code/OutputFiles/pdf_keywords_count_df.csv")

# ### Filter and sort pdf counted df

# <font color="#F7B905" size="3">Please provide how many research papers needed.</font>

# In[ ]:


required_full_text_documents = 100


# In[ ]:


filter_sorted_research_papers = systematic_review.filter_sort.FilterSort(research_paper_search_words_count_df, search_words, required_full_text_documents)


# In[ ]:


selected_review_articles_df = filter_sorted_research_papers.get_dataframe()


# filter_sorted_research_papers.to_csv("./Data files and Python Code/OutputFiles/selected_review_articles_df.csv")

# ## Generating research papers review files: 
# choose any of following

# - sorted based on sources: to make it easier to find articles in folder.

# In[ ]:


sorted_Finaldf = systematic_review.filter_sort.sort_dataframe_based_on_column(selected_review_articles_df, 'source')


# In[ ]:


#sorted_Finaldf.to_csv("./Data files and Python Code/OutputFiles/sorted_Finaldf.csv")


# - Creating the sample literature review file:      
# by adding review columns to enter details manually. The keywords counts are not required at this point of the time, so they are dropped.    

# In[ ]:


selected_citation = systematic_review.citation.drop_search_words_count_columns(sorted_Finaldf, search_words)
selected_citation_review = systematic_review.analysis.creating_sample_review_file(selected_citation)


# selected_citation_review.to_csv("./Data files and Python Code/OutputFiles/selected_citation_review.csv")

# ## Sytematic Review Workflow diagram and info

# In[ ]:


my_analysis = systematic_review.analysis.SystematicReviewInfo(CITATIONS_FILES_PARENT_DIR_PATH, filter_sorted_citations_df,
                 validated_research_papers, selected_review_articles_df)


# In[ ]:


my_analysis.info()


# In[ ]:


my_analysis.systematic_review_diagram()


# ## Analysis

# | Analysis needed                                     | Fact table | Diagram |
# | --------------------------------------------------- | ---------- | ------- |
# | The number of articles                              | yes        | no      |
# | Period of the publications                          | yes        | yes     |
# | Number of authors                                   | yes        | no      |
# | Articles with single authors                        | yes        | no      |
# | Articles per authors                                | yes        | no      |
# | Authors per articles                                | yes        | no      |
# | Top N countries with the highest number of articles | yes        | yes     |
# | Top N journals with the highest number of articles  | yes        | yes     |
# | Top N keywords most used in the articles            | yes        | yes     |
# | The year with the highest number of articles        | yes        | yes     |

# In[ ]:


my_cite_analysis = systematic_review.analysis.CitationAnalysis(sorted_Finaldf)


# In[ ]:


my_cite_analysis.publication_year_info()


# In[ ]:


my_cite_analysis.publication_year_diagram()


# In[ ]:


my_cite_analysis.authors_info()


# In[ ]:


my_cite_analysis.publication_place_info()


# In[ ]:


my_cite_analysis.publication_place_diagram()


# In[ ]:


my_cite_analysis.keywords_info()


# In[ ]:


my_cite_analysis.keyword_diagram(top_result=10)


# In[ ]:


my_cite_analysis.publisher_info()


# In[ ]:


my_cite_analysis.publisher_diagram()

