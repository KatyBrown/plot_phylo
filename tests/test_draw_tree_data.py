import helper_functions


tests_draw_tree = [{},
                   {'xpos': 1, 'ypos': 1},
                   {'dims_height': 6},
                   {'dims_width': 3},
                   {'dims_depth': [2, 2, 2]},
                   {'structure_reverse': True},
                   {'structure_rev_align_tips': True},
                   {'structure_branch_lengths': False},
                   {'structure_reverse': True},
                   {'appearance_col_dict': {'Homo sapiens': 'blue'}},
                   {'appearance_label_dict': {'Homo sapiens': 'human'}},
                   {'appearance_font_size': 20},
                   {'appearance_line_col': 'orange'},
                   {'appearance_line_width': 5},
                   {'appearance_show_support': True},
                   {'appearance_bold': ['Homo sapiens']}]


test_draw_tree_list = []
test_draw_tree_nams = []
for test in tests_draw_tree:
    testnam = "draw_tree_%s" % "_".join(test.keys())
    curr_dict, varis_draw_tree = helper_functions.get_draw_tree_metadata()
    for key, val in test.items():
        if key.startswith("dims") or key.startswith(
                "structure") or key.startswith("appearance"):
            dnam, knam = key.split("_")[0], "_".join(key.split("_")[1:])
            curr_dict[dnam][knam] = val
        else:
            curr_dict[key] = val

    pass_vals = [curr_dict[v] for v in varis_draw_tree]
    pass_vals.append('tests/test_objects/%s.pickle' % testnam)
    pass_vals.append(testnam)
    test_draw_tree_list.append(pass_vals)
    test_draw_tree_nams.append(testnam)

test_draw_tree_vars = ",".join(varis_draw_tree + ['expected', 'ID'])
