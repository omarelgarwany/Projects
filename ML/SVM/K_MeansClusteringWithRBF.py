# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 05:07:14 2016

@author: omar

The aim is to practice implementing K-means clustering using an RBF kernel and compute the in sample error (Ein) averaged over many runs
using many configurations (e.g different numbers of clusters K, different gammas for the kernel)
"""

import numpy as np
def compute_error(attempted_classes, correct_classes):
    error = 0
    for i in range(len(attempted_classes)):
        if attempted_classes[i] != correct_classes[i]:
            error += 1
    return error/len(attempted_classes)   
def function(x):
    return x-0.25*np.sin(np.pi*x)

def target(point):
    return np.sign(point[1]-point[0]+0.25*np.sin(np.pi*point[0]))
 
def generate_points(N):
    dataset = []
    for i in range(N):
        dataset.append([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
    return np.array( dataset )
    
 #K-means   
def assign_points_to_clusters(points, centers):
    """
    This assigns points to clusters based on distance
    """
    K = len(centers)
    N, d = points.shape
    clusters = [[] for i in range(K)]
    for point_index in range(N):
        least_distance = float("inf")
        nearest_center = None
        for center_index in range(K):
            distance = np.linalg.norm(points[point_index] - centers[center_index])
            if distance < least_distance:
                least_distance = distance
                nearest_center = center_index
        clusters[nearest_center].append(point_index)
    return np.array(clusters)
def calculate_clusters_centers(points, clusters):
    """
    This calculates the centers of clusters given K defined clusters
    """
    N, d = points.shape

    centers = []
    for cluster in clusters:
        center = np.array( [0 for i in range(d)] )
        for point_index in cluster:

            center = center + points[point_index]
        center /= len(cluster)
        centers.append(center)
        
    return np.array(centers)
 
def K_means(points, starting_centers, termination_distance = .1):
    """
    This implements a heuristic algorithm for K-means clustering using Lloyd's algorithm
    """
    terminate = False
    K = len(starting_centers)
    while terminate == False:
        terminate = True
        clusters = assign_points_to_clusters(points, starting_centers)
        centers = calculate_clusters_centers(points, clusters)
        for center_index in range(K):
            if np.linalg.norm(starting_centers[center_index] - centers[center_index]) > termination_distance:
                terminate = False
                break
        starting_centers = centers

    return clusters, centers

def K_means_rbf_kernel(points, labels, clusters, centers, gamma = 1):
    """
    Computing weights using an RBF kernel
    """
    N, d =points.shape
    K = len(clusters)
    phi = np.array( [ [ np.exp(-1 * gamma * (np.linalg.norm(points[i] - centers[j])**2)) for j in range(K)] for i in range(N) ] )
    phi = np.concatenate((np.ones((N, 1)), phi), axis=1)    
    return np.dot(np.linalg.pinv(phi), labels)   

def predict_K_means_rbf(k_weights, centers, points, gamma=1):
    """
    Predicts class using RBF kernel
    """
    predictions = []
    N,d = points.shape
    K = len(centers)
    centers = np.concatenate((np.ones((K, 1)), centers), axis=1)    
    points = np.concatenate((np.ones((N, 1)), points), axis=1)    

    for point in points:
        signal = 0
        for i in range(K):
            signal += k_weights[i+1] *  np.exp(-1 * gamma * (np.linalg.norm(point - centers[i])**2) )
        predictions.append(np.sign(signal + k_weights[0]))
    return np.array(predictions)

#K-means
K = 9
termination_distance = 0
gamma = 1.5
train = 100
runs = 200

separable = 0
for i in range(runs):
    training_points = generate_points(train)
    training_labels = np.array([target(point) for point in training_points])

    
    
    #training
    initial_centers= generate_points(K)
    clusters, centers = K_means(training_points, initial_centers, termination_distance)
    k_weights = K_means_rbf_kernel(training_points, training_labels, clusters, centers, gamma=gamma)

    #Ein
    predictions_in_sample = predict_K_means_rbf(k_weights, centers, training_points, gamma=gamma)
    Ein = compute_error(predictions_in_sample, training_labels)
    if Ein == 0:
        separable += 1
    
print("Percentage of Ein=0 is", (separable*100)/runs, "%")
