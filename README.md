# House Price EDA (Greater Jakarta Region)
## Overview
An exploratory data analysis of residential listing in Greater Jakarta region. This projects aim to analyze property price patterns across different cities , evaluate price per square meter, and identify regional differences in house markets.

The analysis focuses on comparing:
* Property Prices
* Price per Square Meter
* House Size Across Cities

## Objective
* Identify price distribution across cities
* Compare property value using price per m2
* Understand market segmentation (premium vs affordable areas)

## Findings
* South Jakarta represents the premium housing market (high price & large house size)
* Bekasi has the highest price per m² despite smaller house sizes
* Depok offers the most affordable housing options
* West Jakarta provides larger houses with relatively moderate prices

## Vizualitation
Price Distribution by City
![Alt text](https://github.com/Surge0Name/house_listing/blob/main/images/boxplot_price.png)

Median and Mean Price per m2
![Alt text](https://github.com/Surge0Name/house_listing/blob/main/images/mean_median_barplot.png)

Properties Values Comparison
![Alt text](https://github.com/Surge0Name/house_listing/blob/main/images/propertyvalue_scatterp.png)

## Data Extraction and Preprocessing
The data was acquired by scrapping house listing website using selenium, cleaned, and preprocessed
Preprocessing steps include:
* Filled any missing data
* Convert price and building size data into numeric format
* Created new feature: price_per_m2
* Perform outliers analysis
* Use log transformation on price because price is extremely right skewed

Full analysis here:
:point_right:   PDF: [Link Text](https://github.com/Surge0Name/house_listing/blob/main/report/House%20Listings%20EDA%20Report.pdf)

:point_right:   Jupyter Notebook: [Link Text](https://github.com/Surge0Name/house_listing/blob/main/notebook/eda.ipynb)

Author:
I Gede Sanjaya Putra Vhysa
A.K.A
Yer Boi

