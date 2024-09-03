import praw
import pandas as pd
import argparse

# We use ChatGPT and link below for instruction 
# https://www.google.com/search?client=firefox-b-1-d&q=how+to+scrape+data+using+reddit+api+in+python#fpstate=ive&vld=cid:615db2be,vid:U9Ogh1OGP-g,st:0


# set credentials of Reddit API
my_client_id = "LGtqEAEdrUfv2W3f0cw_rQ"
my_client_secret = "fc4HLd_n_5cbNyp3-ZO1yXPEVBI46g"
my_user_agent = "teamname"

# Initialize PRAW
reddit = praw.Reddit(
    client_id=my_client_id,
    client_secret=my_client_secret,
    user_agent=my_user_agent
)

# Function to scrape Reddit post
def scrape_reddit_post(url):

    """
    Scrape a Reddit post given its URL and output the title, content, and comments of the post.
    """
    
    # Get the Reddit post submission
    submission = reddit.submission(url=url)

    # Print title, content, and comments of the Reddit post
    print("Title of the Reddit post:", submission.title)
    print("Content of the Reddit post:", submission.selftext)
    
    print("\nComments of the Reddit post:")
    for comment in submission.comments:
        print(comment.body)

    # Put all data into a dictionary
    data = {
        'Title': [submission.title if i == 0 else None for i in range(len(submission.comments))],
        'Body': [submission.selftext if i == 0 else None for i in range(len(submission.comments))],
        'Comments': [comment.body for comment in submission.comments]
    }

    # Put data into a DataFrame
    df = pd.DataFrame(data)

    # Output the DataFrame as CSV
    df.to_csv("reddit.csv", index=False)
    print("\nData saved to 'reddit.csv'.")

# Set up argument parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reddit post scraper using PRAW.')
    parser.add_argument('url', type=str, help='URL of the Reddit post to scrape')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function with the given URL
    scrape_reddit_post(args.url)