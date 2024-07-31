# Hastings Botsford persistence disequation
Python program to calculate Hastings Botsford Persistence from a generic NxN matrix

See: https://www.pnas.org/doi/10.1073/pnas.0506651103

## Requirements
You'll need python 3 in order to run this project.

## Getting started
Open a command prompt.
Clone / Download this repository, and cd into it.

```bash
git clone https://github.com/xtimk/hastings-botsford-persistence.git
cd hastings-botsford-persistence
```

Create python virtual environment
```bash
python -m venv env
```

And activate it
```bash
.\env\Scripts\activate
```

Then we can install all required dependencies.
```bash
pip install -r requirements.txt
```

## How to use it
Put your input matrix into ```inputMatrix.txt```

Example
```
1    2    1    0.5
0.3  0.6  0.8  1
2    3    1.4  0.8
0    0    1    3
```

Then launch the program
```bash
python .\hb-persistence.py
```

At the end 2 outputs will be showed
The generic formula and the actual result

Output example
```bash
[INFO] 2024-07-31 08:45:28,915: ((1) * Q_12 Q_21/ Q_11 Q_22) + ((1) * Q_13 Q_31/ Q_11 Q_33) + ((1) * Q_14 Q_41/ Q_11 Q_44) + ((1) * Q_23 Q_32/ Q_22 Q_33) + ((1) * Q_24 Q_42/ Q_22 Q_44) + ((1) * Q_34 Q_43/ Q_33 Q_44) + ((1) * Q_12 Q_23 Q_31/ Q_11 Q_22 Q_33) + ((1) * Q_13 Q_21 Q_32/ Q_11 Q_22 Q_33) + ((1) * Q_12 Q_24 Q_41/ Q_11 Q_22 Q_44) + ((1) * Q_14 Q_21 Q_42/ Q_11 Q_22 Q_44) + ((1) * Q_13 Q_34 Q_41/ Q_11 Q_33 Q_44) + ((1) * Q_14 Q_31 Q_43/ Q_11 Q_33 Q_44) + ((1) * Q_23 Q_34 Q_42/ Q_22 Q_33 Q_44) + ((1) * Q_24 Q_32 Q_43/ Q_22 Q_33 Q_44) + ((-1) * Q_12 Q_21 Q_34 Q_43/ Q_11 Q_22 Q_33 Q_44) + ((1) * Q_12 Q_23 Q_34 Q_41/ Q_11 Q_22 Q_33 Q_44) + ((1) * Q_12 Q_24 Q_31 Q_43/ Q_11 Q_22 Q_33 Q_44) + 
((1) * Q_13 Q_21 Q_34 Q_42/ Q_11 Q_22 Q_33 Q_44) + ((-1) * Q_13 Q_24 Q_31 Q_42/ Q_11 Q_22 Q_33 Q_44) + ((1) * Q_13 Q_24 Q_32 Q_41/ Q_11 Q_22 Q_33 Q_44) + ((1) * Q_14 Q_21 Q_32 Q_43/ Q_11 Q_22 Q_33 Q_44) + ((1) * Q_14 Q_23 Q_31 Q_42/ Q_11 Q_22 Q_33 Q_44) + ((-1) * Q_14 Q_23 Q_32 Q_41/ Q_11 Q_22 Q_33 Q_44) > 1
[INFO] 2024-07-31 08:45:28,916: 1.5753968253968254 > 1
```

Output will be printed to console and into ```hb-pers.log``` file.

## Debugging problems
Feel free to contribute and/or open Issues if you find any bug/problem.
You can get some more detailed infos by running program in DEBUG mode. In order to set DEBUG mode, edit line 11 of hb-persistence.py, and set 
```python
level = logging.DEBUG
```
