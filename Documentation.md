## ETL Step Function Documentation:
For a given year, this step function can extract GDP data from the World Bank API, transform the data, return with the top 20 largest economies, then save it as CSV into S3 output bucket. It comprises of three lambda functions (extract, tranform, load) and the step functions state machine definition (JSON).<br>

#### Input to the step function:
The input year can be given by user in the following format:<br>
```
{
	"year": 2020
}
```

In this case, the output of the step function will be the CSV file with top 20 countries by GDP in the year 2020.<br>

#### Extract Lambda:
Extract GDP data from the World Bank API for a year specified by user, then save two JSON files (GDP data and Country List) into S3 input bucket.
- for a specified year, extract GDP data from the World Bank API, which are (1) GDP for various countries including aggregates such as GDP for Asia/Subsaharan Area/EU/EMEA, and (2) country list
- write two JSON files (GDP data and Country List) into the S3 input bucket
- pass the S3 input bucket name, and the file key (two JSON file names) to the next lambda (Transform)

#### Transform Lambda:
Transform the GDP data and return a JSON file with top 20 largest economies in the S3 input bucket
- get the input year, the S3 input bucket name, and the file keys from the Extract Lambda response body, as input 
- read the two JSON files from Extract Lambda, and convert them into Pandas dataframe
- remove non-related data
- remove group of countries (country aggregates, as referred by the World Bank API), such as Asia, Subsaharan Area, EU, EMEA. from the Country List, and only individual countries remain
- inner merge GDP data and Country List (without country aggregates), and choose only top 20 countries by GDP
- sort countries by GDP (ascending)
- reset index of the merged dataframe
- write the merged dataframe as a JSON file into S3 input bucket
- pass the S3 input bucket name, and the file key of the resulting JSON, to the next lambda (load)

#### Load Lambda:
Load the JSON file from Transform Lambda, and return CSV file saved in the S3 output bucket 
- get the input year, the S3 input bucket name, and the file key from the Transform Lambda response body, as input 
- read the JSON file writen by previous lambda (Transform)
- convert it into Pandas dataframe
- write the dataframe to CSV and save it in the S3 output bucket