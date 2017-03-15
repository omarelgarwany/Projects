# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 15:01:17 2016

@author: omar
"""
import LinearGenerator as lngn
import numpy as np
import matplotlib.pyplot as plt
import random
runs = 1000
in_sample_N = 100
out_sample_N = 1000
class LR:
    """
    Estimating the weight matrix by linear regression using the Moore-Penrose pseudoinverse method
    """
    def linear_regression(self, points, correct_classifications):
        points = np.array(points)
        correct_classifications = np.array([correct_classifications])
        points_pinv =  np.linalg.pinv(points)
        weights = np.matrix.dot(correct_classifications, points_pinv)
        return weights[0]
total_errors = 0 
for i in range(runs):
    #Producing in-sample and out-of-sample random points
    in_sample_points = lngn.generate_points(in_sample_N)
    out_of_sample_points = lngn.generate_points(out_sample_N)

    #Generating random weights
    correct_weights = lngn.generate_weights()
    
    #Classifying based on correct weights
    correct_classifications_in_sample = lngn.classify_points(in_sample_points, correct_weights)
    correct_classifications_out_of_sample = lngn.classify_points(out_of_sample_points, correct_weights)

    #Attempting to generate weights by linear regression
    LinReg = LR()
    attempted_weights = LinReg.linear_regression(in_sample_points, correct_classifications_in_sample)
    
    #Classifying in-sample and out of sample using learned weights
    attempted_classifications_in_sample = lngn.classify_points(in_sample_points, attempted_weights)    
    attempted_classifications_out_of_sample = lngn.classify_points(out_of_sample_points, attempted_weights)

    #Calculating in-sample and out-of-sample errors    
    error = lngn.classification_error(correct_classifications_in_sample, attempted_classifications_in_sample)
    
    #Averaging error over runs
    total_errors += error

print(total_errors/runs)
