# TdaToolbox 

![LOGO](./figures/header.jpg)

## Introduction

Topological Data Analysis, also abbreviated *TDA*, is a recent field that emerged from various works in applied topology and computational geometry. It aims at providing well-founded mathematical, statistical and algorithmic methods to exploit the topological and underlying geometric structures in data. My aim is to develop some tools in this repository, that may be applied to data science in general. Some of them already proved useful for classification tasks.

Read more about applied TDA:
- [Medium article with general TDA overview](https://towardsdatascience.com/from-tda-to-dl-d06f234f51d)
- [Medium article about TDA for clustering](https://towardsdatascience.com/tda-to-rule-them-all-tomato-clustering-878e03394a1)
- [Paper on applied TDA for arrhythmia detection](https://hal.inria.fr/hal-02155849/file/1906.05795.pdf)

## Tutorial Clustering - 3DShape

This _notebook_ gives a simple example of how to handle three-dimensional shapes. The whole example is based on the height as filtration function, so not invariant in space. However, it gives a pretty good idea of what the output of a topological analysis may give.

## Tutorial Clustering - ToMaTo

This _notebook_ rather focus on a specific strength of TDA: its robustness to detect centroids in dataset, along with its ability to record the relationships between each point, enabling us to retrace the whole structure of the centroids. Examples are provided in the notebook.

## Tutorial TimeSeries - Evolutions

This _section_ is still in construction.