import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score

# Loading dataset
def load_data():
    df = sns.load_dataset("titanic").dropna(subset=['age', 'fare'])
    return df

# Performing t-test
def perform_t_test(df):
    male_ages = df[df['sex'] == 'male']['age']
    female_ages = df[df['sex'] == 'female']['age']
    
    t_stat, p_value = stats.ttest_ind(male_ages, female_ages)
    return t_stat, p_value

# Ploting Age Distribution by Gender
def plot_age_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="age", hue="sex", kde=True, bins=30, palette="viridis", alpha=0.7)
    plt.title("Age Distribution by Gender", fontsize=16)
    plt.xlabel("Age", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    sns.despine()
    plt.show()

# Performing ANOVA
def perform_anova(df):
    anova_result = stats.f_oneway(df[df['class'] == 'First']['fare'],
                                  df[df['class'] == 'Second']['fare'],
                                  df[df['class'] == 'Third']['fare'])
    return anova_result.statistic, anova_result.pvalue

# Ploting Fare Distribution by Class
def plot_fare_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='class', y='fare', data=df, palette="coolwarm")
    plt.title("Fare Distribution by Class", fontsize=16)
    plt.xlabel("Class", fontsize=12)
    plt.ylabel("Fare", fontsize=12)
    sns.despine()
    plt.show()

# Performing Chi-square Test
def perform_chi_square(df):
    contingency_table = pd.crosstab(df['class'], df['survived'])
    chi2_stat, p_val, _, _ = stats.chi2_contingency(contingency_table)
    return chi2_stat, p_val

# Plotting Survival Count by Class
def plot_survival_by_class(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='class', hue='survived', data=df, palette="magma")
    plt.title("Survival Count by Class", fontsize=16)
    plt.xlabel("Class", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    sns.despine()
    plt.show()

# Performing Logistic Regression and return ROC data
def perform_logistic_regression(df):
    X = df[['age', 'fare']]
    y = df['survived']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Logistic regression
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    
    # Predict probabilities
    y_pred_prob = logreg.predict_proba(X_test)[:, 1]
    
    # Calculate ROC curve and AUC
    fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
    roc_auc = roc_auc_score(y_test, y_pred_prob)
    
    return fpr, tpr, roc_auc

# Plotting ROC Curve
def plot_roc_curve(fpr, tpr, roc_auc):
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=16)
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.legend(loc="lower right")
    sns.despine()
    plt.show()

# Main interactive flow
def main():
    df = load_data()
    
    print("Choose a test to perform: \n1. t-test (Compare Age by Gender) \n2. ANOVA (Compare Fare by Class) \n3. Chi-square Test (Class vs Survival)")
    test_choice = int(input("Enter the test number: "))

    if test_choice == 1:
        t_stat, p_value = perform_t_test(df)
        print(f"t-statistic: {t_stat}, p-value: {p_value}")
        plot_age_distribution(df)
    
    elif test_choice == 2:
        f_stat, p_value = perform_anova(df)
        print(f"F-statistic: {f_stat}, p-value: {p_value}")
        plot_fare_distribution(df)
    
    elif test_choice == 3:
        chi2_stat, p_value = perform_chi_square(df)
        print(f"Chi2 Statistic: {chi2_stat}, p-value: {p_value}")
        plot_survival_by_class(df)
    
    else:
        print("Invalid choice! Please enter a valid test number.")

    # Asking if user wants to run logistic regression
    print("\nWould you like to run a logistic regression to predict survival? (yes/no)")
    logreg_choice = input().strip().lower()

    if logreg_choice == 'yes':
        fpr, tpr, roc_auc = perform_logistic_regression(df)
        print(f"ROC AUC: {roc_auc}")
        plot_roc_curve(fpr, tpr, roc_auc)
    else:
        print("Logistic regression skipped.")

if __name__ == "__main__":
    main()
