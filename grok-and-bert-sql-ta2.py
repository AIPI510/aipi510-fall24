def main():
    
    # Used the following you tube vidieo for help on how to connect to sqllite db - https://www.youtube.com/watch?v=UZIhVmkrAEs
    import sqlite3
    import pandas as pd

    df = pd.read_csv("data/tips.csv")

    print(df)

    connection = sqlite3.connect('ta2-grok-and-bert.db')

    print("hi")
    df.to_sql('tips', connection, if_exists = "replace")
    print("hi")

if __name__ == "__main__":
    main()