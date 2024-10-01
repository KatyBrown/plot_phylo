![Tests Passing](https://github.com/KatyBrown/plot_phylo/actions/workflows/main.yml/badge.svg)<br>
[![Documentation Status](https://readthedocs.org/projects/plot-phylo/badge/?version=latest)](https://plot-phylo.readthedocs.io/en/latest/?badge=latest)<br>
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)<br>
![Python Versions](https://img.shields.io/pypi/pyversions/plot-phylo)<br>
![PyPI - Version](https://img.shields.io/pypi/v/plot-phylo)

# plot_phylo

![Illustration](./examples/layered.png "Illustration")

This module allows the user to plot a phylogenetic tree on an existing matplotlib axis.

This means that:
* Phylogenies can be incorporated into existing plots.
* Annotations can be added using standard matplotlib functionality.
* Plots can be output in png, pdf, svg or tiff formats.
* Automatically generated and updated figures can include phylogenies

Full documentation is available via [ReadTheDocs](https://plot-phylo.readthedocs.io/en/latest/index.html).

The module depends on the [ETE Toolkit](http://etetoolkit.org/), an excellent existing Python framework for analysing and visualising phylogenetic trees, plus the [matplotlib](https://matplotlib.org/) visualisation library. It is designed to make generating complex figures incorporating phylogenies easier, as matplotlib plotting functions can be used on top of the basic tree.


# Installation

**Requirements**

* python >= 3.6
* matplotlib >= 2.1.1
* ete3 >= 3.1.0

The module can be installed using pip

`pip install plot_phylo`

You can also download the latest release [here](https://github.com/KatyBrown/plot_phylo/releases/latest)

Or clone the GitHub repository directly.

`git clone git@github.com:KatyBrown/plot_phylo.git`

# Cite
If you use this repository in your work, please cite:
Brown, K (2024) plot_phylo. https://github.com/KatyBrown/plot_phylo