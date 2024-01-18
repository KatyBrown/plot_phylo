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
      'xmax': 0.068,
      'ymin': 0.992,
      'ymax': 1.03,
      'ymid': 1.011,
      'xmid': -0.462},
     'goodbye': {'index': 1,
      'xmin': 2.0,
      'xmax': 2.122,
      'ymin': 2.992,
      'ymax': 3.03,
      'ymid': 3.011,
      'xmid': 1.565},
     'outside text': {'index': 2,
      'xmin': 10.0,
      'xmax': 10.167,
      'ymin': 19.992,
      'ymax': 20.03,
      'ymid': 20.011,
      'xmid': 5.088}}

b2 = {'text1': {'index': 0,
      'xmin': 0.0,
      'xmax': 16.134,
      'ymin': 89.188,
      'ymax': 92.976,
      'ymid': 91.082,
      'xmid': -36.527},
     'text2': {'index': 1,
      'xmin': 20.0,
      'xmax': 36.134,
      'ymin': 29.188,
      'ymax': 32.976,
      'ymid': 31.082,
      'xmid': 23.473},
     'text3': {'index': 2,
      'xmin': 10.0,
      'xmax': 26.134,
      'ymin': 19.188,
      'ymax': 22.976,
      'ymid': 21.082,
      'xmid': 13.473}}

b3 = {'text1': {'index': 0,
      'xmin': 0.0,
      'xmax': 32.157,
      'ymin': 88.377,
      'ymax': 95.952,
      'ymid': 92.165,
      'xmid': -28.11},
     '': {'index': 1,
      'xmin': 20.0,
      'xmax': 20.0,
      'ymin': 30.0,
      'ymax': 30.0,
      'ymid': 30.0,
      'xmid': 15.0},
     '~*~': {'index': 2,
      'xmin': 10.0,
      'xmax': 12.717,
      'ymin': 19.729,
      'ymax': 20.812,
      'ymid': 20.271,
      'xmid': 6.494}}

test_get_boxes_results = [b1, b2, b3]