# Final Project for MCEN 5133

This is the GitHub repository for MCEN 5133: Introduction to Tissue Biomechanics.

Authors:

* Yesica Tellez
* Matthew French
* Josh Gregory

## Overview of the Project

One of our team members (Josh Gregory) injured himself while running an (unplanned) half-marathon. After going to physical therapy for his injury, he found that altering his strike pattern to hit heel first alleviated much of the pain.

For this project, we wanted to investigate the impact of foot-strike patterns on strain in the foot. We found a paper that collected running data at a variety of speeds for runners that ran with different strike patterns (rearfoot, midfoot, and forefoot) [1]. The data used here are taken from the paper and run through our Python code.

### Code Description

To start, the code (`data_read.py`) reads in the metadata spreadsheet and extracts several key points of information. Firstly, it removes all of the duplicate rows so that there is one row per participant. It then finds all of the instances where the runner's right foot has a forefoot, midfoot, and rearfoot strike pattern at 3.5 m/s, saving the corresponding raw file path in the list.

The `data_read` function then reads in each of these file paths stored in the `forefoot`, `midfoot`, and `rearfoot` lists, pulling out the relevant data labels. The `format_data` function is then called, which wraps each point in the form `<pt>value,value</pt>`, which is what FEBio reads. This is done for reach of the raw data files in `forefoot`, `midfoot`, and `rearfoot`, with each foot strike pattern being saved in its own directory (i.e. `processed/midfoot`).

These points were then inserted into an FEBio simulation, utilizing the Cleveland Clinic's [foot model](https://repo.febio.org/permalink/project/25).

The Python script `strain_stats.py` takes the strain written to the Models/Forefoot, Models/Midfoot, and Models/Rearfoot CSV files and calculates the maximum strain for each patient (i.e. takes the range of each column of the CSV file that corresponds to each patient). It then runs an ANOVA test with the entire dataset and then a t-test with only the midfoot and rearfoot datasets.

## References

[1] Fukuchi RK, Fukuchi CA, Duarte M. A public dataset of running biomechanics and the effects of running speed on lower extremity kinematics and kinetics. PeerJ. 2017 May 9;5:e3298. doi: 10.7717/peerj.3298. PMID: 28503379; PMCID: PMC5426356.
