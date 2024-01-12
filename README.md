# plot_tree

This module allows the user to plot a phylogenetic tree on an existing matplotlib axis.

This means that:
* Phylogenies can be incorporated into existing plots.
* Annotations can be added using standard matplotlib functionality.
* Plots can be output in png, pdf, svg or tiff formats.
* Automatically generated and updated figures can include phylogenies

The module depends on the ETE Toolkit, an existing Python framework for analysing and visualising phylogenetic trees, plus the matplotlib visualisation library.


## Quick Start

To draw a phylogeny under the default settings onto a blank figure.

```
# Create an empty plot, 8in (width) by 10in (height) - matplotlib
f = plt.figure(figsize=(8, 10))

# Add an axis - matplotlib
ax = plt.subplot()

# Plot the tree on this axis, using the default settings - plot_tree
results = plot_tree.plot_tree("examples/primates.nw", ax)

# Save the tree - matplotlib
plt.savefig("mytree.png")
```

The output of this function is:
![Basic Tree](./examples/basic_plot.png "Basic Tree")

## Examples
*Reverse a tree on the y-axis

![Mirrored Tree](./examples/reversed.png "Mirrored Tree")


* 

## Parameters
* **`tree`** (`str`, Required)

	Either the path to a newick formatted tree or a string containing a newick formatted tree. 

* **`ax`** (`matplotlib.axes._axes.Axes`, Required)

	An open matplotlib ax object where the tree will be plotted. Required.

* **`x`** (`float`, Default 0)

	Desired position of the root node of the tree on the x axis, in axis units. 

* **`y`** (`float`, Default 0)

	Desired position of the bottom of the tree on the y axis, in axis units. Default 0.

* **`height`** (`float`, Default 10)

	Desired height of the tree, in axis units. Default 10.

* **`width`** (`float`, Default 10)

	Desired width of the tree, in axis units. Default 10.

* **`show_axis`** (`bool`, Default False)
 
	Show the axis lines and ticks on the output tree. 


* **`show_support`** (`bool`, Default False)
	Display branch support on the internal nodes of the tree. 


* **`align_tips`** (`bool`, Default False)

	If True, the tip labels will be horizontally aligned rather than positioned at the tips of the branches. By default, they are left-aligned for a standard tree and right-aligned for a mirrored tree (reverse=True)

* **`rev_align_tips`** (`bool`, Default False)

	If True the tip labels are right-aligned if reverse=False and left-aligned if reverse=True.

* **`branch_lengths`** (`bool`, Default True)

	If True, the branch lengths provided in the tree are used, otherwise all branches are fixed to the same length.

* **`scale_bar`** (`bool`, Default True)

	If True and branch_lengths is True, draw a scale bar.
 
* **`scale_bar_width`** (`float`, Default None)

	Width of scale bar in axis units. If not specified, the scale bar will be 1/4 of the width of the tree.

* **`reverse`** (`bool`, Default False)
	If True, mirror the tree on the y-axis, showing the root on the right-hand side.
    
* **`col_dict`** (`dict`, Default {})
	User provided dictionary with tip labels as keys and colours (in any [format accepted by matplotlib](https://matplotlib.org/stable/users/explain/colors/colors.html) as values. If this is not specified all labels will be black, if only some labels are specified all others will be black.

* **`label_dict`** (`dict`, Default {})

	User provided dictionary with current tip labels as keys and desired
tip labels as values. If this is not specified all labels will be as specified in the newick, if some labels are specified all others will match the newick.

* **`font_size`** (`int`, Default 10)
	Font size for tip labels. Branch support and scale bar labels will be two sizes smaller.
 
* **`line_col`** (`str` or `tuple`, Default 'black')
	Line colour, in any [format accepted by matplotlib](https://matplotlib.org/stable/users/explain/colors/colors.html).

* **`line_width`** (`float`, Default 2)
	Line width.


