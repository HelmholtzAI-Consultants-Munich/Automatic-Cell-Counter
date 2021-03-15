# Automatic Cell Counter

## What is this?
This repository provides an automatic cell counter algorithm to count cell numbers.

## Installation:
To install the necessary packages for this framework run:
```
pip install -r requirements.txt
```
If you are using conda first install pip by: ```conda install pip```


## Usage:

To run the cell counter, user could easily input following code in terminal. You should modify two parameters acoording to different input conditions.

**Require arguments**:

* -image: The path of the input image or the path of a directory.

```
python viewer.py --image example_data/8.tif
```
or
```
python viewer.py --image example_data/
```

**example output**:
The user interface for manual correction will be open for every image one by one. User could add dots or delete dots manually. After manual correction, **press 'd' (denotes Done) key on the keyboard to print the updated cell numbers on the terminal and close the current window.** When all images are corrected, an excel file called **result** will be generated and contain both automatically detected cell numbers and corrected cell numbers.

User interface for manual correction:
![image](https://github.com/HelmholtzAI-Consultants-Munich/Automatic-Cell-Counter/blob/master/images/example_result.png)

Example output on the terminal (left) and in the excel (right):
<p float="left">
  <img src="https://github.com/HelmholtzAI-Consultants-Munich/Automatic-Cell-Counter/blob/master/images/Terminal_output.png" width="400" />
  <img src="https://github.com/HelmholtzAI-Consultants-Munich/Automatic-Cell-Counter/blob/master/images/Excel_output.png" width="400" /> 
</p>

