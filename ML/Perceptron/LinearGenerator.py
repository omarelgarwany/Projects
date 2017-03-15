# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 05:38:57 2016

@author: omar
This is a group of helper functions to generate linearly separable classified points (how much separation, if any, can also be controlled)
There are also helper functions for plotting, computing classification error and classify points given thir weights
"""
import random
import numpy as np
def generate_points( N=100, x1=[-1, 1], x2=[-1, 1]):
    x0 = [1 for x in range(N)]
    x1 = [random.uniform(x1[0], x1[1]) for x in range(N)]
    x2 = [random.uniform(x2[0], x2[1]) for x in range(N)]
    return [x0, x1, x2]
def generate_weights( x1=[-1, 1], x2=[-1, 1]):
    point_one = (random.uniform(x1[0], x1[1]), random.uniform(x2[0], x2[1]))
    point_two = (random.uniform(x1[0], x1[1]), random.uniform(x2[0], x2[1]))
    m = (point_one[1]-point_two[1])/((point_one[0]-point_two[0]))
    A = np.random.uniform(-1000, 1000)
    B = (-A) * m
    C = A*point_one[1] + B*point_one[0]
    C = -C
    return [C, B, A]

def generate_line( weights, domain=[-1, 1]):

    x1 = [x for x in np.linspace(domain[0], domain[1])]
    x2 = [((-weights[1]*x) -weights[0])/weights[2] for x in x1]
    return [x1, x2]
def separate_points(points, weights):
    classified_points = {-1: [[], [], []], 1: [[], [], []]}
    x1 = points[1]
    x2 = points[2]
    for i in range(len(x1)):
        classification = np.sign(weights[0] + weights[1]*x1[i] + weights[2]*x2[i])
        classified_points[classification][0].append( 1 )
        classified_points[classification][1].append( x1[i] )
        classified_points[classification][2].append( x2[i] )
    return classified_points
def random_separate_points(points, weights, fraction=0.9):
    classified_points = {-1: [[], [], []], 1: [[], [], []]}
    x1 = points[1]
    x2 = points[2]
    for i in range(len(x1)):
        random_counter = random.uniform(0, 1)
        if random_counter > fraction:
            classification = np.random.choice([-1, 1])
        else:
            classification = np.sign(weights[0] + weights[1]*x1[i] + weights[2]*x2[i])
        classified_points[classification][0].append( 1 )
        classified_points[classification][1].append( x1[i] )
        classified_points[classification][2].append( x2[i] )
    return classified_points
def classify_points( points, weights):
    points_count = len(points[0])
    y = []
    for i in range(points_count):
        if weights[2]*points[2][i] + weights[1]*points[1][i] + weights[0]*points[0][i] > 0:
            y.append(1)
        else:
            y.append(-1)
    return y
def classification_error(error1, error2):
    assert len(error1) == len(error2)    
    error = 0
    total_points = len(error1)
    for i in range(total_points):
        if error1[i] != error2[i]:
            error += 1
    return error/total_points
