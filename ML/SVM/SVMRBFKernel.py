# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 22:15:46 2016

@author: omar
"""

import numpy as np
import quadprog

def transform(point):
    return [ (point[1]**2) - (2*point[0]) - 1, (point[0]**2)-(2*point[1]) + 1]

def signal(point, weights):
	"""
	Gives the signals given the points matrix (N, d+1) and the weights vector (1, d+1)
	"""
    return np.dot(point, weights)
def predict(point, weights):
	"""
	Classifies depending on the points matrix and the weights vector
	"""
    return np.sign(signal(point, weights))

def compute_error(attempted_classes, correct_classes):
	"""
	Computes error based on correct classifications and attempted classifications
	"""
    error = 0
    for i in range(len(attempted_classes)):
        if attempted_classes[i] != correct_classes[i]:
            error += 1
    return error/len(attempted_classes)





def svm_rbf_kernel(X, Y, gamma = 1):
    """
	This function implements the a RBF kernel that will be used later to implement the SVM algorithm.
	It utilizes a quadratic programming package to find the value of the kernel function (RBF Kernel).

	According to documentation this package solves:
	Minimize 1/2 x^T G x - a^T x
	Subject to C.T x >= b

	We tweak this formulation to solve the dual problem. We find the alphas vector and return them
    """
    N = len(Y)
    G = np.array([[Y[i]*Y[j]*np.exp( -1 * gamma * (np.linalg.norm(X[i] - X[j])**2) ) for j in range(N)] for i in range(N)], dtype='d')+(np.eye(N)*(1*np.e**-14))

    a = np.ones(N)
    C = np.concatenate( ([Y], np.identity(N)), axis=0).T

    b = np.zeros(N+1)
    return quadprog.solve_qp(G=G, a=a, C=C, b=b, meq=1)

def svm_rbf_bias(points, labels, alphas, gamma = 1):
    """
    Computes the bias term
    """
    N, d = points.shape

    b = 0
    m = None
    for alpha_index in range(len(alphas)):
        if alphas[alpha_index] > 0:
            if m == None:
                m = alpha_index
            n = alpha_index
            b += labels[n]*alphas[n]*np.exp( -1 * gamma * (np.linalg.norm(points[n] - points[m])**2) )
    b = labels[m] - b
    return b
def predict_svm_rbf(points, labels, alphas, test_point, gamma = 1):
    """
    Predicts the class using an RBF kernel
    """
    signal = 0
    b = svm_rbf_bias(points, labels, alphas, gamma = 1)
    for alpha_index in range(len(alphas)):
        if alphas[alpha_index] > 0:
            n = alpha_index
            signal += labels[n]*alphas[n]*np.exp( -1 * gamma * (np.linalg.norm(points[n] - test_point)**2) )
    return np.sign(signal +b)
