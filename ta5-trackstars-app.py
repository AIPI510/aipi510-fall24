import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

# Streamlit  basics courtesy of https://docs.streamlit.io/get-started/fundamentals/main-concepts
#
# NB (from Streamlit docs): 
# Whenever a callback is passed to a widget via the on_change (or on_click) parameter, 
# the callback will always run before the rest of your script. For details on the Callbacks
# API, please refer to our Session State API Reference Guide.
#
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.0)

@st.cache_data
def stream(text): 
    st.write_stream(stream_data(text))

def init_state(): 
        st.session_state.button1 = False
        st.session_state.button2 = False
        st.session_state.button3 = False
        st.session_state.button4 = False
        st.session_state.button5 = False
        st.session_state.button6 = False

# Clicky *things to increase the drama
if 'button1' not in st.session_state:
    init_state()

def click_button1():
    st.session_state.button1 = True

def click_button2():
    st.session_state.button2 = True

def click_button3():
    st.session_state.button3 = True

def click_button4():
    st.session_state.button4 = True

def click_button5():
    st.session_state.button5 = True

def click_button6():
    st.session_state.button6 = True

month_coding = {
    'January': 'JAN',
    'February': 'FEB',
    'March': 'MAR',
    'April': 'APR',
    'May': 'MAY',
    'June': 'JUN',
    'July': 'JUL',
    'August': 'AUG',
    'September': 'SEP',
    'October': 'OCT',
    'November': 'NOV',
    'December': 'DEC'
}

def load_rainfall(path):
    """
    Fetch and preprocess the rainfall data
    """
    df = pd.read_csv(path)

    # The data is pretty ratty earlier than 1888
    df = df[df['YEAR']>1887]
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'] 
    for month in months: 
        df[month] = pd.to_numeric(df[month])
    
    return df

def load_river_crests(path):
    """
    Fetch and preprocess river crests/height data
    """
    df = pd.read_csv(path) 
    return df

def categorize_floods(df):
    """
    Categorize floods based on NOAA thresholds. See https://water.noaa.gov/gauges/avln7
    """
    flood_categories = {
        'major' : 18, 
        'moderate' : 13, 
        'minor' : 9.5, 
        'action' : 6.5
    }

    def categorize_crests(level): 
        """
        Assign flood categories based on water level
        """
        for category, height in flood_categories.items(): 
            if level >= height: 
                return category

    df['Category'] = df['Level'].apply(categorize_crests)

    return df

def plot_river_height(df): 
    """
    Generate a plot of river heights provided a dataframe that includes expected 
    columns (Level, Year)
    """
    df_major = df[df['Category'] == 'major']
    df_moderate = df[df['Category'] == 'moderate']
    df_minor = df[df['Category'] == 'minor']

    decades = range(1888, 2024, 5) 

    fig = plt.figure(figsize=[10,3])
    
    plt.bar(df_major['Year'], df_major['Level'],label='Major Flood Event', align='center', color='lightcoral')
    plt.bar(df_moderate['Year'], df_moderate['Level'], label='Moderate Flood Event', color='orange')
    plt.bar(df_minor['Year'], df_minor['Level'], label='Minor Flood Event', align='edge', color='khaki')
    plt.xlabel("Year") 
    plt.xticks(decades, rotation=90)
    plt.ylabel("River Crest (Feet)")
    plt.title("French Broad River Height, Flood Events, 1888-2023") 
    _ = plt.legend()
    
    # Critical insight on using the streamlit global pyplot instance to render pyplot-style charts
    # from https://discuss.streamlit.io/t/how-to-display-matplotlib-graphs-in-streamlit-application/35383/2
    st.pyplot(fig) 

def plot_ice_age_scale(df):
    
    millenia = range(-115000, 2024, 5000) 

    fig = plt.figure(figsize=[15,5])

    plt.bar(df['YEAR'], df['ANN'], label='September Rainfall', color='lightblue') 
    plt.bar([2024], df.iloc[-1]['SEP'], label='September 2024 Rainfall', color='red') 
    plt.xticks(millenia, rotation=90)
    plt.xlabel("Year") 
    plt.ylabel("Precipitation (Inches)")
    plt.title("Annual Rainfall in Asheville, 115,000 BCE - 2023 CE")
    _ = plt.legend()

    st.pyplot(fig) 

def plot_september_rainfall(df, df_flood):         
    
    fig = plt.figure(figsize=[15,5])

    plt.vlines(df_flood['Year'], ymin=0, ymax=25,label='Major Flood Event',color='lightcoral')
    plt.bar(df['YEAR'], df['SEP'], label='September Rainfall', color='lightblue') 

    plt.bar([2024], df.iloc[-1]['SEP'], label='September 2024 Rainfall', color='red') 
    plt.xlabel("Year") 
    plt.ylabel("Precipitation (Inches)")
    plt.title("September Rainfall in Asheville, 1888 - 2023")
    _ = plt.legend()

    st.pyplot(fig)

def plot_rainfall_anomalies(df, df2): 
    fig = plt.figure(figsize=[15,5])
    
    df2_major = df2[df2['Category'] == 'major']
    df2_moderate = df2[df2['Category'] == 'moderate']
    df2_minor = df2[df2['Category'] == 'minor']

    plt.vlines(df2_major['Year'], ymin=0, ymax=25,label='Major Flood Event',color='lightcoral')
    #plt.bar(df['YEAR'], df['ANN'], label='September Rainfall', color='lightblue') 
    plt.plot(df['YEAR'], df['ANN']/12, color='orange', label='Average Monthly Rainfall')
    plt.bar([2024], df.iloc[-1]['SEP'], label='September 2024 Rainfall', color='red') 
    plt.bar(df2_major['Year'], df2_major['Level'],label='Major Flood Event', align='center', color='lightcoral')
    plt.bar(df2_moderate['Year'], df2_moderate['Level'], label='Moderate Flood Event', color='orange')
    plt.bar(df2_minor['Year'], df2_minor['Level'], label='Minor Flood Event', align='edge', color='khaki')
    plt.xlabel("Year") 
    plt.ylabel("Precipitation (Inches)")
    plt.title("September Rainfall in Asheville, 1888 - 2023")
    _ = plt.legend()

    st.pyplot(fig)

def estimate_prior_rain(df, m, y): 
    """
    Get the two prior months of rainfall and return it
    """
    rain_prior = 0
    for i, month in enumerate(month_coding):
        if m == month:     

            # We don't transition year boundaries... fix when this assert hits, if ever
            assert(month != 'January' and month != 'February')
            
            prior_code = list(month_coding.values())[i-1]  
            rain_prior = df[df['YEAR']==y].iloc[0][prior_code]

            prior_code = list(month_coding.values())[i-2]  
            rain_prior = rain_prior + df[df['YEAR']==y].iloc[0][prior_code]
            
            return rain_prior    

st.title('🧪 Bayes Theorem Introduction')
stream('This app provides a loose introduction to Bayes theorem by way of a real-world example.')

st.button("Continue...", on_click=click_button1)

if st.session_state.button1: 

    st.header("Frequentist vs Bayesian Statistics")
    stream("It might be interesting to talk for a second about frequentist vs bayesian approaches to probability estimation.") 
    stream("Bayes theorem is often illustrated with an example where our belief about rain is adjusted based on the fact it's cloudy. This example is sort of unhelpful as we usually have so much in the way of historicals, that we can go the frequentist approach and just directly estimate the probability of rain based our long history of observations. Using a bayesian update technique in this case seems impractical, and indeed throws out a lot of data that you could use.") 
    stream("However, many situations do not have rich historicals to draw estimates from, or might be deviate wildly from the historicals, and either of these cases would be inferior to a bayesian approach that is really at its heart about trying to perpetually contextualize new observations")

    df = load_rainfall('ta5-trackstars-resources/avl_rainfall.csv')
    df2 = load_river_crests('ta5-trackstars-resources/avl_crests.csv')
    df2 = categorize_floods(df2) 

    plot_river_height(df2)

    stream("Probability of a major flood event (shown in red) is:")
    st.latex("p_{flood} = {\\dfrac{events}{years}}") 
    st.latex("p_{flood} = {\\dfrac{2}{2024-1888}}")
    st.latex("p_{flood} \\approx{0.015}")

    p_maj_flood = 2/(2024 - 1888)
    p_mod_flood = 6/(2025-1888) 
    p_flood = p_maj_flood + p_mod_flood 

    stream(f"The probability of a major flood event in Asheville based on historical events, prior to 2024 is ~= **{p_maj_flood:.2}**")
    stream(f"The probability of a moderate flood event in Asheville based on historical events, prior to 2024 is ~= **{p_mod_flood:.2}**")

    st.subheader("Challenges")
    stream("Note while 100+ years of measurements seems thorough, it's not even a remotely representative sample of what's happened with the weather since the last ice age. See the plot below for visual evidence of this.")  
    plot_ice_age_scale(df) 

    stream("We also have the problem with the frequentist approach of tracking changes with the underlying phenomenon. Here we see the flood event of 2024, which is ceertainly an outlier. Do we have other options for adapting to these types of changes?")    
    plot_september_rainfall(df, df2[df2['Category'] == 'major'])

    st.button("Continue to an overview of Bayes theorem", on_click=click_button2)
    if st.session_state.button2: 

        st.header("Bayesian Approach")

        st.subheader("Bayes Theorem")
        stream("Bayes theorem gives us a tool to cope with ad-hoc prior probabilities and rapidly evolving phenonema.")
        st.markdown("The degree to which a hypothesis **H** is likely to occur in the presence of evidence **E**\
                    can be related as a probability. We write this probability as **P(H|E)**, and we call this term\
                    the *likelihood*. The term yields the probability that $H$ is true in the context of **E**. The\
                    *likelihood* of **H** given **E**.In it's basic form, Bayes theorem gives us a way to compute that\
                    likelihood: ")
        st.markdown("In it's basic form, Bayes theorem gives us a way to compute that likelihood:")
        st.latex("P(H|E) = \dfrac{P(E|H)P(H)}{P(E)}")
        st.markdown("Here we also need information about our base or *prior* belief about **H**, **P(H)** and the \
                    likelihood that the evidence we're considering has demonstrated some influence on **H**, **P(E|H)**.\
                    These three values yield the estimate we're after, our *posterior* belief that **H** is likely given\
                     **E**.")

        st.button("Continue to Bayes Factor...", on_click=click_button3)
        if st.session_state.button3: 

            st.subheader("Bayes Factor")

            stream("We can and should talk about another way to think about what this equation is doing when solving for \
                   **P(H|E)**. The likelihood of the evidence in the context of the hypothesis, normalized by the \
                   probability of the evidence is called the **Bayes Factor**.")

            st.latex("P(H|E) = {BF}\cdot{P(H)}")
            st.latex("P(H|E) = \dfrac{P(E|H)}{P(E)}\cdot{P(H)}")

            stream("The Bayes Factor scales the likelihood of the *prior* belief. Essentially we incorporate the new\
                   information *to the degree it has bearing on the hypothesis we care about. Where the new information\
                   supports our old information, we want to increase the likelihood estimate. Where the new information\
                   rejects our old information, we want to erode the likelihood estimate.")
            stream("Said another way, if the evidence is more likely to occur than the base rate, in the context of the \
                   hypothesis, it should strengthen the hypothesis. If the evidence is less likely to occur than the base \
                   rate, in the context of the hypothesis, it should weaken H.") 
            stream("**Bayes factor is the ratio of the likelihood of the conditioned event to the unconditioned global probabilty.**")


            st.button("Continue to example...", on_click=click_button4)
            if st.session_state.button4: 

                st.subheader("Likelihood of a flood following above-average rainfall")
                stream("We'll resume with the example used above to compute the historical probability of rain in Asheville, NC.")
                stream("We know the proximate cause of a flood event is rain. But let's say we suspect an underappreciated \
                       factor of the flooding is that the soil was saturated at the time the rain arrived. That is, the \
                       ground had no further capacity to absorb water and thus contributed to the likelihood heavy rain \
                       pools to create flood conditions.") 

                st.markdown("**Question**: What is the chance of having a flood event if we have above average rain event the months preceding the flood?")
                st.markdown("""\
                    - We have computed an estimate for the probability of a flood based on historical measurements, **P(flood)**
                    - We can compute the probability of above average rain events, **P(rain_abnormal)**
                    - We need to know in historical flood conditions, what is the probability that we had above average rain in \
                    the months prior? I.e. **P(rain_abnormal|flood)**""") 

                stream("The answer to our question is as follows.") 
                st.latex("P(flood|rain_{abnormal}) = \dfrac{P(rain_{abnormal}|flood) P(flood)}{P(rain_{abnormal})}") 

                ###
                st.markdown("#### 1 - Probability of a flood")
                stream(f"The probability of major or moderate flooding computed above, from historical data is **{p_flood:.2}**")
                
                ###
                st.markdown("#### 2 - Historical probability of above average rain event")

                average_rainfall = df['ANN'].sum()/(df['YEAR'].max() - df['YEAR'].min())
                average_monthly_rainfall = average_rainfall / 12

                above_average_months = 0 
                for month in month_coding.values():
                    above_average_months = above_average_months + df[df[month] > average_monthly_rainfall].count().iloc[0] 

                # Rows in the data set (one per year) * 12 months each, plus or minus 
                total_months = df.count().iloc[0] * 12

                p_excess_rain = above_average_months/total_months

                stream(f"Across **{total_months}** months in the dataset, the average monthly rainfall is \
                    **{average_monthly_rainfall:.2}** inches, and **{above_average_months}** exceeded that. The \
                    historical probability of a month with rain in excess of the average is \
                    **{p_excess_rain:.2}**, accordingly.")

                ###
                st.markdown("#### 3 - Likelihood of excessive rain prior to flood.")
                stream("We need to estimate the likelihood that we have excess rainfall in the months leading up to a flood.\
                        This is the **P(rainfall|flood)** term.")

                df2_flood = df2[df2['Category'].isin(['major','moderate'])]
                df2_flood['Rain2mo'] = df2_flood.apply(lambda x: estimate_prior_rain(df, x.Month, x.Year), axis=1)

                flood_event_count = df2_flood.count().iloc[0]

                # Number of rows where the two months prior had rain exceeding the average
                excess_rain_prior_month_count = df2_flood[df2_flood['Rain2mo'] > (average_monthly_rainfall * 2)].count().iloc[0]

                p_excess_rain_given_flood = excess_rain_prior_month_count/flood_event_count

                stream(f"Of the **{flood_event_count}** flood events, **{excess_rain_prior_month_count}** had rain \
                in the prior two months that exceeded the historical monthly average. The probability \
                of excess rainfall leading up to a flood is hence **{p_excess_rain_given_flood:.2}**")
                
                ###
                st.markdown("#### 4 - Application of Bayes Theorem")
                p_flood_given_abnormal_rain = p_excess_rain_given_flood * p_flood / p_excess_rain
                stream(f"The base rate for historical floods is **{p_flood:.3}**.")

                st.latex("P(flood|rain_{abnormal}) = \dfrac{P(rain_{abnormal}|flood) P(flood)}{P(rain_{abnormal})}")
                st.latex("P(flood|rain_{abnormal}) = \dfrac{0.86 \cdot 0.058}{0.43}")
                st.latex("P(flood|rain_{abnormal}) = 0.116")
                
                stream(f"Bayes theorem helps us calculate that the likelihood of a flood, when the two months prior \
                    experience above average rainfall, is **{p_flood_given_abnormal_rain:.3}**.") 

                stream(f"We can get some better intuition about the power of the evidence here by computing\
                        the Bayes factor first and examining its effect on the prior probability.") 
                
                st.latex("P(flood|rain_{abnormal}) = {Bayes factor}\cdot{P(rain_{abnormal})}")
                st.latex("P(flood|rain_{abnormal}) = \\dfrac{0.86}{0.43}\cdot{0.058}") 
                st.latex("P(flood|rain_{abnormal}) = \\textbf{2.05}\cdot\\textit{0.058}") 

                stream("We see that the **Bayes factor** will essentially double the belief in our *prior* belief.") 

                st.button("Continue to conclusion...", on_click=click_button5)
                if st.session_state.button5: 
                    st.header("Conclusion")

                    plot_rainfall_anomalies(df, df2)

                    stream("Bayes theorem gives us a tool to adjust likelihood (of a hypothesis, prediction, event, ...) based on \
                           the arrival of some new evidence. It is at the heart of a number of interesting algorithms that use \
                           a belief updated process to do practical things like track the stock market, moving aircraft and robot positions.")
                    
                    st.markdown("Continue on learning about Bayesian filters, a much more interesting topic [here](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python).")

                    stream("❤️, Team Trackstars")
                    
