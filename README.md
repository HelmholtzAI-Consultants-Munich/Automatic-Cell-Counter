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

To run the cell counter, user could easily input following code in the terminal.
**Require arguments**:

* -image: The path of the input image or the path of the directory.

```
python viewer.py --image example_data/8.tif
```
or
```
python viewer.py --image example_data/
```

**example output**:

The user interface will be built based on every input image for manual correction. Inside each image, red dots are used to denote the centers of detected cells. We also used green dots and red bounding boxes to guide users to pay more attention to those easy-to-make-mistake areas: green dots (detected cells are quite small, perhaps one cell is divided to several parts) and red bounding box (high density areas, perhaps two cells are merged). User could add dots or delete dots manually based on the automatically detected results. 

After manual correction, **press 'd' (denotes Done) key on the keyboard to print the updated cell numbers on the terminal and close the current window.** When all images are corrected, an excel file called **result** will be generated and contain both automatically detected cell numbers and corrected cell numbers.

User interface for manual correction:
![image](https://github.com/HelmholtzAI-Consultants-Munich/Automatic-Cell-Counter/blob/master/images/example_result.png)

Example output on the terminal (left) and in the excel (right):
<p float="left">
  <img src="https://github.com/HelmholtzAI-Consultants-Munich/Automatic-Cell-Counter/blob/master/images/Terminal_output.png" width="350" />
  <img src="https://github.com/HelmholtzAI-Consultants-Munich/Automatic-Cell-Counter/blob/master/images/Excel_output.png" width="350" /> 
</p>

