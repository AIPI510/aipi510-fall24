from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def main():
    # load dataset
    iris = load_iris()

    # select model
    logistic_model = LogisticRegression(max_iter=1000)

    # Without feature engineering
    train_and_eval_model(iris, logistic_model, with_feature_eng=False)

    # With feature engineering
    train_and_eval_model(iris, logistic_model, with_feature_eng=True)


def train_and_eval_model(dataset, model, with_feature_eng = False):
    '''
    This function is the main body, it first load dataset features,
    then decides whether or not to do feature engineering, 
    then print distribution, 
    finally it performs training on the model and evaluate the result
    '''
    result_title = "Following are results without feature engineering"

    X = dataset.data
    y = dataset.target

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=12)
    
    # 2 different situations
    if with_feature_eng:
        X_train = feature_eng_pipeline(X_train)
        X_test = feature_eng_pipeline(X_test)
        result_title = "Following are results with feature engineering"

    # plot the feature distribution
    plot_feature_distribution(X, dataset.feature_names)


    # train and evaluate the model
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    acc_score = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred, average="macro") # multi-variate classification 
    auroc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='macro') # one-vs-rest and multi-variate classification 
    
    cv_acc_scores = cross_val_score(model, X, y, cv=3, scoring='accuracy')
    cv_rec_scores = cross_val_score(model, X, y, cv=3, scoring='recall_macro')
    
    # print out result
    print(result_title)
    print(f"Accuracy score: {acc_score:.2f}")
    print(f"Recall score: {recall:.2f}")
    print(f"Avg CV Accuracy: {np.mean(cv_acc_scores):.2f}")
    print(f"Avg CV Recall: {np.mean(cv_rec_scores):.2f}")
    print(f"AUROC score: {auroc:.2f}", "\n")
    

def plot_feature_distribution(X, feature_names):
    '''Plot the graph of X features'''
    # Plot the first two features of the dataset
    num_features = X.shape[1] # number of columns
    plt.figure(figsize=(15, 10))
    for i in range(num_features):
        plt.subplot(2, 2, i + 1) # total 4 features
        plt.hist(X[:, i], bins=20, color='c', edgecolor='k') # 
        plt.title(f'Distribution of {feature_names[i]}')
        plt.xlabel(feature_names[i])
        plt.ylabel('Frequency')

    plt.show()

def feature_eng_pipeline(X):
    '''Perform feature engineering on X'''
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled


if __name__ == "__main__":
    main()