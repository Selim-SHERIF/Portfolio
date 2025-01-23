# CS-433 Machine Learning
# Project 1 - Model for predicting MICHD

# Group Pandas
    # Ali Elkilesly - 345334
    # Selim Sherif - 346035
    # Roy Turk - 345573

# "run.py"
# Main python script for building the model and predicting MICHD

# Header declaration
import importlib
import matplotlib.pyplot as plt
import seaborn as sns

import random
import numpy as np

import implementations
from implementations import *
import functions
from functions import *

importlib.reload(functions)
importlib.reload(implementations)

# ==============================================================================
# SECTION: [Load dataset]
# ==============================================================================

path_x_train = '../data/dataset/x_train.csv' # Filepath to x_train
path_y_train = '../data/dataset/y_train.csv' # Filepath to y_train
path_x_test = '../data/dataset/x_test.csv' # Filepath to x_test

x_train, headers = load_csv_data(path_x_train) # Load x_train
y_train, headers_y_train = load_csv_data(path_y_train) # Load y_train
x_test, _ = load_csv_data(path_x_test) # Load x_test

# ==============================================================================
# SECTION: [Pre-processing and feature engineering]
# ==============================================================================

# Filter all features containing more than 60% of NaNs
x_tr_no_sparse, x_te_no_sparse , headers_no_sparse = filter_features_with_nans(x_train, x_test, headers, nan_threshold=0.60)


# Filter all features with very low variance
x_tr_no_const, headers_no_const, x_te_no_const = check_variance(x_tr_no_sparse,x_te_no_sparse, headers_no_sparse, 0.05)

# Create a copy of the dataset, and replace all coded values such as 77,88... with NaNs
x_copy = replace_values_with_nan(x_tr_no_const, headers_no_const)

# Filter features with the mean difference and ratio of standard deviation techniques
filtered_x_copy, filtered_headers, mean_diffs, std_ratios= target_feature_selection(x_copy, 
                                y_train[:,1], headers_no_const, 0.1, 1.3)

# Import the type.csv file to select the hand-picked features with their respective type (continuous, categorical, ordinal)
filename = "types.csv" # Filepath to .csv file
filtered_headers, masked_features = load_headers_extract_features(filename)

# Select the hand-picked features from the training and test data
x_filtered = filter_dataset1(x_tr_no_const, headers_no_const, filtered_headers)
x_te_filtered = filter_dataset1(x_te_no_const, headers_no_const, filtered_headers)

# Get the masks to organize features by their respective type (continuous, categorical, ordinal)
masked_headers_continuous, masked_first_row_continuous, masked_headers_categorical,masked_first_row_categorical, masked_headers_ordinal, masked_first_row_ordinal = variable_type_separation(filename, filtered_headers)


# Remove all NaN values and missing responses (blank, refused to answer, don't know...) from training and test data
x_filtered2 = filter_dataset2(x_filtered, filtered_headers)
x_te_filtered2 = filter_dataset2(x_te_filtered, filtered_headers)

x_filtered2, x_te_filtered2 = standardize_filtered_headers(filtered_headers, masked_headers_continuous, x_filtered2, x_te_filtered2)

# Measure the highly correlated features for continuous features
high_correlation_results = identify_highly_correlated_features(x_filtered2, filtered_headers, masked_headers_continuous,threshold=0.8)


# Measure the highly correlated features for ordinal features
high_correlation_results = identify_highly_correlated_features(x_filtered2, filtered_headers, masked_headers_ordinal,threshold=0.8)


# Measure the highly correlated features for categorical features
categorical_indices = [filtered_headers.index(header) for header in masked_headers_categorical] # Get the categorical variables indices
x_categorical = x_filtered2[:, categorical_indices] # Create a NumPy array containing all the categorical features

results_all_pairs = calculate_cramers_v_all_pairs(x_categorical) # Get Cramer's V for all categorical features

threshold = 0.85 # Set a threshold to filter inter-dependent features
correlated  = get_correlated_features(x_categorical, results_all_pairs, masked_headers_categorical, threshold) # Get the correlated categorical features

features_to_remove = select_redundant_features(correlated)
features_to_remove.append('_AGE80')

# Identify columns to keep (i.e., not in the redundant features)
columns_to_keep = [i for i in range(x_filtered2.shape[1]) if filtered_headers[i] not in features_to_remove]

# Return the final dataset
x_filtered2 = x_filtered2[:, columns_to_keep]
x_te_filtered2 = x_te_filtered2[:, columns_to_keep]



# Remove the correlated features from masked_headers_categorical
filtered_headers = [
    header for header in filtered_headers if header not in features_to_remove
]

# One-hot encode the categorical features in the training and testing data
encoded_data = one_hot_encode_batches(x_filtered2, filtered_headers, masked_headers_categorical, batch_size=1000)
test_encoded_data = one_hot_encode_batches(x_te_filtered2, filtered_headers, masked_headers_categorical, batch_size=1000)

# ==============================================================================
# SECTION: [Model building]
# ==============================================================================

# Convert all -1 in y_train to 0 for the logistic loss function
y_train[y_train == -1] = 0

# Add bias term in both training and testing matrices
ones2 = np.ones((encoded_data.shape[0], 1))  # Column of ones for x_filtered2
tx = np.hstack((ones2, encoded_data))  # Concatenate ones as the first column

ones_test2 = np.ones((test_encoded_data.shape[0], 1))  # Column of ones for x_te_filtered2
tx_test = np.hstack((ones_test2, test_encoded_data))  # Concatenate ones as the first column

initial_w = np.zeros(tx.shape[1])

w, train_losses= logistic_regression_no_early_stopping(y_train[:,1], tx, initial_w, gamma=0.001, batch_size=2000, lambda_=0.0, max_iter=1800)
w,train_losses_fine=logistic_regression_no_early_stopping(y_train[:,1], tx, w, gamma=0.0001, batch_size=2000, lambda_=0.0, max_iter=150)

y_test = np.zeros((x_test.shape[0],2))

y_test[:,0] = x_test[:,0]

# Assuming tx_test is your test feature set and w is your weight vector
y_test[:, 1] = sigmoid(tx_test @ w)  # Compute predictions using the sigmoid function
y_test[:, 1] = (y_test[:, 1] > 0.195).astype(int)  # Convert probabilities to binary outcomes

# Convert 0s to -1s in y_test
y_test[y_test == 0] = -1

header = np.array([["Id", "Prediction"]])
y_test= np.vstack((header, y_test.astype(str)))
np.savetxt('y_test.csv', y_test, delimiter=',', comments='', fmt='%s')


print("The logistic regression model was successfully built. Please check the 'y_test.csv' file saved in the same repository as this 'run.py' file.")
