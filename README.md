
<div align="center">
  <img src="https://raw.githubusercontent.com/chandraveshchaudhari/personal-information/initial_setup/logos/my%20github%20logo%20template-systematic-reviewpy%20small.png" width="640" height="320">
</div>

# An open-source Python framework for systematic review based on PRISMA : systematic-reviewpy
> Chaudhari, C., Purswani, G. (2023). Stock Market Prediction Techniques Using Artificial Intelligence: A Systematic Review. In: Kumar, S., Sharma, H., Balachandran, K., Kim, J.H., Bansal, J.C. (eds) Third Congress on Intelligent Systems. CIS 2022. Lecture Notes in Networks and Systems, vol 608. Springer, Singapore. https://doi.org/10.1007/978-981-19-9225-4_17

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Contribution](#contribution)
- [Future Improvements](#future-improvements)

## Introduction
The main objective of the Python framework is to automate systematic reviews to save reviewers time without creating 
constraints that might affect the review quality. The other objective is to create an open-source and highly 
customisable framework with options to use or improve any parts of the framework. python framework supports each step in
the systematic review workflow and suggests using checklists provided by Preferred Reporting Items for Systematic Reviews
and Meta-Analyses (PRISMA). 

### Authors
<img align="left" width="231.95" height="75" src="https://raw.githubusercontent.com/chandraveshchaudhari/personal-information/initial_setup/images/christ.png">

The packages [systematic-reviewpy](https://github.com/chandraveshchaudhari/systematic-reviewpy) and 
[browser-automationpy](https://github.com/chandraveshchaudhari/browser-automationpy) are part of Research paper 
`An open-source Python framework for systematic review based on PRISMA` created by [Chandravesh chaudhari][chandravesh linkedin], Doctoral candidate at [CHRIST (Deemed to be University), Bangalore, India][christ university website] under supervision of [Dr. Geetanjali purswani][geetanjali linkedin].

<br/>

[chandravesh linkedin]: https://www.linkedin.com/in/chandravesh-chaudhari "chandravesh linkedin profile"
[geetanjali linkedin]: https://www.linkedin.com/in/dr-geetanjali-purswani-546336b8 "geetanjali linkedin profile"
[christ university website]: https://christuniversity.in/ "website"

## Features
- supported file types: ris, json, and [pandas IO](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html)   
- supports the complete workflow for systematic reviews.
- supports to combine multiple databases citations.
- supports searching words with boolean conditions and filter based on counts.
- browser automation using [browser-automationpy](https://github.com/chandraveshchaudhari/browser-automationpy)
- validation of downloaded articles.
- contains natural language processing techniques such as stemming and lemmatisation for text mining. 
- sorting selected research papers based on database.
- generating literature review excel or csv file.
- automatically generates analysis tables and graphs.
- automatically generates workflow diagram.
- generate the ASReview supported file for Active-learning Screening

#### Significance
- Saves time
- Automate monotonous tasks
- Never makes mistakes
- Provides replicable results

## Installation 
This project is available at [PyPI](https://pypi.org/project/systematic-reviewpy/). For help in installation check 
[instructions](https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi)
```bash
python3 -m pip install systematic-reviewpy  
```

### Dependencies
##### Required
- [rispy](https://pypi.org/project/rispy/) - A Python 3.6+ reader/writer of RIS reference files.
- [pandas](https://pypi.org/project/pandas/) - A Python package that provides fast, flexible, and expressive data 
structures designed to make working with "relational" or "labeled" data both easy and intuitive.
##### Optional
- [browser-automationpy](https://github.com/chandraveshchaudhari/browser-automationpy/)
- [pdftotext](https://pypi.org/project/pdftotext/) - Simple PDF text extraction
- [PyMuPDF](https://pypi.org/project/PyMuPDF/) - PyMuPDF (current version 1.19.2) - A Python binding with support for 
MuPDF, a lightweight PDF, XPS, and E-book viewer, renderer, and toolkit.

## Important links
- [Documentation](https://chandraveshchaudhari.github.io/systematic-reviewpy/)
- [Quick tour](https://chandraveshchaudhari.github.io/systematic-reviewpy/systematic-reviewpy%20tutorial.html)
- [Project maintainer (feel free to contact)](mailto:chandraveshchaudhari@gmail.com?subject=[GitHub]%20Source%20sytematic-reviewpy) 
- [Future Improvements](https://github.com/chandraveshchaudhari/systematic-reviewpy/projects)
- [License](https://github.com/chandraveshchaudhari/systematic-reviewpy/blob/master/LICENSE.txt)

## Contribution
all kinds of contributions are appreciated.
- [Improving readability of documentation](https://chandraveshchaudhari.github.io/systematic-reviewpy/)
- [Feature Request](https://github.com/chandraveshchaudhari/systematic-reviewpy/issues/new/choose)
- [Reporting bugs](https://github.com/chandraveshchaudhari/systematic-reviewpy/issues/new/choose)
- [Contribute code](https://github.com/chandraveshchaudhari/systematic-reviewpy/compare)
- [Asking questions in discussions](https://github.com/chandraveshchaudhari/systematic-reviewpy/discussions)

## Future Improvements
Graphical User Interface
- [ ] Linux
- [ ] Mac Os
- [ ] Windows
- [ ] Android
- [ ] Ios App
