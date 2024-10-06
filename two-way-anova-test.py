import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

#########     SCRIPT    #########
# Use the updated dataset from the previous results
updated_df = pd.DataFrame({
    'Substances': ['Garlic Powder']*11 + ['Silver']*11 + ['None']*14,
    'Religious_Iconography': ['Crosses']*6 + ['No Crosses']*5 + ['Crosses']*6 + ['No Crosses']*5 + ['Crosses']*6 + ['No Crosses']*8,
    'Noise_Level': [50.00, 52.48, 49.31, 53.24, 57.62, 48.83, 65.00, 63.83, 72.90, 68.84, 62.65,
                    55.00, 52.68, 52.67, 56.21, 45.43, 46.38, 70.00, 67.19, 64.94, 71.57, 65.46,
                    60.00, 67.33, 58.87, 60.34, 52.88, 57.28, 75.00, 75.55, 69.25, 76.88, 72.00, 73.54, 67.71, 68.49]
})

# Set random seed for reproducibility
np.random.seed(42)

# Function to generate new noise levels
def generate_noise_levels(mean, std_dev, size):
    return np.round(np.random.normal(loc=mean, scale=std_dev, size=size), 2)

# Generate additional data for each combination
substances = ['Garlic Powder', 'Silver', 'None']
iconography_list = ['Crosses', 'No Crosses']
new_data = []
for substance in substances:
    for iconography in iconography_list:
        subset = updated_df[(updated_df['Substances'] == substance) & (updated_df['Religious_Iconography'] == iconography)]
        mean_noise = subset['Noise_Level'].mean()
        new_noise = generate_noise_levels(mean_noise, 5, 200)  # Generate 200 new values for each combination
        new_data.extend([(substance, iconography, noise) for noise in new_noise])

# Create a new dataframe with the additional data
additional_df = pd.DataFrame(new_data, columns=['Substances', 'Religious_Iconography', 'Noise_Level'])

# Combine the original and new data
final_df = pd.concat([updated_df, additional_df], ignore_index=True)

# Display summary statistics of the final dataset
print(final_df.groupby(['Substances', 'Religious_Iconography'])['Noise_Level'].describe())

# Display the total number of samples
print(f"\nTotal number of samples: {len(final_df)}")

# Display the grand mean
grand_mean = final_df['Noise_Level'].mean()
print(f"\nGrand mean: {grand_mean}\n")

# Perform 2-way ANOVA
model = ols('Noise_Level ~ C(Substances) + C(Religious_Iconography) + C(Substances):C(Religious_Iconography)', data=final_df).fit()
anova_table = anova_lm(model, typ=2)

# Print ANOVA results
print("ANOVA Results:")
print(anova_table)
print("\n")

# Create interaction plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Substances', y='Noise_Level', hue='Religious_Iconography', data=final_df)
plt.title('Interaction Plot: Substances and Religious Iconography')
plt.ylabel('Noise Level (dB)')
plt.show()

# Print interpretations
print("Interpretations:")
print("1. Main effect of Substances:", "Significant" if anova_table.loc['C(Substances)', 'PR(>F)'] < 0.05 else "Not significant")
print("2. Main effect of Religious Iconography:", "Significant" if anova_table.loc['C(Religious_Iconography)', 'PR(>F)'] < 0.05 else "Not significant")
print("3. Interaction effect:", "Significant" if anova_table.loc['C(Substances):C(Religious_Iconography)', 'PR(>F)'] < 0.05 else "Not significant")

# Calculate the F Statistic

# Calculate SS for Substances
ss_substances = sum([(group['Noise_Level'].mean() - grand_mean)**2 * len(group) 
                     for name, group in final_df.groupby('Substances')])

# Calculate SS for Religious Iconography
ss_iconography = sum([(group['Noise_Level'].mean() - grand_mean)**2 * len(group) 
                      for name, group in final_df.groupby('Religious_Iconography')])

# Calculate SS for Interaction
ss_interaction = sum([(group['Noise_Level'].mean() - grand_mean)**2 * len(group) 
                      for name, group in final_df.groupby(['Substances', 'Religious_Iconography'])])
ss_interaction -= (ss_substances + ss_iconography)

# Calculate SS Total and SS Error
ss_total = sum((final_df['Noise_Level'] - grand_mean)**2)
ss_error = ss_total - (ss_substances + ss_iconography + ss_interaction)

# Calculate degrees of freedom
df_substances = 2  # 3 levels - 1
df_iconography = 1  # 2 levels - 1
df_interaction = 2  # (3-1) * (2-1)
df_error = len(final_df) - (3 * 2)  # total samples - (levels of A * levels of B)

# Calculate Mean Squares
ms_substances = ss_substances / df_substances
ms_iconography = ss_iconography / df_iconography
ms_interaction = ss_interaction / df_interaction
ms_error = ss_error / df_error

# Calculate F-statistics
f_substances = ms_substances / ms_error
f_iconography = ms_iconography / ms_error
f_interaction = ms_interaction / ms_error

print(f"F-statistic for Substances: {f_substances}")
print(f"F-statistic for Religious Iconography: {f_iconography}")
print(f"F-statistic for Interaction: {f_interaction}")


# Save the final dataset to a CSV file
final_df.to_csv('apocalypse_bunker_data.csv', index=False)
print("\nDataset saved as 'apocalypse_bunker_data.csv'")


######### STREAMLIT APP #########
import plotly.express as px
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

ctx = get_script_run_ctx()

def prevpage(): st.session_state.page -= 1

def nextpage(): st.session_state.page += 1

def escape(): st.session_state.page = 0

def homepage():
    st.write('''
            # The Two-Way ANOVA Test
            ## Welcome to the Post-Apocalyptic ANOVA Bunker Simulator!
            **Greetings, brave survivor!** Don't worry, you're not actually trapped in a bunker surrounded by strange monsters. 
            This is just a fun and slightly unsettling way to explore the fascinating world of Two-Way ANOVA testing.

            Disclaimer: No actual apocalypses were triggered in the making of this application. The monsters outside are purely fictional and are not planning to eat your brain... probably.
            
            Here's what you need to know:

            * You're safe behind your computer screen.
            * The other bunkers can't actually hear your screams.
            * The strange noises you hear are just your neighbor's cat... we hope.

            So sit back, relax, and prepare to dive into the thrilling world of statistical analysis – post-apocalyptic style! 
            Remember, in this simulation, the only thing truly terrifying is a p-value greater than 0.05.
            Now, let's explore how different factors affect survival rates in our imaginary bunker network. Who knows? 
            The skills you learn here might come in handy during the real apocalypse. (Just kidding... or are we?)
            ''')

    left, middle, right = st.columns(3)

    right.button('Start Simulation', type='primary', on_click=nextpage)

    st.divider()

    st.write('''
             *The above text and images in the simulation were generated by Perplexity AI and Google Gemini respectively. The final two images were found from Google Images.*
             ''')

def staged_scene(scene, action_text=None, on_click=None):
    st.button('Esc', type='secondary', on_click=escape)

    scene()

    left, _, right = st.columns(3)
    if st.session_state.page > 1:
        left.button('Back', type='secondary', on_click=prevpage)
    right.button('Next' if action_text == None else action_text, type='primary', on_click=nextpage if on_click == None else on_click)

    st.progress(st.session_state.page / 15)

def scene1():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             You find yourself in a bunker. The world as you know it has come to an end.
             ''')
    
def scene2():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             You made it to safety as soon as you heard the reports on the news. You were one of the lucky ones.
             ''')
    
def scene3():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             A frightening sound emanates from the heavy steel bunker door and reverberates.
             ''')
    
def scene4():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             You hear a crackle over Discord.
             ''')
    
def scene5():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             "-one ther-" *nothing* "-ello?! Is anyone there?!"

             The audio comes into focus and you hear a man sobbing on the other end.
             ''')
    
def scene6():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             The sobbing man: "Oh thank God!"

             Another voice, also sobbing: "Hello?"

             Several other voices tune in, one by one.

             One of them: "What are we going to do?! We can't stay here forever! I'm getting out of here!"
             ''')
    
def scene7():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             You hear a bunker door creak open, followed by a blood-curdling scream.
             ''')
    
def scene8():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             You explain to the Discord channel that before you rushed to the bunker, you heard on the news that
             officials speculated that the monsters outside might be zombies, werewolves, or vampires.

             You hear a deafening silence from the channel, as their new reality sinks in.
             ''')

def scene9():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)

             "Maybe there's some material or substance in our bunkers that wards off the monsters outside!
             If we can figure out what it is, then whoever has it can leave the bunker and come rescue the others!
             We can rebuild!"

             The channel is silent for a while.

             Someone: "How do we figure out what works?"

             You: "We'll do a **TWO-WAY ANOVA TEST**."

             Another voice: "A two way a-what-a what?"
             ''')
    
def scene10():
    st.write('''
             **The Two-Way ANOVA Test!** ANOVA stands for Analysis of Variance.

             Using the Two-Way ANOVA Test, we can test two different **factors** and their **levels** to see whether they have an effect
             on a continuous outcome variable, and whether they interact with each other. 
             The **factors** are independent categorical variables, where the *levels* are the types within each category.
             The outcome variable is our dependent variable.

             In our case, we can measure the noise coming from outside, and we can report back over this channel with data over the next three hours. 
             And we can report it with

             1. what noteworthy substance is in your bunker. For example, I have some silver here. That should work against werewolves.
             2. whether your bunker has any religious iconography. Vampires hate that.

             Those are our two factors.

             We just need a few things to be true to perform our test.

             1. We need at least 3 groups to record data independently. We should be good there, because we have several bunkers reporting data.
             2. We need our audio data to be normal distributions.
             3. We need the variance of our audio data to be homegenous. We can check this using Levene's Test.
             
             Is everyone ready?

             **You're met with an enthusiastic cheer.**
             ''')
    
def scene11():
    st.code('''
final_df.head()
            ''', language="python")
    st.dataframe(final_df.head())
    st.write('''
             You: "We now have all the data we need. I'll start on the analysis, folks! Please sit back and relax."
             ''')
    
def scene12():
    st.write('''#### Testing normality''')
    st.write('''We need to check that the distribution is normal from each group (i.e. each bunker). We'll validate this visually as well as using the Anderson-Darling Test.''')
    tabs = st.tabs([f'({substance}, {iconography})' for substance in substances for iconography in iconography_list])
    i = 0
    for substance in substances:
        for iconography in iconography_list: 
            with tabs[i]:
                group_df = final_df[(final_df['Substances'] == substance) & (final_df['Religious_Iconography'] == iconography)]
                fig = px.histogram(group_df, x='Noise_Level')
                st.plotly_chart(fig, theme='streamlit')
                st.code(f'''
from scipy import stats

group_df = final_df[(final_df['Substances'] == '{substance}') & (final_df['Religious_Iconography'] == '{iconography}')]
stats.anderson(group_df['Noise_Level'])
                ''', language='python')
                result = stats.anderson(group_df['Noise_Level'])
                st.write(f'''{result}''')
                i += 1
    
def scene13():
    st.write('''
             #### Testing homogeneity of variance
             ''')
    st.write('''We need to check that the distribution is normal from each group (i.e. each bunker). We'll use Levene's Test.''')
    groups = []
    for substance in substances:
        for iconography in iconography_list:
            group_df = final_df[(final_df['Substances'] == substance) & (final_df['Religious_Iconography'] == iconography)]
            groups.append(group_df['Noise_Level'])
    result = stats.levene(groups[0], groups[1], groups[2], groups[3], groups[4], groups[5])
    st.code('''
for substance in substances:
    for iconography in iconography_list:
        group_df = final_df[(final_df['Substances'] == substance) & (final_df['Religious_Iconography'] == iconography)]
        groups.append(group_df['Noise_Level'])
stats.levene(groups[0], groups[1], groups[2], groups[3], groups[4], groups[5])
''', language='python')
    st.write(f'''{result}''')

def scene14():
    st.write('''
             #### Two-Way ANOVA Test

             ##### Grand Mean
             ''')
    st.code('''
final_df['Noise_Level'].mean()
            ''', language='python')
    st.write(f'{grand_mean}')
    st.write('''
            ##### Running ANOVA Linear Model
            ''')
    st.code('''
model = ols('Noise_Level ~ C(Substances) + C(Religious_Iconography) + C(Substances):C(Religious_Iconography)', data=final_df).fit()
anova_table = anova_lm(model, typ=2)
            ''', language='python')
    st.dataframe(anova_table)
    
def scene15():
    st.write('''
             ![](https://raw.githubusercontent.com/aipi510fall24foreverloop/assignment5resources/8cbdd55d55a09d3ec4547427dd88dd68ddcd35ed/bunker.jpeg)
             
             You: "Now we know there's a chance at warding off these monsters! Whatever they happen to be!"

             Everyone cheers over the channel.

             You: "Now I just need to figure out what ***specifically*** worked using a post-hoc test."

             Everyone:

             ![](https://i.redd.it/spongebob-you-what-meme-v0-54he65l7d02b1.png?width=432&format=png&auto=webp&s=e4694bcd8f6051ee80b6e6319a5aa203b55b4532)

             ![](https://preview.redd.it/ss3dlqgtfgq71.jpg?width=640&crop=smart&auto=webp&s=85756c17519cffd04d7e807144ad6abcbd3ddb8a)
             ''')

if ctx is not None:
    # Page navigation reference: https://discuss.streamlit.io/t/how-to-clear-screen-make-blank-again/30971/2
    if 'page' not in st.session_state:
        st.session_state.page = 0

    if st.session_state.page == 0:
        homepage()
    elif st.session_state.page == 1:
        staged_scene(scene1)
    elif st.session_state.page == 2:
        staged_scene(scene2)
    elif st.session_state.page == 3:
        staged_scene(scene3, action_text="What was that?!")
    elif st.session_state.page == 4:
        staged_scene(scene4, action_text="Tune the radio")
    elif st.session_state.page == 5:
        staged_scene(scene5, action_text="Hello!! I'm here!")
    elif st.session_state.page == 6:
        staged_scene(scene6, action_text="No, don't do it!!")
    elif st.session_state.page == 7:
        staged_scene(scene7)
    elif st.session_state.page == 8:
        staged_scene(scene8, action_text="I have an idea!")
    elif st.session_state.page == 9:
        staged_scene(scene9, action_text="Explain")
    elif st.session_state.page == 10:
        staged_scene(scene10, action_text="3 hours later...")
    elif st.session_state.page == 11:
        staged_scene(scene11, action_text="Check normality")
    elif st.session_state.page == 12:
        staged_scene(scene12, action_text="Check homogeneity of variance")
    elif st.session_state.page == 13:
        staged_scene(scene13, action_text="Perform Two-Way ANOVA")
    elif st.session_state.page == 14:
        staged_scene(scene14)
    elif st.session_state.page == 15:
        staged_scene(scene15, action_text="END", on_click=escape)
