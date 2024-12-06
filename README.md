# AIPI 510: Data Sourcing & Analytics (Fall 2024)
# Team Assignment #5
## Statistical Analysis

This is the accompanying GitHub to the Fall 2024 section of AIPI 510, taught by Dr. Brinnae Bent. Teaching assistance from XX and XX. 
## Instructions
1. Put together a code demo for your assigned topic. 
### Code should be:
* Clean and well organized script
* Using best practices (if you aren’t sure, go back to the Premodule content)
* Well-commented
* Contains appropriate unit testing
* Clear name (ie ‘wilcoxon-test.py’)

## Course Description
Course introduces students to the technical and non-technical aspects of collecting, cleaning and preparing data for use in machine learning applications. Technical aspects covered will include the types of data, methods of sourcing data via the web, APIs and from domain-specific sensors and hardware, an increasingly common source of analytics data in technical industries. The course also introduces methods and tools for evaluating the quality of data, performing basic exploratory data analysis, and pre-processing data for use in analytics. Non-technical aspects covered include an introduction to data privacy, GDPR, regulatory issues, bias and industry-specific concerns regarding data usage.
2. In addition to your code demo, you should put together a creative demonstration of your topic. Options include: song, rap, poem, children’s book, painting, short movie, interactive webpage, app demonstrating concept. You are welcome to do something beyond this list, just clear it with me first. You can use GenAI to create images for your creative component. If you use GenAI for your text component, you will need to go the extra mile and do a performance with it (ie a slam poem or sing the song and play guitar). Make sure to cite the GenAI used, per the syllabus.

## Installation
## Submission
To submit your code, make a PR into the statistical-analysis-ta5 branch and add me and the TA as reviewers. In your PR, add any links to your creative component. Also, add any requirements (and versions) that are not currently in the requirements.txt file to the text of your PR.

1. Clone the repository:
   ```
   git clone https://github.com/AIPI510/aipi510-fall24.git
   cd aipi510-fall24
   ```
You will be presenting your creative component in class live either Week 6 or Week 7. If the creative component is a short movie, it is acceptable to show the video. 

2. Recommended: Use a virtual environment, using venv or conda
## Topics
### Descriptive Statistics
* Measures of central tendency (mean, median, mode)
* Measures of dispersion (standard deviation, variance, range, interquartile range)
* Measures of distributions (skew, kurtosis)
### Hypothesis Testing
* Type I and Type II errors
* P-values and significance levels
* Multiple hypothesis correction (Bonferroni)
### Parametric Tests
* Z-score and standard normal distribution
* One-sample t-test
* Independent samples t-test
* Paired samples t-test
### Nonparametric Tests
* Mann-Whitney U test (unpaired t-test)
* Wilcoxon signed rank test (paired t-test)
* Chi-square test for independence
### ANOVA
* One-way ANOVA
* Post-hoc tests (Tukey)
### Regression Analysis
* Simple linear regression
* Ordinary Least Squares (OLS) method and assumptions
* Interpretation of regression coefficients
* Multiple linear regression
### Bayes’ Theorem
### Model Evaluation
* Goodness of fit measures (R-squared, AIC, BIC)
* Residual analysis
* Confidence Intervals
* Simpson’s Paradox

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
## Rubric
### Code (15 points)
* Code is a script, not a notebook
* Code is clean and well organized
* Code is documented with docstrings and comments 
* Code is free of commented out code (ie debug print statements)
* Script has a clear name
* Branching and PRs were done appropriately
* Requirements are included in the text of the PR and are correct and versioned
* The code runs as documented

## How to use this GitHub:
### Creative Component (30 points)
* Creative Component is presented in class on the correct date (either Week 6 or 7, depending on topic)
* Creative Component demonstrates topic in a clear way
* Creative Component is creative

For each assignment:

1. Create a feature branch in the class GitHub repository for your team. We recommend branching off of the assignment branch for each assignment. Feature branch naming convention: ta#-teamname. If individual team members create their own feature branches, ensure these branches are PR'd into your team feature branch, merged, and deleted prior to submission. 

2. Each assignment has its own branch. To submit your code, make a PR into the branch specified in the rubric and add me and the TAs as reviewers. In your PR, add any requirements (and versions) that are not currently in the requirements.txt file to the text of your PR.

## Assignment Branches
* [hello-world-ta0]()
* [data-sourcing-ta1]()
* [sql-ta2]()
* [data-eda-ta4]()
* [statistical-analysis-ta5]()
* [feature-engineering-ta7]()
* [etl-ta8](
