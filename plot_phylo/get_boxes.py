#!/usr/bin/env python3

def get_boxes(ax, texts):
    '''
    Converts a list of text objects to their co-ordinates on the axis in
    axis units.

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes,
        An open matplotlib ax object where the tree will be plotted.
    texts : list
        A list of matplotlib.pyplot.text objects representing the tip
        labels from the tree and their metadata.

    Returns
    -------
    boxpos : dict
        A dictionary of dictionaries where the top level keys are the tip
        labels. Within each subdictionary the key value pairs are
        index (position in the tree starting from the top) and the minimum,
        maximum and central position of the text box on the x and y axis,
        as index, xmin, xmid, xmax and ymin, ymid and ymax.

    '''
    boxpos = dict()
    # Iterate through the tip labels
    for i, txt in enumerate(texts):
        # Get the position of the boxes containing the labels, convert to axis
        # units
        box = ax.transData.inverted().transform(txt.get_window_extent(
            ax.figure.canvas.get_renderer()))
        nam = txt.get_text().strip()
        # Build the dictionary
        boxpos[nam] = dict()
        boxpos[nam]['index'] = i
        boxpos[nam]['xmin'] = box[0][0].round(3)
        boxpos[nam]['xmax'] = box[1][0].round(3)
        boxpos[nam]['ymin'] = box[0][1].round(3)
        boxpos[nam]['ymax'] = box[1][1].round(3)
        boxpos[nam]['ymid'] = (box[0][1] + ((
            box[1][1] - box[0][1]) / 2)).round(3)
        boxpos[nam]['xmid'] = (
            box[0][0] + ((box[1][0] - box[0][1]) / 2)).round(3)

    return (boxpos)
