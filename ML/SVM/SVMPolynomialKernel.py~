# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 23:12:56 2016

@author: omar
"""

import numpy as np
import quadprog


def transform(point):
	"""
	This is a helper function in which you can specify any transformation
	"""
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

def svm_poly_kernel(X, Y, C=1, degree=2):
	"""
	This function implements the a polynomial kernel that will be used later to implement the SVM algorithm.
	It utilizes a quadratic programming package to find the value of the kernel function.

	According to documentation this package solves:
	Minimize 1/2 x^T G x - a^T x
	Subject to C.T x >= b

	We tweak this formulation to solve the dual problem. We find the alphas vector and return them
	"""
    N = len(Y)
    G = np.array([[Y[i]*Y[j]*((C + np.dot(X[i], X[j]))**degree) for j in range(N)] for i in range(N)], dtype='d')+(np.eye(N)*(1*np.e**-30))

    a = np.ones(N)
    C = np.concatenate( ([Y], np.identity(N)), axis=0).T

    b = np.zeros(N+1)
    return quadprog.solve_qp(G=G, a=a, C=C, b=b, meq=1)

def svm_poly_bias(X, Y, alphas, C=1, degree=2):
	"""
	Solves the bias term of the minimization function
	"""
    N, d = X.shape

    b = 0
    for alpha_index in range(N):
        if alphas[alpha_index] > 0:
            m = alpha_index
            break

    for alpha_index in range(N):
        if alphas[alpha_index] > 0:
            n = alpha_index
            b += Y[n]*alphas[n]*(C + np.dot(X[n], X[m]))**degree
    b = Y[m] - b
    return b
def predict_svm_poly(X, labels, alphas, test_points, C=1, degree=2):
	"""
	Predicts the classification using the SVM algorithm (hard-margin) with polynomial kernel
	"""
    N,d = X.shape
    predictions = []

    b = svm_poly_bias(X, labels, alphas, C, degree)

    positive_alphas = []
    for alpha_index in range(N):
        if alphas[alpha_index] > 0:
            positive_alphas.append(alpha_index)


    for test_point in test_points:
        signal = 0
        for n in positive_alphas:
            signal += (labels[n]*alphas[n]*(C + np.dot(X[n], test_point))**degree )
        predictions.append(np.sign(signal+b))
    return predictions

points = np.array([[1, 0], [ 0, 1], [0, -1],  [-1, 0], [0, 2], [0, -2], [-2, 0]])
labels = np.array( [-1]*3+[1]*4, dtype='d')

alphas = svm_poly_kernel(points, labels, C=1, degree=2)[0]
print(alphas)

predictions = predict_svm_poly(points, labels, alphas, points, C=1, degree=2)
print(predictions)
