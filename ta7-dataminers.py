# import all relevant packages for tsfresh demo

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tsfresh.examples.robot_execution_failures import download_robot_execution_failures,     load_robot_execution_failures
download_robot_execution_failures()
timeseries, y = load_robot_execution_failures()
from tsfresh import extract_features, extract_relevant_features

# NOTE: the dataset of robots and their success at completing a task is built in to tsfresh

if __name__ == "__main__":

    print("\nRajiv Raman and Owais Kamdar\nAIPI 510 Team Assignment 7: Feature Engineering\nTSFresh Code Demo\n")

    # we first generate the entire augmented dataframe with features extracted from time-series data

    all_features = extract_features(timeseries, column_id="id", column_sort="time")

    print("A total of " + str(len(all_features.columns)) + " features were generated.\n")

    # we can use the built-in tsfresh functionality to clean the data and pull out only relevant features

    special_features = extract_relevant_features(timeseries, y, column_id='id', column_sort='time')

    print("Only " + str(len(special_features.columns)) + " features (" + str(np.round(100*float(len(special_features.columns)/len(all_features.columns)),decimals=2)) + " % of total) were determined to be relevant.\n")

    # NOTE: this demo will randomly select 4 elements from the set of relevant features

    # we extract an array that contains the names of all relevant features

    labels = special_features.columns

    # we randomly select 4 of these features for displaying to the user

    myLabels = np.random.choice(labels, size = 4, replace = False)

    # now, we print out our 4 randomly selected labels and guide the user forward

    print("We have randomly selected 4 of these features for further analysis.")

    # iterate through the list of 4 labels to print out their names

    for i in range(len(myLabels)):
        print(str(i+1) + ". " + myLabels[i])

    # NOTE: the demo outputs the data graphed along all 4 C 2 = 6 unique combinations of 2D feature axes   

    print("\nWe will visualize how the robots performed when compared along all 6 unique sets of 2 features.")

    # initialize the empty arrays for storing feature labels when forming our 6 sets of 2

    f1 = []
    f2 = []

    # iterate through the 4 randomly selected labels to build the list of 6 sets of 2 features

    for i in range(len(myLabels)):
        for j in range(i,len(myLabels)):
            if(i != j):
                f1.append(myLabels[i])
                f2.append(myLabels[j])

    # set up a big figure that contains all 6 graphs

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 8))

    # use a counter variable to track your spot in the f1 and f2 arrays while moving through the 2 x 3 grid

    counter = 0;

    # iterate through every set of axes in the grid

    for i in range(2):
        for j in range(3):

            ax = axes[i,j]

            # plot all robots that passed as green points on the axes of our selected features

            ax.scatter(special_features[f1[counter]][y == True], special_features[f2[counter]][y == True], color='lightgreen', label='Pass')

            # plot all robots that failed as red points on the axes of our selected features

            ax.scatter(special_features[f1[counter]][y == False], special_features[f2[counter]][y == False], color='red', label='Fail')

            ax.set_xlabel(f1[counter],fontsize=6)
            ax.set_ylabel(f2[counter],fontsize=6)
            ax.set_title(f'{f2[counter]} vs {f1[counter]}',fontsize=6)
            ax.grid(True)
            ax.legend()

            # update counter to move over to the next unique set of labels in f1 and f2

            counter = counter + 1
    
    plt.subplots_adjust(wspace=1, hspace=1)
    plt.tight_layout()
    plt.show()

