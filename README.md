# Hastings Botsford persistence disequation
Python program to calculate Hastings Botsford Persistence from a generic NxN matrix

See: https://www.pnas.org/doi/10.1073/pnas.0506651103

The formula implemented here is
![hastings Botsford persistence](./images/HBformula.png)

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
Put your input matrix into a txt file. 

For example create ```inputMatrix.txt``` and put in the following matrix
```
0    0.8  0.5  0.5
0.3  0.6  0.8  1
0.5  0.3  0.4  0.8
0    0    0.7  0.1
```

Then launch the program and specify the file containing the input matrix.
```bash
python .\hb-persistence.py inputMatrix.txt
```

The program will produce 3 outputs:

 - The generic formula 
 - A simplified formula, obtained by removing the zero elements from the generic formula
 - The actual calculation.

Output example
```bash
[INFO] 2024-07-31 12:02:49,070: Generic Full Disequation:
   ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_23 Q_31/(1 - Q_11)(1 - Q_22)(1 - Q_33)) + ( Q_13 Q_21 Q_32/(1 - Q_11)(1 - Q_22)(1 - Q_33))
 + ( Q_12 Q_23 Q_31/(1 - Q_11)(1 - Q_22)(1 - Q_33)) + ( Q_13 Q_21 Q_32/(1 - Q_11)(1 - Q_22)(1 - Q_33))
 + ( Q_12 Q_23 Q_31/(1 - Q_11)(1 - Q_22)(1 - Q_33)) + ( Q_13 Q_21 Q_32/(1 - Q_11)(1 - Q_22)(1 - Q_33))
 + ( Q_12 Q_23 Q_31/(1 - Q_11)(1 - Q_22)(1 - Q_33)) + ( Q_13 Q_21 Q_32/(1 - Q_11)(1 - Q_22)(1 - Q_33))
 + (- Q_12 Q_21 Q_34 Q_43/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_12 Q_23 Q_34 Q_41/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_12 Q_24 Q_31 Q_43/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_13 Q_21 Q_34 Q_42/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + (- Q_13 Q_24 Q_31 Q_42/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_13 Q_24 Q_32 Q_41/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_14 Q_21 Q_32 Q_43/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_14 Q_23 Q_31 Q_42/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + (- Q_14 Q_23 Q_32 Q_41/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) > 1
[INFO] 2024-07-31 12:02:49,072: Generic Disequation also considering presence of zeros:
   ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_21/(1 - Q_11)(1 - Q_22))
 + ( Q_12 Q_23 Q_31/(1 - Q_11)(1 - Q_22)(1 - Q_33)) + ( Q_13 Q_21 Q_32/(1 - Q_11)(1 - Q_22)(1 - Q_33))
 + ( Q_13 Q_21 Q_32/(1 - Q_11)(1 - Q_22)(1 - Q_33))
 + ( Q_13 Q_21 Q_32/(1 - Q_11)(1 - Q_22)(1 - Q_33))
 + (- Q_12 Q_21 Q_34 Q_43/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_12 Q_24 Q_31 Q_43/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) + ( Q_14 Q_21 Q_32 Q_43/(1 - Q_11)(1 - Q_22)(1 - Q_33)(1 - Q_44)) > 1
[INFO] 2024-07-31 12:02:49,073: Actual Disequation: 6.69074074 > 1
[INFO] 2024-07-31 12:02:49,074: All done
```

Output will be printed to console and into ```hb-pers.log``` file.

## Debugging problems
Feel free to contribute and/or open Issues if you find any bug/problem.
You can get some more detailed infos by running program in DEBUG mode. In order to set DEBUG mode, edit line 11 of hb-persistence.py, and set 
```python
level = logging.DEBUG
```
