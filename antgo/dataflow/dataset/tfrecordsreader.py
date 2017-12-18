# -*- coding: UTF-8 -*-
# Time: 12/2/17
# File: tfdataset.py
# Author: jian<jian@mltalker.com>
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from antgo.dataflow.dataset import Dataset
import tensorflow as tf
slim = tf.contrib.slim
import os
import sys


class TFRecordsReader(Dataset):
  def __init__(self, train_or_test, dir=None, params=None):
    super(TFRecordsReader, self).__init__(train_or_test, dir, params)
    self._data_size = None
    self._data_type = tf.uint8
    self._label_size = None
    self._label_type = tf.uint8
    self._num_samples = getattr(self, '_num_samples', 199600)
    self._pattern = getattr(self, '_pattern', '*.tfrecords')
  
  @property
  def capacity(self):
    return self._capacity
  @capacity.setter
  def capacity(self, val):
    self._capacity = val
  
  @property
  def min_after_dequeue(self):
    return self._min_after_dequeue
  @min_after_dequeue.setter
  def min_after_dequeue(self, val):
    self._min_after_dequeue = val
  
  @property
  def data_size(self):
    return self._data_size
  @data_size.setter
  def data_size(self, val):
    self._data_size = val
  
  @property
  def label_size(self):
    return self._label_size
  @label_size.setter
  def label_size(self, val):
    self._label_size = val
  
  @property
  def data_type(self):
    return self._data_type
  @data_type.setter
  def data_type(self, val):
    self._data_type = val
  
  @property
  def label_type(self):
    return self._label_type
  @label_type.setter
  def label_type(self, val):
    self._label_type = val
  
  @property
  def num_samples(self):
    return self._num_samples
  @num_samples.setter
  def num_samples(self, val):
    self._num_samples = val
  
  @property
  def file_pattern(self):
    return self._pattern
  @file_pattern.setter
  def file_pattern(self,val):
    self._pattern = val

  def data_pool(self):
    raise NotImplementedError
  
  def at(self, id):
    raise NotImplementedError

  def split(self, split_params={}, split_method=""):
    raise NotImplementedError
  
  @property
  def size(self):
    return self.num_samples
    
  def model_fn(self, *args, **kwargs):
    # 1.step candidate data file list
    file_names = tf.train.match_filenames_once(os.path.join(self.dir, self.train_or_test, self.file_pattern))
    
    # 2.step shuffle data file list
    filename_queue = tf.train.string_input_producer(file_names)
    
    # 3.step read from data file
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    
    # 4.step parse data
    features = tf.parse_single_example(serialized_example,
                                       features={
                                          'image': tf.FixedLenFeature([], tf.string),
                                          'label': tf.FixedLenFeature([], tf.string),
                                       })
    
    image = tf.decode_raw(features['image'], self.data_type)
    if self.data_size is not None:
      image = tf.reshape(image, self.data_size)

    label = tf.decode_raw(features['label'], self.label_type)
    if self.label_size is not None:
      label = tf.reshape(label, self.label_size)
    
    return image, label