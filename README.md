# Team Assignment #1
## Data Sourcing
World Bank API

This is a Python script that can request GDP data from World Bank API, print resulting table, draw horizontal bar chart, and save the result as CSV.

## Installation

1. Install all dependencies
```
pip install -r requirements.txt
```

2. To run the code, type the followings in the terminal
On Windows:
```
py api_world_bank.py --year <YEAR> --top <TOP> --gdptyp <TYPE>
```
On other systems:
```
python api_world_bank.py --year <YEAR> --top <TOP> --gdptyp <TYPE>
```

where   `<YEAR>` is the input year for the GDP data [default = 2023]
        `<TOP>` is number of top countries to show in the GDP chart (top largest) [default = 10]
        `<TYPE>` can be either 0, 1, or 2 [default = 0]
                0: GDP, Current USD
                1: GDP per capita, Current USD
                2: GDP Growth, Constant Local Currency

For example, to get top `5` largest economies in `2020` by GDP:
```
py api_world_bank.py --year 2020 --top 5 --gdptyp 0
```
You should see output like this:
```
  country_id    country_name             gdp_value
1         US   United States        21322950000000
2         CN           China        14687744162801
3         JP           Japan  5055587093501.589844
4         DE         Germany  3887727161914.410156
5         GB  United Kingdom  2697806592293.859863
```
The horizontal bar chart should pop up automatically


## Unit Test
Run `pytest`
```
pytest api_world_bank.py
```
This will run 4 test functions in api_world_bank.py
