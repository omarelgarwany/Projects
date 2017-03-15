# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 13:17:24 2016

@author: omar
"""
import matplotlib.pyplot as plt
import LinearGenerator as lngn
import numpy as np
N = 10
runs = 1000
linear_regression=False
class PLA:
    """
    This perceptron classifier implements a pocket version of the PLA. This means that even if the sample points are not
    linearly separable it returns the weights that classify the points with the least error.
    It also has the ability to reduce the number of attempts by starting with weights generated from linear regression
    instead of starting from a 0 matrix of weights (This ).
    """
    def linear_regression_initial_weights(self, points, correct_classifications):
        points = np.array(points)
        correct_classifications = np.array([correct_classifications])
        points_pinv =  np.linalg.pinv(points)
        weights = np.matrix.dot(correct_classifications, points_pinv)
        return weights[0]
    def pla(self, points, correct_classifications, max_attempts = 5000, linear_regression = False):
        #Variables that we keep track of during the learning process
        errors = float("inf")
        min_errors = float("inf")
        best_attempt = None
        attempts = 0
        #We initialize the weights as a vector of size d+1 (we may choose to initialize the to 0 or have initial weights by linear regression)
        if linear_regression:
            attempted_weights = self.linear_regression_initial_weights(points, correct_classifications)            
        else:
            attempted_weights = [0 for i in range(len(points))]
        
        #We only stop when there are no misclassified point
        while errors > 0: 
            
            attempts += 1
            errors = 0
            wrong_point_indices = []
            #We obtain the classification with the current learned weights..
            attempted_classifications = lngn.classify_points(points, attempted_weights)
            
            #Here we check if there are any miscalssified points and keep track of them..            
            for j in range(len(correct_classifications)):
                if correct_classifications[j] != attempted_classifications[j]:
                    wrong_point_indices.append( j )
                    errors += 1
            #We put the best obtained weight vector in our "pocket" by keeping track of the weights which produced the least error
            if errors < min_errors:
                min_errors = errors
                best_attempt = attempted_weights
            #If there are no misclassified points or we have exceeded a specified limit for attempts, our experiment is over and we record the weights..
            #Note that it is easier to reach this point as N gets smaller
            if min_errors == 0 or attempts > max_attempts:
                break
	    #If not, we update our weights by choosing any misclassified point and use it to update the weights vector (using gradient descent)
            #We choose a random misclassified point and use it to update our weights
            wrong_point_index = np.random.choice(wrong_point_indices)
            for k in range(len(attempted_weights)):
                attempted_weights[k] += correct_classifications[wrong_point_index]*points[k][wrong_point_index] 
        self.attempts = attempts        
        self.best_attempt = best_attempt
        return  self.best_attempt
    
#Running classifier for a predefined number of times (determined by the runs variable)
total_attempts = 0
for i in range(runs):
    #Here, we generate an N number of random points (necessarily linearly separable in order for the perceptron to converge) and d+1 weights
    #just for the sake of experimatation
    points = lngn.generate_points(N)
    weights = lngn.generate_weights()
    correct_classifications = lngn.classify_points(points, weights)
    
    #We let the perceptron learn and generate learned weights (we also keep track of the total attempts)
    Perceptron = PLA()
    attempts_weights = Perceptron.pla(points, correct_classifications, linear_regression=linear_regression)
    total_attempts += Perceptron.attempts


print("Average attempts: " + str(total_attempts/runs))
