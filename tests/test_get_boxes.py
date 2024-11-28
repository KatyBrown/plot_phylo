import pytest
from plot_phylo import get_boxes
from test_get_boxes_data import (test_get_boxes_axes,
                                 test_get_boxes_texts,
                                 test_get_boxes_results)


@pytest.mark.parametrize("ax, texts, expected_result",
                         list(zip(test_get_boxes_axes,
                                  test_get_boxes_texts,
                                  test_get_boxes_results)))
def test_get_boxes(ax, texts, expected_result):
    boxes = get_boxes.get_boxes(ax, texts)
    bclean = dict()
    for b, vals in boxes.items():
        bclean[b] = dict()
        for v in vals:
            bclean[b][v] = round(vals[v], 0)
    assert bclean == expected_result
