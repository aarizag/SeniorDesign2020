# To Run
After installing python 3.7.6,
https://www.python.org/downloads/release/python-376/
Go to the command line by pressing windows button
and type in cmd. When the terminal opens use this to install the packages:
- pip install xlwt xlsxwriter xlrd pandas gensim nltk progressbar
- make sure to read the readme file in models folder

To run the completed project, ensure you have downloaded the model
by following the link in the `models` folder and run the following commands:
- `cd FinalProject`
- `python3 main.py`

To get the County results:
- 'python3 GenCountyResults.py'


It will take a lot time to load and create everything.

To improve the speed of the result, create a slimmer version of the UNSPSC 
file with the following commands:
- `cd FinalProject/utils`
- `python3 gen_slim_unspsc.py`
- `cd ../`
- `python3 main.py`