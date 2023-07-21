# Phase-based-ENF-extraction-method

** You can find the sample video data from [here](https://drive.google.com/file/d/1GQbCZ-SD3T_5vCKTJ4FDfPJMY9-iaEen/view?usp=sharing)

## About
This repository contains the main coding framework of the paper [A Phase-Based Approach for ENF Signal Extraction From Rolling Shutter Videos](https://ieeexplore.ieee.org/abstract/document/9822384), published at the IEEE Signal Processing Letters (SPL). 

## Evironment:
It is implemented with basic python signal processing libraries on Ubuntu 18.04 LTS.

PLEASE NOTE:
We were using the FDR (Frequency Disturbance Recorder) for collecting and storing ground truth reference ENF signals.
People with similar experimental environments like us will be able to use #(SPL)Phase-based_ENF_extracton_method.ipynb. 

If not, use the modified #(SPL)Phase-based_ENF_estimation+time-estimation_(using_stored_ground_truth_ENF).ipynb to load the ground truth ENF of the saved sample video instead.
You might not be able to run "enf_ref"&"enf_ref_day" because they are the ground-truth ENF collected 


## Citation:
@article{han2022phase,
  title={A phase-based approach for ENF signal extraction from rolling shutter videos},
  author={Han, Hyekyung and Jeon, Youngbae and Song, Baek-kyung and Yoon, Ji Won},
  journal={IEEE Signal Processing Letters},
  volume={29},
  pages={1724--1728},
  year={2022},
  publisher={IEEE}
}
