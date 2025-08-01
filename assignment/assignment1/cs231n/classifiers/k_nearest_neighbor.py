from builtins import range
from builtins import object
import numpy as np
from past.builtins import xrange


class KNearestNeighbor(object):
    """ a kNN classifier with L2 distance """

    def __init__(self):
        pass

    def train(self, X, y):
        """
        Train the classifier. For k-nearest neighbors this is just
        memorizing the training data.

        Inputs:
        - X: A numpy array of shape (num_train, D) containing the training data
          consisting of num_train samples each of dimension D.
        - y: A numpy array of shape (N,) containing the training labels, where
             y[i] is the label for X[i].
        """
        self.X_train = X
        self.y_train = y

    def predict(self, X, k=1, num_loops=0):
        """
        Predict labels for test data using this classifier.

        Inputs:
        - X: A numpy array of shape (num_test, D) containing test data consisting
             of num_test samples each of dimension D.
        - k: The number of nearest neighbors that vote for the predicted labels.
        - num_loops: Determines which implementation to use to compute distances
          between training points and testing points.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
          test data, where y[i] is the predicted label for the test point X[i].
        """
        if num_loops == 0:
            dists = self.compute_distances_no_loops(X)
        elif num_loops == 1:
            dists = self.compute_distances_one_loop(X)
        elif num_loops == 2:
            dists = self.compute_distances_two_loops(X)
        else:
            raise ValueError("Invalid value %d for num_loops" % num_loops)

        return self.predict_labels(dists, k=k)

    def compute_distances_two_loops(self, X):
        """
        Compute the distance between each test point in X and each training point
        in self.X_train using a nested loop over both the training data and the
        test data.

        Inputs:
        - X: A numpy array of shape (num_test, D) containing test data.

        Returns:
        - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
          is the Euclidean distance between the ith test point and the jth training
          point.
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            for j in range(num_train):
                #####################################################################
                # TODO:                                      #
                # Compute the l2 distance between the ith test point and the jth    #
                # training point, and store the result in dists[i, j]. You should   #
                # not use a loop over dimension, nor use np.linalg.norm().
                # 计算第i个测试点与第j个训练点之间的 l2 距离 #
                # 并将结果存储在dists[i,j]中 #
                # 不要使用维度循环，也不要使用np.linalg.norm() #
                #####################################################################
                diff = X[i] - self.X_train[j]
                dists[i, j] = np.sqrt(np.sum(diff ** 2))
                # pass
        return dists

    def compute_distances_one_loop(self, X):
        """
        Compute the distance between each test point in X and each training point
        in self.X_train using a single loop over the test data.

        Input / Output: Same as compute_distances_two_loops
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            #######################################################################
            # TODO:                                      #
            # Compute the l2 distance between the ith test point and all training #
            # points, and store the result in dists[i, :].               #
            # Do not use np.linalg.norm().                         #
            #######################################################################
            dists[i, :] = np.sqrt(np.sum((self.X_train - X[i]) ** 2, axis=1))
            # pass
        return dists

    def compute_distances_no_loops(self, X):
        """
        Compute the distance between each test point in X and each training point
        in self.X_train using no explicit loops.

        Input / Output: Same as compute_distances_two_loops
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        #########################################################################
        # TODO:                                          #
        # Compute the l2 distance between all test points and all training      #
        # points without using any explicit loops, and store the result in      #
        # dists.                                         #
        #                                            #
        # You should implement this function using only basic array operations; #
        # in particular you should not use functions from scipy,                #
        # nor use np.linalg.norm().                              #
        #                                            #
        # HINT: Try to formulate the l2 distance using matrix multiplication    #
        #       and two broadcast sums.                         #
        #########################################################################
        X_square = np.sum(X ** 2, axis=1) # (num_test,)
        X_train_square = np.sum(self.X_train ** 2, axis=1) # (num_train,)
        cross_term = X.dot(self.X_train.T) # (num_test, num_train)
        # 广播展开，加后是 (num_test, num_train)
        dists = np.sqrt(X_square[:, np.newaxis] + X_train_square[np.newaxis, :] - 2 * cross_term)
        return dists

    def predict_labels(self, dists, k=1):
        """
        Given a matrix of distances between test points and training points,
        predict a label for each test point.

        Inputs:
        - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
          gives the distance betwen the ith test point and the jth training point.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
          test data, where y[i] is the predicted label for the test point X[i].
        """
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test)
        for i in range(num_test):
            # A list of length k storing the labels of the k nearest neighbors to
            # the ith test point.
            # 长度为k的列表，存储第i个测试点的k个近邻的标签。
            closest_y = []
            #########################################################################
            # TODO:                                        #
            # Use the distance matrix to find the k nearest neighbors of the ith    #
            # testing point, and use self.y_train to find the labels of these       #
            # neighbors. Store these labels in closest_y.                   #
            # Hint: Look up the function numpy.argsort.
            # 使用距离矩阵找出第 i 个测试点的 k 个近邻，并使用 self.y_train 找出这些测试点的标签。#
            # 测试点，并使用 self.y_train 查找这些                          #
            # 邻居的标签。将这些标签存储在 closest_y 中。                      #
            # 提示：查找函数 numpy.argsort。                             #
            #########################################################################
            
            closest_y = self.y_train[np.argsort(dists[i])[:k]]

            #########################################################################
            # TODO:                                        #
            # Now that you have found the labels of the k nearest neighbors, you    #
            # need to find the most common label in the list closest_y of labels.   #
            # Store this label in y_pred[i]. Break ties by choosing the smaller     #
            # label.                                       #
            # 现在，您已经找到了k个最近邻的标签，您需要在标签列表 closest_y 中找到最常见的标签。#
            # 需要找到标签列表 closest_y 中最常见的标签。                   #
            # 将此标签存储在 y_pred[i]中。通过选择较小的标签。                  #
            #########################################################################
            y_pred[i] = np.bincount(closest_y).argmax()

        return y_pred
