# Stonks (Senator-Periodic-Transactions)

#### Note: This program can only read electronically submitted data. Senators that submit handwritten documents will be ignored. 

This program is designed to scrape data from [`https://efdsearch.senate.gov/search/`](https://efdsearch.senate.gov/search/). It will then create [`graphs`](https://github.com/Anton22-del/Stonks/tree/main/Output%20Images) and generate a [`.csv`](https://raw.githubusercontent.com/Anton22-del/Stonks/main/Stonks%20v1.1/dist/Stock%20Data.csv) file containing the data it found. If the program crashes, update your `chromedriver.exe` (explained later) and make sure your inputs use the correct format.

## This Program Can Sort Data Outputs By:
* Year
* Month
* Max or Min values shown on [`https://efdsearch.senate.gov/search/`](https://efdsearch.senate.gov/search/)
* Senators
* Stocks or Bonds
* Stock/Stock Option/Corporate Bond (You Can Choose Multiple)
* .csv File Name
* Stock
* Pages to sort through
* Number of electronic vs scanned submissions
* Number of Amended Reports
* Most Sold Stock per Year, Month, and Senator
* Most Bought Stock per Year, Month, and Senator


## How To Use
#### Without Coding:
Download the repository .zip and extract all files. Navigate to `Stonks v1.1` -> `dist` and run `Stonks_updated.exe`. Follow the prompts that are given in the command window. If you aren't sure what commands to use, pressing enter will auto-fill each section.
1. If it crashes, `chromedriver.exe` is likely out of date
	1. Open chrome on your computer 
	2. Click the three-dot icon in the top-right corner
	3. Select Help > About Google Chrome
	4. Note your Chrome Version
	5. Go to [`https://chromedriver.chromium.org/downloads`](https://chromedriver.chromium.org/downloads) and download the same version of `chromedriver.exe`
	6. Extract and place chromedriver.exe in the same folder as `Stonks_updated.exe`
	7. This should stop the program from crashing
	
#### With Python:
Download Python and copy [`Stonks_updated.py`](https://github.com/Anton22-del/Stonks/blob/main/Python%20Files/Stonks_updated.py) into your Python IDE. Download the dependencies and run. If you aren't sure what commands to use, pressing enter will auto-fill each section.
1. If it crashes, `chromedriver.exe` is likely out of date
	1. Open chrome on your computer 
	2. Click the three-dot icon in the top-right corner
	3. Select Help > About Google Chrome
	4. Note your Chrome Version
	5. Go to [`https://chromedriver.chromium.org/downloads`](https://chromedriver.chromium.org/downloads) and download the same version of `chromedriver.exe`
	6. Extract and place chromedriver.exe in the same folder as `Stonks_updated.py`
	7. This should stop the program from crashing

Please excuse the length of the Python script. It is messy to look at, but it gets the job done.  
License: CC0
