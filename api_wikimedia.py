# Dependencies needed were the wikipedia API along with the transformers module. We parsed the documentation on the wikimedia page to become
# familiar with requirements.

import wikipediaapi
from transformers import pipeline

# We next needed to establish the generator function using the pipeline function with appropriate parameters;
# the t5-model was employed-this was similiar to the models presented in the python bootcamp.
generator = pipeline("summarization", model="t5-small", tokenizer="t5-small", max_length=512)

# The API required a user agent. I established an account with my personal email.
user_agent = "bbenedicks4234@gmail.com"

# The sample code on the API website instructs the user to establish a language. Wiki was our object to work with
wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)


# Let's create a couple of functions to do things like checking if article exists or summarize the text.
# Then we will create some unit tests for each method.
def fetch_article_text(article_title):
    # Fetches the first 512 characters of a Wikipedia article.
    page = wiki.page(article_title)

    if not page.exists():
        return None

    return page.text[:512]


def summarize_text(text):
    # Generates a summary for the provided text.
    summary = generator(text, max_length=500, min_length=200, do_sample=False)[0]['summary_text']
    return summary


def get_article_summary(article_title):
    # Fetches and summarizes a Wikipedia article by title.
    text_to_summarize = fetch_article_text(article_title)
    if text_to_summarize is None:
        return f"Article '{article_title}' does not exist on Wikipedia."

    summary = summarize_text(text_to_summarize)
    return f"Title: {article_title}\n\nSummary:\n{summary}"


def assignment_1():
    # Outputs the result
    article_title = input("Enter the Wikipedia article you want to read: ")
    result = get_article_summary(article_title)
    print(result)


if __name__ == "__main__":
    # We can individualy call unit tests in this section of our main script.
    assignment_1()
