# We use ChatGPT and link below for instruction 
# https://www.google.com/search?client=firefox-b-1-d&q=how+to+scrape+data+using+reddit+api+in+python#fpstate=ive&vld=cid:615db2be,vid:U9Ogh1OGP-g,st:0


"""
    This is a script of wrapper of Reddit API using PRAW without outputing to CSV File and User CLI
"""

import praw
import pandas as pd

# set creditials of Reddit API
my_client_id="LGtqEAEdrUfv2W3f0cw_rQ"
my_client_secret="fc4HLd_n_5cbNyp3-ZO1yXPEVBI46g"
my_user_agent="teamname"

# initialize PAW

reddit = praw.Reddit(
    client_id=my_client_id,
    client_secret=my_client_secret,
    user_agent=my_user_agent
)

# set url
url_towrap="https://www.reddit.com/r/EngineeringStudents/comments/1f53a5b/finally_left_my_company_is_this_normal/"

submission=reddit.submission(url=url_towrap)

# print title ,content and comments of this reddit post
 
print("Title of the reddit post:",submission.title)
print("Content of the reddit post:",submission.selftext)

print("Comment of the reddit post:")
for comment in submission.comments:
    print(comment.body)


# put all data into a dictionary
data={
    'Title':[submission.title if i==0 else None for i in range(len(submission.comments)) ],
    'Body':[submission.selftext if i==0 else None for i in range(len(submission.comments))],
    'Comments':[comment.body for comment in submission.comments]
}

# put data into a Dataframe
df=pd.DataFrame(data)

# output the dataframe as csv
df.to_csv("reddit.csv",index=False)