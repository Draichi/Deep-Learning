import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot = True)

n_classes = 10
batch_size = 128

x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')
def maxpool2d(x): #          size of window    movement of window
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

def convolutional_neural_network(x):
    # 5 by 5 convolutional, gonna take 1 input, gonna produce 32 features/outputs
    weights = {'W_conv1':tf.Variable(tf.random_normal([5,5,1,32])),
               'W_conv2':tf.Variable(tf.random_normal([5,5,32,64])),
               'W_fc':tf.Variable(tf.random_normal([7*7*64,1024])), # fully connected layer
               'out':tf.Variable(tf.random_normal([1024, n_classes]))}

    biases = {'b_conv1':tf.Variable(tf.random_normal([32])),
               'b_conv2':tf.Variable(tf.random_normal([64])),
               'b_fc':tf.Variable(tf.random_normal([1024])), # fully connected layer
               'out':tf.Variable(tf.random_normal([n_classes]))}
    # reshaping a 784 pixels image to a 28x28 image
    x = tf.reshape(x, shape=[-1,28,28,1])

    conv1 = tf.nn.relu(conv2d(x, weights['W_conv1']))
    conv1 = maxpool2d(conv1)
    conv2 = tf.nn.relu(conv2d(conv1, weights['W_conv2']))
    conv2 = maxpool2d(conv2)

    # fully connected
    fc = tf.reshape(conv2, [-1, 7*7*64])
    fc = tf.nn.relu(tf.matmul(fc, weights['W_fc'])+biases['b_fc'])

    output = tf.matmul(fc, weights['out'])+biases['out']

    return output

def train_neural_network(x):
    prediction = convolutional_neural_network(x)
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    hm_epochs = 10
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss)

        correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy_sum = tf.reduce_sum(tf.cast(correct_prediction, 'float'))
        good = 0
        total = 0
        for i in range(int(mnist.test.num_examples/batch_size)):
            testSet = mnist.test.next_batch(batch_size)
            good += accuracy_sum.eval(feed_dict={x:testSet[0], y:testSet[1], keep_prob:1.0})
            total += testSet[0].shape[0]
        print('Test Accuracy %g' %(good/total))

train_neural_network(x)
