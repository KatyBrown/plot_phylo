import helper_functions


tests_rev_align = [{},
                   {'xpos': 1, 'ypos': 1},
                   {'dims_height': 6},
                   {'dims_width': 3},
                   {'dims_depth': [2, 2, 2]},
                   {'structure_rev_align_tips': True},
                   {'structure_branch_lengths': False},
                   {'appearance_col_dict': {'Homo sapiens': 'blue'}},
                   {'appearance_label_dict': {'Homo sapiens': 'human'}},
                   {'appearance_font_size': 20},
                   {'appearance_line_col': 'orange'},
                   {'appearance_line_width': 5},
                   {'appearance_show_support': True},
                   {'appearance_bold': ['Homo sapiens']}]


test_rev_align_list = []
test_rev_align_nams = []
for test in tests_rev_align:
    testnam = "amend_tree_%s" % "_".join(test.keys())
    curr_dict, varis_rev_align = helper_functions.get_draw_tree_metadata()
    curr_dict['structure']['rev_align_tips'] = True
    curr_dict['structure']['reverse'] = True
    for key, val in test.items():
        if key.startswith("dims") or key.startswith(
                "structure") or key.startswith("appearance"):
            dnam, knam = key.split("_")[0], "_".join(key.split("_")[1:])
            curr_dict[dnam][knam] = val
        else:
            curr_dict[key] = val

    pass_vals = [curr_dict[v] for v in varis_rev_align]
    pass_vals.append('tests/test_objects/%s.pickle' % testnam)
    pass_vals.append(testnam)
    test_rev_align_list.append(pass_vals)
    test_rev_align_nams.append(testnam)

test_rev_align_vars = ",".join(varis_rev_align + ['expected', 'ID'])
