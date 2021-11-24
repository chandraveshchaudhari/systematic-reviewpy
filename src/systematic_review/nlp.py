"""Module: nlp (Natural language processing)
This module contains functions related to removing stop words, Lemmatization, and stemming  Approaches. Functions will
import the supporting AI model only when they are executed.
For more Examples and info visit: https://www.machinelearningplus.com/nlp/lemmatization-examples-python/ and
https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
"""
from typing import List


def nltk_remove_stopwords(text: str) -> str:
    """Remove unnecessary words such as she, are, of, which, and in.

    Parameters
    ----------
    text : str
        This may contains all words in dictionary.

    Returns
    -------
    str
        This contains words other than stop words described in nltk english stop words.

    """
    try:
        import nltk
    except ImportError:
        print("This function requires nltk library. Please install it using 'pip install nltk' or visit "
              "https://pypi.org/project/nltk/ for more lemma_info.")
        return ""

    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w.lower() in stop_words]
    # normal version of above list comprehension
    # for w in word_tokens:
    #   if w not in stop_words:
    #       filtered_sentence.append(w)
    filtered_text = " ".join(filtered_text)
    return filtered_text


def pattern_lemma_or_lemmatize_text(input_text: str, lemma_info: bool = False) -> str:
    """This return lemma if lemma_info is True else it returns lemmatize text. Uses pattern.en lemma

    Parameters
    ----------
    input_text : str
        This may contains all words in dictionary.
    lemma_info : bool
        This is the switch variable which define return either to lemma information or lemmatize text.

    Returns
    -------
    str
        This output text contains word-forms which are linguistically valid lemmas.
        Example - “car” is matched with words like “cars” and “automobile”.

    """
    try:
        import pattern
    except ImportError:
        print("This function requires pattern library. Please install it using 'pip install Pattern' or visit "
              "https://pypi.org/project/Pattern/ for more lemma_info.")
        return ""
    from pattern.en import lemma, lexeme
    if lemma_info:
        from pattern.en import parse
        return parse(input_text, lemmata=True, tags=False, chunks=False)
    else:
        try:
            output = " ".join([lemma(wd) for wd in input_text.split()])
        except RuntimeError:
            output = " ".join([lemma(wd) for wd in input_text.split()])
    return output


def nltk_word_net_lemmatizer(input_text: str) -> str:
    """This function returns lemmatize text. Uses nltk.stem WordNetLemmatizer

    Parameters
    ----------
    input_text : str
        This may contains all words in dictionary.

    Returns
    -------
    str
        This output text contains word-forms which are linguistically valid lemmas.
        Example - “car” is matched with words like “cars” and “automobile”.

    """
    try:
        import nltk
    except ImportError:
        print("This function requires nltk library. Please install it using 'pip install nltk' or visit "
              "https://pypi.org/project/nltk/ for more lemma_info.")
        return ""
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(input_text)


def nltk_porter_stemmer(input_text: str) -> str:
    """This function returns stemmed text. Uses nltk.stem PorterStemmer

    Parameters
    ----------
    input_text : str
        This may contains all words in dictionary.

    Returns
    -------
    str
        This output text contains stems of a words.
        Example - “car” is matched with words like “cars” but not “automobile”.

    """
    try:
        import nltk
    except ImportError:
        print("This function requires nltk library. Please install it using 'pip install nltk' or visit "
              "https://pypi.org/project/nltk/ for more lemma_info.")
        return ""
    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    return stemmer.stem(input_text)


def nltk_lancaster_stemmer(input_text: str) -> str:
    """This function returns stemmed text. Uses nltk.stem LancasterStemmer

    Parameters
    ----------
    input_text : str
        This may contains all words in dictionary.

    Returns
    -------
    str
        This output text contains stems of a words.
        Example - “car” is matched with words like “cars” but not “automobile”.

    """
    try:
        import nltk
    except ImportError:
        print("This function requires nltk library. Please install it using 'pip install nltk' or visit "
              "https://pypi.org/project/nltk/ for more lemma_info.")
        return ""
    from nltk.stem import LancasterStemmer
    stemmer = LancasterStemmer()
    return stemmer.stem(input_text)


def spacy_lemma(input_text: str) -> str:
    """This function returns lemmatize text. Uses spacy en_core_web_sm

    Parameters
    ----------
    input_text : str
        This may contains all words in dictionary.

    Returns
    -------
    str
        This output text contains word-forms which are linguistically valid lemmas.
        Example - “car” is matched with words like “cars” and “automobile”.

    """
    try:
        import spacy
    except ImportError:
        print("This function requires spacy library. Please install it using 'pip install -U pip setuptools wheel' "
              "'pip install -U spacy' 'python -m spacy download en_core_web_sm' or "
              "visit https://spacy.io/usage for more lemma_info.")
        return ""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(input_text)
    filtered_text = " ".join([token.lemma_ for token in doc])
    return filtered_text


def nltk_remove_stopwords_spacy_lemma(string_list_lower: str) -> List[str]:
    """This function returns lemmatize text of lowercase input string. Uses spacy en_core_web_sm

    Parameters
    ----------
    string_list_lower : str
        This may contains all lowercase words in dictionary.

    Returns
    -------
    List[str]
        This output text contains word-forms which are linguistically valid lemmas.

    """
    string_list_lower_filter_lemma = []
    for string in string_list_lower:
        string_lower_filter = nltk_remove_stopwords(string)
        string_lower_filter_lemma = spacy_lemma(string_lower_filter)
        string_list_lower_filter_lemma.append(str(string_lower_filter_lemma))
    return string_list_lower_filter_lemma
