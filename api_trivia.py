# Resources used:
# Requests API : https://realpython.com/python-requests/
# Pandas API : https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html 
#    (Along with related web-pages in pandas documentation for other references)
# JSON API : https://www.geeksforgeeks.org/how-to-remove-key-value-pair-from-a-json-file-in-python/

import requests
import pandas as pd
import argparse
import sys
import json

CATEGORY_MAP = {
    9: "General Knowledge",
    10: "Entertainment: Books",
    11: "Entertainment: Film",
    12: "Entertainment: Music",
    13: "Entertainment: Musicals & Theatres",
    14:	"Entertainment: Television",
    15: "Entertainment: Video Games",
    16: "Entertainment: Board Games",
    17: "Science & Nature",
    18: "Science: Computers",
    19: "Science: Mathematics",
    20: "Mythology",
    21:	"Sports",
    22: "Geography",
    23: "History",
    24: "Politics",
    25: "Art",
    26: "Celebrities",
    27: "Animals",
    28: "Vehicles",
    29: "Entertainment: Comics",
    30: "Science: Gadgets",
    31: "Entertainment: Japanese Anime & Manga",
    32: "Entertainment: Cartoon & Animations"
}

def call_api(arguments):
    """
    Calls the Trivia API

    Returns: Results array
    """
    URL = "https://opentdb.com/api.php?"
    if arguments.category is not None:
        URL += f"&category={arguments.category}"
    URL += f"&amount={arguments.n}"
    response = requests.get(URL)
    response_json = response.json()
    
    if response_json.get('response_code') == 0:
        results = response.json().get('results')
        return results
    else:
        raise ConnectionError("Can't establish a connection to the Open Trivia API!")
    

def make_dataframe(questions):
    """
    Make a data-frame object out of the questions array

    Returns: A data-frame object with headers corresponding to the data returned
    """
    for idx, question in enumerate(questions):
        incorrect_answers = question.get('incorrect_answers')
        for idx, incorrect_answer in enumerate(incorrect_answers):
            question[f"incorrect_answer_{idx + 1}"] = incorrect_answer
        question.pop("incorrect_answers")
    return pd.DataFrame(questions)


def save_df_to_csv(dataframe, filename):
    """
    Saves the dataframe to csv format
    """
    dataframe.to_csv(filename, index = False)

def parse_args(args):
    parser = argparse.ArgumentParser(description = 'Get questions from the Open Trivia API')
    parser.add_argument('--category', type = int, choices = list(range(9, 33)),
                help = json.dumps(CATEGORY_MAP), default = None)
    parser.add_argument('-n', type = int,
                help = "Number of questions to fetch", default = 10)
    arguments = parser.parse_args(args)
    return arguments


if __name__ == "__main__":
    arguments = parse_args(sys.argv[1:])
    results = call_api(arguments)
    processed_dataframe = make_dataframe(results)
    save_df_to_csv(processed_dataframe, "trivia_questions.csv")