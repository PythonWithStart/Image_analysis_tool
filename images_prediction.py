
from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow.keras import datasets, layers, models


new_model = tf.keras.models.load_model('saved_model/my_model')

# 检查其架构
new_model.summary()