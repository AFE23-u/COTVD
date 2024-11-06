# COTVD Package

## code

1. joern.py: Utilize Joern to extract the target function slice. Here we show an example of a code dependency slice extraction algorithm in the paper. [流图.pdf](https://github.com/user-attachments/files/17641179/default.pdf)![CleanShot 2024-11-06 at 11 10 14@2x](https://github.com/user-attachments/assets/8c912ee8-26ad-41e5-bc9c-0767339260c0)

2. rm_no_slice: Remove invalid samples.
3. merge: Merge datasets.
4. prompt: Generate prompts for the merged dataset.

## data

1. SourceSlice: COTVD's detection results on prompts and negative samples.
2. Abalation: Used for ablation experiment prompts.
3. cotvd.json: Complete data set constructed by COTVD.
4. test.json: COTVD test dataset.
5. Other datasets and data processing middleware.

## originData

1. Devign.json: Devign origin dataset.
2. Reveal\*.json: Reveal origin dataset.

## baselines

The package contains the implementations of two deep learning models compared by COTVD.

## Due to GitHub upload limits, the complete version is on Google Drive
[https://drive.google.com/drive/folders/1hOpAYKFUGXAn4YVOapJYO487F-If7PUi?usp=share_link](https://drive.google.com/drive/folders/1hOpAYKFUGXAn4YVOapJYO487F-If7PUi?usp=share_link)
