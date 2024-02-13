#!/usr/bin/env python3
import matplotlib.pyplot as plt

f1 = plt.figure()
a1 = f1.add_subplot(1, 1, 1)

f2 = plt.figure()
a2 = f2.add_subplot(1, 2, 1)
a2.set_xlim(0, 100)
a2.set_ylim(0, 100)

f3 = plt.figure()
a3 = f3.add_subplot(1, 2, 1)
a3.set_xlim(0, 100)
a3.set_ylim(0, 100)

test_get_boxes_axes = [a1, a2, a3]

text11 = a1.text(0, 1, "hello")
text12 = a1.text(2, 3, "goodbye")
text13 = a1.text(10, 20, "outside text")

text21 = a2.text(0, 90, "text1")
text22 = a2.text(20, 30, "text2")
text23 = a2.text(10, 20, "text3")

text31 = a3.text(0, 90, "text1", fontsize=20)
text32 = a3.text(20, 30, "", fontsize=10)
text33 = a3.text(10, 20, "~*~", fontsize=2)

test_get_boxes_texts = [[text11, text12, text13],
                        [text21, text22, text23],
                        [text31, text32, text33]]

b1 = {'hello': {'index': 0,
                'xmin': 0.0,
                'xmax': 0.0,
                'ymin': 1.0,
                'ymax': 1.0,
                'ymid': 1.0,
                'xmid': -0.0},
      'goodbye': {'index': 1,
                  'xmin': 2.0,
                  'xmax': 2.0,
                  'ymin': 3.0,
                  'ymax': 3.0,
                  'ymid': 3.0,
                  'xmid': 2.0},
      'outside text': {'index': 2,
                       'xmin': 10.0,
                       'xmax': 10.0, 
                       'ymin': 20.0,
                       'ymax': 20.0,
                       'ymid': 20.0,
                       'xmid': 5.0}}

b2 = {'text1': {'index': 0,
                'xmin': 0.0,
                'xmax': 16.0,
                'ymin': 89.0,
                'ymax': 93.0, 
                'ymid': 91.0,
                'xmid': -37.0},
      'text2': {'index': 1,
                'xmin': 20.0,
                'xmax': 36.0,
                'ymin': 29.0,
                'ymax': 33.0,
                'ymid': 31.0,
                'xmid': 23.0},
      'text3': {'index': 2,
                'xmin': 10.0,
                'xmax': 26.0,
                'ymin': 19.0,
                'ymax': 23.0,
                'ymid': 21.0,
                'xmid': 13.0}}


b3 = {'text1': {'index': 0,
                'xmin': 0.0,
                'xmax': 32.0,
                'ymin': 88.0,
                'ymax': 96.0,
                'ymid': 92.0,
                'xmid': -28.0},
      '': {'index': 1,
           'xmin': 20.0,
           'xmax': 20.0,
           'ymin': 30.0,
           'ymax': 30.0,
           'ymid': 30.0,
           'xmid': 15.0},
      '~*~': {'index': 2,
              'xmin': 10.0,
              'xmax': 13.0,
              'ymin': 20.0,
              'ymax': 21.0,
              'ymid': 20.0,
              'xmid': 6.0}}

test_get_boxes_results = [b1, b2, b3]