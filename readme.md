# TdaToolbox 

`Author: Meryll Dindin`

![LOGO](./figures/header.jpg)

## Introduction

Topological Data Analysis, also abbreviated *TDA*, is a recent field that emerged from various works in applied topology and computational geometry. It aims at providing well-founded mathematical, statistical and algorithmic methods to exploit the topological and underlying geometric structures in data. My aim is to develop some tools in this repository, that may be applied to data science in general. Some of them already proved useful for classification tasks.

Read more about applied TDA:
- [Medium article with general TDA overview](https://towardsdatascience.com/from-tda-to-dl-d06f234f51d)
- [Medium article about TDA for clustering](https://towardsdatascience.com/tda-to-rule-them-all-tomato-clustering-878e03394a1)
- [Paper on applied TDA for arrhythmia detection](https://hal.inria.fr/hal-02155849/file/1906.05795.pdf)

## Package Installation

This is **a** way to install the project. Nonetheless, it depends on your OS and your good habits. I currently work on _Ubuntu 18.04_ and like to separate each of my project in their relative virtual environment.

* Install your distribution of [MiniConda](https://docs.conda.io/en/latest/miniconda.html).
* Install the [GUDHI](https://anaconda.org/conda-forge/gudhi) python package.
* Clone the GitHub repository.
* Install recursively all the python packages used by the project.

```bash
bash Miniconda3-latest-Linux-x86_64.sh -p /home/meryll/CondaEnvs
cd /home/meryll/CondaEnvs
source bin/activate
conda install -c conda-forge gudhi
git clone https://www.github.com/Coricos/TdaToolbox
cd TdaToolbox
pip install -r requirements.txt
```

### Specific to Jupyter Notebooks Users

If like me, each of your project is separated into their respective environment, then you will have to define relative kernels.

```bash
pip install jupyter notebook ipython ipykernel
python -m ipykernel install --user --name=tdatoolbox
```

For others purposes, those command lines may turn out to be useful:

```bash
# Display the list of all installed kernels
jupyter kernelspec list
# Remove a specific kernel of ipython
jupyter kernelspec uninstall tdatoolbox
```

## Tutorial Clustering - 3DShape

This _notebook_ gives a simple example of how to handle three-dimensional shapes. The whole example is based on the height as filtration function, so not invariant in space. However, it gives a pretty good idea of what the output of a topological analysis may give.

## Tutorial Clustering - ToMaTo

This _notebook_ rather focus on a specific strength of TDA: its robustness to detect centroids in dataset, along with its ability to record the relationships between each point, enabling us to retrace the whole structure of the centroids. Examples are provided in the notebook.

## Tutorial TimeSeries - Evolutions

This _section_ is still in construction.