# Detailed Example
This detailed example shows how `plot_phylo` can be combined with matplotlib and basic Python to draw complex plots.

```
# Build the blank figure
f = plt.figure(figsize=(15, 10))
ax = plt.subplot(1, 1, 1)

# Set the x and y axis limits
ax.set_xlim(2, 122)
ax.set_ylim(9, 21)
ypos_val = 10

# Define colours for specific nodes
colours = {'Gorilla gorilla': '#e21c0c', 'Pan troglodytes': '#0c57e2', 'Saimiri boliviensis': '#338c3e',
           'Chiropotes satanas': '#dc9d0c'}

# Draw the left tree
results_left = plot_phylo.plot_phylo("primates.nw",
                                      ax, xpos=5, ypos=ypos_val, width=15,
                                      show_axis=False, show_support=False,
                                      font_size=16, col_dict=colours,
                                      rev_align_tips=True)

# Draw the right tree
results_right = plot_phylo.plot_phylo("primates_mixed.nw",
                                       ax, xpos=105, ypos=10, width=15,
                                       show_axis=False, show_support=False,
                                       reverse=True,
                                       font_size=16, col_dict=colours,
                                       rev_align_tips=True)

# Using matplotlib and basic Python functionality on the returned dictionaries from hereforward

# Connection between trees

# Find the labels which differ between trees
links = []
for r1 in results_left:
    # Find the index of each label in the tree
    ind1 = results_left[r1]['index']
    ind2 = results_right[r1]['index']
    
    # If they differ, store them
    if ind1 != ind2:
        links.append(r1)

for link in links:
    # Retrieve the positions of the non-matched labels
    left_box = results_left[link]
    right_box = results_right[link]
    
    # Get the position of the labels in each tree
    left_x = left_box['xmax'] + 1
    left_y = left_box['ymid']
    
    right_x = right_box['xmin'] - 1
    right_y = right_box['ymid']

    # Plot the points on the left tree
    ax.scatter(left_x, left_y, color=colours[link])
    
    # Plot the points on the right tree
    ax.scatter(right_x, right_y, color=colours[link])
    
    # Connect the two points
    ax.plot([left_x, right_x], [left_y, right_y], color=colours[link])

# Box highlighting great apes
# Define which species are great apes
great_apes = ['Gorilla gorilla', 'Pan troglodytes', 'Homo sapiens', 'Pongo abelii']
ga_pos = []

# Store the positions of the great ape labels
for nam, box in results_left.items():
    if nam in great_apes:
        ga_pos.append(box['ymin'])
        ga_pos.append(box['ymax'])

# Draw the grey box. 15.5 is based on visually inspecting the axis.
ax.fill_between([15.5, box['xmax']], min(ga_pos), max(ga_pos), color='lightgrey')

# Additional labels
# Add the Tree 1 and Tree 2 labels, using figure co-ordinates
f.text(0.2, 0.85, 'Tree 1', ha='center', fontsize=16, fontweight='bold')
f.text(0.8, 0.85, 'Tree 2', ha='center', fontsize=16, fontweight='bold')

# Add the overall title
f.suptitle("Primate Phylogeny", fontsize=24, y=0.92)

# Save
f.savefig("examples/layered.png", bbox_inches='tight')
```

![Detailed Example](./examples/layered.png "Detailed Example")
