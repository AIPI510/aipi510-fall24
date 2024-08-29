import requests
import pandas as pd


def call_api():
    """
    Calls the Trivia API

    Returns: Results array
    """
    response = requests.get("https://opentdb.com/api.php?amount=10")
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
        


if __name__ == "__main__":
    results = call_api()
    processed_dataframe = make_dataframe(results)
    save_df_to_csv(processed_dataframe, "trivia_questions.csv")