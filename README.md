# Phase-based-ENF-extraction-method

** You can find the sample video data from [here](https://drive.google.com/file/d/1GQbCZ-SD3T_5vCKTJ4FDfPJMY9-iaEen/view?usp=sharing)

## About
This repository contains the main coding framework of the paper [A Phase-Based Approach for ENF Signal Extraction From Rolling Shutter Videos](https://ieeexplore.ieee.org/abstract/document/9822384), published at the IEEE Signal Processing Letters (SPL). 

## Evironment:
It is implemented with basic python signal processing libraries on Ubuntu 18.04 LTS.

PLEASE NOTE:

1. Do you have the FDR (Frequency Disturbance Recorder)?
   
We were using the FDR for collecting and storing ground truth reference ENF signals.

People with similar experimental environments like us will be able to use **(SPL)Phase-based_ENF_extracton_method.ipynb**.

If not, use the modified **(SPL)Phase-based_ENF_estimation+time-estimation_(using_stored_ground_truth_ENF).ipynb** to load the ground truth ENF of the saved sample video instead.

3. .npy file of your custom video
   
When running for the first time with your custom video, please uncomment the lines at the end of the first cell.
```
## when running for the first time
# cut the video into 2 minutes (2 sec~ 122 sec)
# F_ST = int(video.fps*(2*1))  
# F_ED = int(video.fps*(122*1)) 
# video.set_vector(F_ST, F_ED) 
### video.save_vector()
```
This allows you to save time by making the .npy file of your video that you want to inspect.
Once you run the code, you can re-comment the above lines as 
`video.load_vector()`
will load the saved .npy file.
   

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
