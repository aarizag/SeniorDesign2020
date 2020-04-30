# To Run
To run the completed project, ensure you have downloaded the model
by following the link in the `models` folder and run the following commands:
- `cd FinalProject`
- `python3 main.py`


It will take a lot time to load and create everything.

To improve the speed of the result, create a slimmer version of the UNSPSC 
file with the following commands:
- `cd FinalProject/utils`
- `python3 gen_slim_unspsc.py`
- `cd ../`
- `python3 main.py`