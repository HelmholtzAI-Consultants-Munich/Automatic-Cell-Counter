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

* -image: The path of the input image.
* -dense: Whether the cells are dense or not in the input image, default True. If True, watershed algorithm will be applied.

```
python viewer.py --image images/8.tif --dense False 
```


