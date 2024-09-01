import argparse
import requests
import pandas as pd
import matplotlib.pyplot as plt


def get_cli_argument():
    """ArgumentParser to accept inputs from user via command line: year [2023], top [10 countries], percapita [false]"""
    parser = argparse.ArgumentParser(description="Retrieve GDP data from World Bank API, and create a bar chart showing top largest economies by GDP")
    parser.add_argument("--year", type=int, dest="year", default = "2023", help="Year for the GDP chart")
    parser.add_argument("--top", type=int, dest="top", default = "10", help="Number of countries to show in the GDP chart (top largest)")
    parser.add_argument("--gdptype", type=int, dest="gdptype", default = "0", help="""0: GDP, Current USD
                        1: GDP per capita, Current USD
                        2: GDP Growth, Constant Local Currency""")
    args = parser.parse_args()
    if args.year < 1961: 
        raise RuntimeError("Available data starts from 1961")
    if args.top < 1: 
        raise RuntimeError("Number of top countries must be at least 1")
    if args.gdptype < 0 or args.gdptype > 2: 
        raise RuntimeError("""Available option: 0, 1, or 2:
                           0: GDP, Current USD
                           1: GDP per capita, Current USD
                           2: GDP Growth, Constant Local Currency""")   
    return args


def create_world_bank_argumentbased_url(year, gdptype):
    """Create a URL string for query from World Bank API"""
    match gdptype:
        case 0:
            return f"https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?per_page=1000&&format=json&date={year}"
        case 1:
            return f"https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?per_page=1000&&format=json&date={year}"
        case 2:
            return f"https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.KD.ZG?per_page=1000&&format=json&date={year}"  


def request_json(urlstring):
    """json request from urlstring and return json data"""
    try:
        response = requests.get(url=urlstring)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise RuntimeError("No json data returned from the World Bank API query")
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return data


def create_pd_dataframe(data, isgdpdata):
    """Read from json data and return pandas dataframe"""
    country_id, country_name, gdp_value = [], [], []
    if isgdpdata:
        # Create pandas dataframe for GDP data
        for country_entries in data[1]:
            country_id.append(country_entries['country']['id'])
            gdp_value.append(country_entries['value'])
        return pd.DataFrame([country_id, gdp_value], index=["country_id","gdp_value"]).T
    else:
        # Create pandas dataframe for the list of countries (excluding Aggregates)
        for country_entries in data[1]:
            if country_entries['region']['value'] != "Aggregates":
                country_id.append(country_entries['iso2Code'])
                country_name.append(country_entries['name'])
        return pd.DataFrame([country_id, country_name], index=["country_id","country_name"]).T


def main():
    """"""
    # Get all user's arguments
    args = get_cli_argument()
    year = args.year
    top = args.top
    gdptype = args.gdptype

    # Create an API query for the list of countries, get json data, create dataframe, and remove all Aggregates (group of countries/region) in order to get only the list of individual countries
    countrylist_apicall_url = "https://api.worldbank.org/v2/country?format=json&per_page=1000"
    countrylist_data = request_json(countrylist_apicall_url)
    countrylist_df = create_pd_dataframe(countrylist_data, isgdpdata=False)

    # Create an API query for GDP data, get json data, and create dataframe, which still includes Aggregates (such as GDP of Asia, GDP of Europe, etc.)
    gdp_apicall_url = create_world_bank_argumentbased_url(year, gdptype)
    gdp_data = request_json(gdp_apicall_url)
    gdp_df = create_pd_dataframe(gdp_data, isgdpdata=True)

    # Merge countrylist_df and gdp_df to remove all Aggregates' GDP data, and sort the data in descending order.
    gdp_noagg_df = pd.merge(countrylist_df, gdp_df, on = "country_id", how="inner").sort_values(by="gdp_value", ascending=False).head(top)
    # Reset index of the gdp_noagg_df dataframe, and set them to start from 1 instead of 0, so that the country with highest GDP value/per capita/growth will ranked as first
    gdp_noagg_df = gdp_noagg_df.reset_index(drop=True)
    gdp_noagg_df.index = gdp_noagg_df.index + 1

    # Rename gdp_value column to "gdp_percapita" or "gdp_growth", if applicable
    match gdptype:
        case 0:
            gdpcolumn = "gdp_value"
        case 1:
            gdpcolumn = "gdp_percapita"
        case 2:
            gdpcolumn = "gdp_growth"
    gdp_noagg_df.rename(columns={"gdp_value":gdpcolumn}, inplace=True)

    # Print the resulting table
    print(gdp_noagg_df)

    # Plot horizontal bar chart
    ax = gdp_noagg_df.sort_values(by=gdpcolumn, ascending=True).plot(kind="barh", x="country_name", y=gdpcolumn, legend=False, figsize=(16, 8), color='#86bf91')
    # Remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # Remove ticks
    ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
    # Create vertical axis lines
    vals = ax.get_xticks()
    for tick in vals:
        ax.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
    # Set axis label
    match gdptype:
        case 0:
            ylabel = f"GDP, {year}, Top {top}, based on current USD"
        case 1:
            ylabel = f"GDP per capita, {year}, Top {top}, based on current USD"
        case 2:
            ylabel = f"GDP Growth, {year}, Top {top}, based on constant local currency"
    ax.set_xlabel(ylabel, labelpad=20, weight='bold', size=12)
    ax.set_ylabel("Country", labelpad=20, weight='bold', size=12)
    plt.show()

    
if __name__ == '__main__':
	main()
