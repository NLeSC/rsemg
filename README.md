# rsemg

<p align="center">
    <img style="width: 30%; height: 30%" src="https://github.com/NLeSC/rsemg/blob/main/rsemgU.png">
</p>


This library contains functions, scripts and notebooks for machine learning related to EMGs (electromyograms). The work of the research group will include interfaces for clinicians as well as researchers.

### Folders and Notebooks


researcher_interface:
- These are a growing series of interactive notebooks that allow researchers to investigate questions about their own EMG data

open_work:
- This folder contains experimental work by core members of the rsemg team


### Program files

The main program in this repository contains functions for analysis of EMG.


## Data sets

The notebooks are configured to run on various datasets.
Contact Candace Makeda Moore (c.moore@esciencecenter.nl) to discuss any questions on data configuration. 

## Getting started

How to get the notebooks running? Assuming the raw data set and metadata is available.

1. Install all Python packages required, using conda and the environment.yml file.
1a. The command for Windows/Anaconda users can be something like: conda env create -f environment.yml
1b. Linux users can create their own environment by hand

2. Open a notebook in researcher_interface and interactively run the cells.