# Dataset Guide

This guide documents the dataset formats expected by the notebooks in this repository.

The repo currently mixes multiple stages of the EEG pipeline:

1. raw `.edf` recordings
2. subject-level `.csv` exports
3. preprocessed combined training CSVs
4. DWT-transformed feature CSVs

Because the notebooks were developed iteratively, they do not all use the same exact schema. This file is the clean reference for what each notebook expects.

## 1. Raw EEG Source Dataset

Used in:

- [MAT_Preprocessing.ipynb](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/MAT_Preprocessing.ipynb)

Expected source:

- EDF files from the EEG mental arithmetic dataset

Observed path in notebook:

```text
/content/drive/MyDrive/Signal_Processing/data_set_eeg-during-mental-arithmetic-tasks-1.0.0/eeg-during-mental-arithmetic-tasks-1.0.0/
```

Expected filenames:

```text
Subject01_1.edf
Subject01_2.edf
Subject10_2.edf
Subject20_1.edf
...
```

Loading method:

- `mne.io.read_raw_edf(...)`

Purpose:

- convert EDF recordings into CSV for downstream preprocessing and model training

## 2. Subject-Level CSV Exports

Used in:

- [MAT_Preprocessing.ipynb](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/MAT_Preprocessing.ipynb)

Expected filenames:

```text
Subject01_1.csv
Subject01_2.csv
...
```

Observed important columns:

- `AF3`
- `F7`
- `F3`
- `FC5`
- `T7`
- `P7`
- `O1`
- `O2`
- `P8`
- `T8`
- `FC6`
- `F4`
- `F8`
- `AF4`
- `# COUNTER`

Notes:

- The notebook explicitly selects the 14 EEG channels above.
- `# COUNTER` appears to be kept as an auxiliary signal/timestamp-like column.
- The notebook mentions both `500 Hz` and later `128 Hz` processing assumptions.

Typical format:

```text
AF3,F7,F3,FC5,T7,P7,O1,O2,P8,T8,FC6,F4,F8,AF4,# COUNTER
...
```

Purpose:

- filtering
- ICA artifact removal
- export into cleaned CSV files

## 3. Preprocessed EEG CSV Output

Produced in:

- [MAT_Preprocessing.ipynb](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/MAT_Preprocessing.ipynb)

Observed output path:

```text
/content/drive/MyDrive/Signal_Processing/preprocessed_data/
```

Observed output pattern:

```text
Subject01_1.csvica_butter
```

Notes:

- This naming is messy in the notebook and likely needs cleanup in a future refactor.
- These files appear to contain filtered EEG channel data after ICA/bandpass steps.

## 4. Combined Training CSV For Deep Learning

Used in:

- [DEEPLEARNING_EEG.ipynb](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/DEEPLEARNING_EEG.ipynb)

Observed input path:

```text
/content/drive/MyDrive/Sam40/final_datset_Sam40_Mat/Combined_Data.csv
```

Observed characteristics:

- shape shown in notebook: `768000 rows x 33 columns`
- intended for train/test split and deep learning models
- one label column is expected

Important inconsistency:

- some notebook cells use `data['label']`
- other notebook cells use `target`

Most likely intended schema:

- 32 feature columns
- 1 binary label column

Likely format:

```text
feature_1,feature_2,...,feature_32,label
```

or

```text
feature_1,feature_2,...,feature_32,target
```

How the notebook uses it:

- epoch construction:
  - `epoch_size = 128`
  - overlapping windows
- deep learning input:
  - examples show input shapes like `(32, 1)`

Recommendation:

- standardize this file to use exactly one target column name, preferably `label`

## 5. DWT Raw CSV Inputs

Used in:

- [DWT.ipynb](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/DWT.ipynb)

Observed input folders:

```text
/content/drive/MyDrive/filtered_data_csv/Arithmetic_task/
/content/drive/MyDrive/wewill2
/content/drive/MyDrive/try1
```

Observed file pattern:

```text
Arithmetic_sub_10_trial1.csv
...
```

Expected columns in some cells:

- EEG columns named numerically:
  - `"0"`, `"1"`, `"2"`, ..., `"31"`
- plus:
  - `target`

Likely raw DWT input format:

```text
0,1,2,3,...,31,target
...
```

Purpose:

- compute wavelet coefficients
- derive arithmetic/statistical features

Important note:

- This is different from the 14-channel schema used in `MAT_Preprocessing.ipynb`
- So the repo mixes at least two EEG tabular schemas:
  - 14 named channels
  - 32 indexed channels

## 6. DWT Coefficient Datasets

Produced in:

- [DWT.ipynb](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/DWT.ipynb)

Observed intermediate output folder:

```text
/content/drive/MyDrive/wewill2
```

Observed coefficient columns:

- `{channel}_cA5`
- `{channel}_cD5`
- `{channel}_cD4`
- `{channel}_cD3`
- `{channel}_cD2`
- plus `target`

Example shape shown:

- `966 rows x 161 columns`

Purpose:

- store wavelet decomposition outputs for each EEG channel

## 7. DWT Feature Datasets

Produced in:

- [DWT.ipynb](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/DWT.ipynb)

Observed output folder:

```text
/content/drive/MyDrive/8_feactures
```

Observed output file:

```text
features.csv
```

Observed feature naming pattern:

- `{channel}_{coefficient}_mean`
- `{channel}_{coefficient}_std`
- `{channel}_{coefficient}_skewness`
- `{channel}_{coefficient}_kurtosis`
- `{channel}_{coefficient}_entropy`
- `{channel}_{coefficient}_energy`
- plus `target`

Observed examples:

- `31_cD2_skewness`
- `31_cD2_kurtosis`
- `31_cD2_entropy`
- `31_cD2_energy`

Observed shapes:

- one notebook stage shows `966 rows x 161 columns`
- another stage shows `1 rows x 961 columns`

This suggests multiple feature-generation attempts exist in the notebook.

## 8. Synthetic Demo Dataset In This Repo

Added for the app and baseline ML example:

- [synthetic_cognitive_load_dataset.csv](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/data/synthetic_cognitive_load_dataset.csv)

This dataset is:

- synthetic
- not the original EEG research dataset
- suitable for demo UI flows and baseline model scaffolding

It should not be confused with the deep learning notebook inputs above.

## Summary Of Expected Dataset Types

### A. Raw research source

- `.edf` files
- per subject/session EEG recordings

### B. Converted tabular EEG

- `.csv`
- either 14 named EEG channels plus `# COUNTER`
- or 32 indexed channel columns plus `target`

### C. Combined deep learning dataset

- `Combined_Data.csv`
- around 32 feature columns plus one binary label

### D. DWT engineered datasets

- coefficient-level CSVs
- feature-level CSVs
- always expecting a `target` label

## Known Problems In The Current Notebook Workflow

1. Target column name is inconsistent:
- `label`
- `target`

2. Channel schema is inconsistent:
- 14 named channels
- 32 indexed channels

3. Paths are hardcoded to Google Drive:
- `/content/drive/...`

4. Some notebook cells are incomplete or broken:
- shape mismatch errors
- indentation errors
- file-not-found errors

## Recommended Standardization

If you want to make the repo easier to run, use this standard:

### Deep learning standard

- file: `data/Combined_Data.csv`
- columns:
  - `f1` to `f32`
  - `label`

### DWT standard

- file: `data/features.csv`
- columns:
  - engineered wavelet features
  - `target`

### Raw EEG standard

- folder: `data/raw_edf/`
- files:
  - `Subject##_#.edf`

## Best Next Step

The cleanest next improvement would be to refactor the notebooks so they all point to a repo-local `data/` folder and use one consistent target column name.
