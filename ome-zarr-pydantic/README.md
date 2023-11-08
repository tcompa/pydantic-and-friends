# OME-Zarr Pydantic Project

> Note: Project should be a OME-Zarr Reader/Writer IMHO

<!-- TOC tocDepth:2..6 chapterDepth:2..6 -->

- [OME-Zarr Pydantic Project](#ome-zarr-pydantic-project)
  - [1. Installation](#1-installation)
  - [2. Run](#2-run)
    - [2.1. Command line](#21-command-line)
    - [2.2. Code](#22-code)
  - [3. Development](#3-development)
    - [3.1 Packaging](#31-packaging)

<!-- /TOC -->
## 1. Installation
Setting up a virtual environment with [Conda](https://docs.conda.io/en/latest/)

```bash
conda env create -f environment.yml
conda activate ome-zarr-pydantic
```

The conda environment comes with `pip` and `poetry` installed, we recommend `poetry`:

```bash
poetry install
```

## 2. Run
See section below to obtain example of zarr files

### 2.1. Command line
The reader expects the test zarr file to be in `resources/` 
```bash
run
```

### 2.2. Code
TODO: Change to a single zarr file

Make sure you initialized your conda environment (see above) the do the following python

```Python
    # Set data path
    folder_path: Path = Path("./relative/path/to/folder/containing/zarr/files/")
    # Load data
    model: Model = Model(folder_path)
```

## 3. Development
Small dataset provided by Fractal: [Zenodo Link](https://zenodo.org/records/8091756)

```
curl -O https://zenodo.org/records/8091756/files/20200812-CardiomyocyteDifferentiation14-Cycle1.zarr.zip
unzip 20200812-CardiomyocyteDifferentiation14-Cycle1.zarr.zip
```

### 3.1 Packaging
Create the conda package without default packages to ensure reproducibility by others:
```
conda env create -f environment.yml --no-default-packages
```