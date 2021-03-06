# -*- coding: utf-8 -*-
"""Mnist Classifier Using Tensorflow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M0Xh1wX5mfqE9Y22VJoa6o61vhFs-OHY

This Code is to build a classifier for MNIST dataset in Tensorflow
"""

# import all packages on top 
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

"""one is on and rest are off , used for multiclass classification for one class output will be 1, and for others it be zero"""

# Read and create dataset 

mnist = input_data.read_data_sets('/tmp/data',one_hot=True)

# Define model variables 
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 10
batch_size = 100

# Place holder to store values while passing through graph 
# float value, Height of row is None and width will be 784
x = tf.placeholder('float',[None,784])
y = tf.placeholder('float')

# Method to define model 

def neural_network_model(data):

    # (input_data * weight)  + bias
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([784, n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}
    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}
    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                      'biases': tf.Variable(tf.random_normal([n_classes]))}

    #input_data * weight +b
    l1 = tf.add(tf.matmul(data,hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1,hidden_2_layer['weights']),hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2,hidden_3_layer['weights']),hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3,output_layer['weights'])+  output_layer['biases']

    return output

# Method to intialize model and train using mnist data and test model function 
def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = prediction,labels=y))

    # Adam optimizer does has learning rate parameter
    optimizer = tf.train.AdamOptimizer().minimize(cost)


    #cycles for feed forward and backprop error
    nm_epochs = 100

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(nm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x,epoch_y = mnist.train.next_batch(batch_size)
                _ ,c = sess.run([optimizer,cost], feed_dict= {x :epoch_x, y : epoch_y})
                epoch_loss += c
            print("Epoch", epoch,' completed out of ', nm_epochs , "Loss:" , epoch_loss)
        correct = tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))
        accuracy =  tf.reduce_mean(tf.cast(correct,'float'))
        print("Accuracuy" ,accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

# Calling method 
train_neural_network(x)