from tabulate import tabulate
from termcolor import colored

def show_data(df, title="Data Summary"):
    """Helper function to display a formatted pandas DataFrame."""
    print(colored(f"\n{title}", 'cyan', attrs=['bold']))
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def simpsons_paradox_demo():
    print(colored("Welcome to the Simpson's Paradox Demo!", 'green', attrs=['bold']))

    # Step 1: Ask the user if they think the drug is effective before seeing any data
    print(colored("\nWe are studying a new drug for a disease and want to determine its effectiveness.", 'yellow'))
    user_opinion = input(colored("Do you believe the drug is effective? (yes/no): ", 'magenta')).strip().lower()

    if user_opinion == "yes":
        print(colored("\nYou seem confident about the drug's effectiveness. Let's see if the data confirms that!", 'yellow'))
    elif user_opinion == "no":
        print(colored("\nYou're skeptical about the drug. Let's take a look at the data to check.", 'yellow'))
    else:
        print(colored("\nI'll assume you are unsure. Let's analyze the data together.", 'yellow'))

    # Step 2: Display the aggregated data
    aggregated_data = {
        'Treatment': ['Treated', 'Control'],
        'Recovered': [20, 16],
        'Did Not Recover': [20, 24],
        'Total': [40, 40],
        'Recovery Rate (%)': [50, 40]
    }
    show_data(aggregated_data, "Aggregated Data")

    # Step 3: Ask the user to analyze the aggregated data
    print(colored("\nBased on the aggregated data above:", 'yellow'))
    aggregated_opinion = input(colored("Do you think the drug is effective now? (yes/no): ", 'magenta')).strip().lower()

    if aggregated_opinion == "yes":
        print(colored("\nThe aggregated data suggests that the drug is 10% more effective than the control.", 'yellow'))
        print(colored("But let's dig deeper and see if this holds true for all groups.", 'yellow'))
    elif aggregated_opinion == "no":
        print(colored("\nYou still don't believe in the drug's effectiveness despite the aggregated data.", 'yellow'))
        print(colored("Let's take a closer look at different subgroups to see if your skepticism is justified.", 'yellow'))
    else:
        print(colored("\nIt seems like you're still unsure. Let's analyze the data by subgroup.", 'yellow'))

    # Step 4: Display disaggregated data for males and females
    disaggregated_data_males = {
        'Group': ['Treated', 'Control'],
        'Recovered': [18, 7],
        'Did Not Recover': [12, 3],
        'Total': [30, 10],
        'Recovery Rate (%)': [60, 70]
    }
    disaggregated_data_females = {
        'Group': ['Treated', 'Control'],
        'Recovered': [2, 9],
        'Did Not Recover': [8, 21],
        'Total': [10, 30],
        'Recovery Rate (%)': [20, 30]
    }

    print(colored("\nNow, let's look at the data broken down by gender (disaggregated data):", 'yellow'))
    show_data(disaggregated_data_males, "Disaggregated Data (Males)")
    show_data(disaggregated_data_females, "Disaggregated Data (Females)")

    # Step 5: Explain Simpson's Paradox and resolve the paradox
    print(colored("\nSurprising, right?", 'cyan'))
    
    if aggregated_opinion == "yes":
        print(colored("Despite initially thinking the drug was effective based on the aggregated data,", 'yellow'))
        print(colored("the disaggregated data shows that the recovery rate is actually lower for both males and females.", 'yellow'))
    elif aggregated_opinion == "no":
        print(colored("It looks like your skepticism was justified!", 'yellow'))
        print(colored("The disaggregated data shows that the recovery rate is lower for both males and females, even though the aggregated data suggested otherwise.", 'yellow'))

    print(colored("\nThis is an example of Simpson's Paradox.", 'cyan'))
    print(colored("In this case, gender is a confounding factor, which masks the true relationship between the drug and recovery.", 'yellow'))
    
    # Step 6: Final reflection
    resolved_opinion = input(colored("Now that you see the disaggregated data, do you think the drug is effective? (yes/no): ", 'magenta')).strip().lower()

    if resolved_opinion == "yes":
        print(colored("\nInteresting! Despite the subgroup analysis, you still believe the drug is effective.", 'yellow'))
        print(colored("Remember, it's important to look at the true causal relationships behind the data.", 'yellow'))
    elif resolved_opinion == "no":
        print(colored("\nIt seems you've changed your mind after seeing the disaggregated data.", 'yellow'))
        print(colored("This is the power of analyzing confounders like gender. The drug is not effective for either group.", 'yellow'))
    else:
        print(colored("\nIt seems you're still unsure, but that's okay!", 'yellow'))
        print(colored("Simpson's Paradox can be tricky, and it shows why deeper analysis is so important.", 'yellow'))

    print(colored("\nThank you for participating in this Simpson's Paradox demo!", 'green', attrs=['bold']))

if __name__ == "__main__":
    simpsons_paradox_demo()
