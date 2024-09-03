# Team MIA Assignment #1

### Ensure you use Python versions around 3.10 in your virtual environment, as versions around 3.12 may cause issues!

## Installation
1. Clone this repo

```bash
git clone https://github.com/AIPI510/aipi510-fall24.git
```

2. Go into the directory where this repo was cloned
```bash
cd aipi510-fall24
```

3. Checkout the ta1-mia branch to retrieve our team's changes
```bash
git checkout ta1-mia
```

3. Install the required dependencies using the following command
```bash
pip install requirements.txt
```

4. Run the api_opensky.py script and follow instructions in terminal to use the application
```bash
python data_visualization_opensky.py
```

## Notes
* Upon running the live tracking web app there may be an error that shows up as follows
```
Traceback (most recent call last):
  File "c:\Users\aryan\Documents\aipi510-fall24\data_visualization_opensky.py", line 171, in update_graph
    for state in state_vectors.states:
AttributeError: 'NoneType' object has no attribute 'states'
```
This is expected and simply requires a refresh of the page or waiting a few seconds for the page to automatically update

