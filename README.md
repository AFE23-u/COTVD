# CoTVD Package
Package for "CoTVD: A Function-Level Vulnerability Detection Framework Using Chain-of-Thought Reasoning"

## code

1. joern.py: Utilize Joern to extract the target function slice. Here we show an example of a code dependency slice extraction algorithm in the paper (We should have displayed in the corresponding position in the paper, very sorry.). ![CleanShot 2024-11-06 at 11 10 14@2x](https://github.com/user-attachments/assets/9f30f77d-7eb2-4331-a58a-045e4e403376)
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
