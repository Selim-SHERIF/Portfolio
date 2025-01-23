# CS-433 Machine Learning
# Project 1 - Model for predicting MICHD

# Group Pandas
    # Ali Elkilesly - 345334
    # Selim Sherif - 346035
    # Roy Turk - 345573

# "functions.py"
# Python script containing all additional functions used in run.py script

# Header declaration
import numpy as np
import csv
import os

# ==============================================================================
# SECTION: Data Preprocessing
# ------------------------------------------------------------------------------
# Purpose  : Functions to clean, filter, and prepare the dataset for analysis,
#            including handling NaN values, feature scaling, and encoding.
#
# Usage    : Call these functions before any modeling to ensure that the dataset
#            is clean and properly formatted for input into machine learning models.
# ------------------------------------------------------------------------------
# Function List:
#    - load_csv_data(file_path)
#    - filter_features_with_nans(x_train, x_test, headers, nan_threshold)
#    - check_variance(data, x_test, headers, threshold)
#    - min_max_normalize(data)
#    - target_feature_selection(data, target, headers, mean_threshold, std_ratio_threshold)
#    - replace_values_with_nan(data, headers)
#    - load_headers_extract_features(filename)
#    - variable_type_separation(filename, filtered_headers)
#    - filter_dataset1(X_sampled, headers, filtered_headers)
#    - filter_dataset2(x_filtered, filtered_headers)
#    - standardize(data)
#    - identify_highly_correlated_features(x_data, filtered_headers, masked_headers_continuous, threshold=0.8)
#    - chi2(x, y)
#    - cramers_v(x, y)
#    - cramers_v_with_target(categorical_features, target, headers)
#    - chi2_2arrays(x, y)
#    - cramers_v_2arrays(x, y)
#    - calculate_cramers_v_all_pairs(categorical_features)
#    - print_cramers_v(results, feature_names)
#    - print_combinations_above_threshold(results, feature_names, threshold)
#    - get_correlated_features(data, results, headers, threshold)
#    - select_redundant_features(correlated_dict)
#    - one_hot_encode_batches(X, headers, masked_headers_categorical, batch_size=1000)
# ==============================================================================

def load_csv_data(file_path):
    """
    Load data from a CSV file, converting values to float where possible
    and replacing empty strings with np.nan.

    Args: 
        file_path: .csv filepath

    Returns: 
        data: Dataset as a numpy array
        headers: List of headers corresponding to each feature
    """

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Assume there's a header row and skip it
        
        data = []
        for row in reader:
            processed_row = []
            for value in row:
                if value == '':
                    processed_row.append(np.nan)  # Replace empty strings with np.nan
                else:
                    try:
                        processed_row.append(float(value))  # Convert to float if possible
                    except ValueError:
                        processed_row.append(value)  # Keep non-numeric values as is
            data.append(np.array(processed_row))

    return np.array(data), headers

def filter_features_with_nans(x_train, x_test, headers, nan_threshold):
    """
    Filters out features from x_train with more than a given percentage of NaN values and removes the same features from x_test.
    
    Args:
        x_train: NumPy array of shape (N, D)
        x_test: NumPy array of shape (N, D)
        headers: List of feature names (headers)
        nan_threshold: Proportion of NaN values (between 0 and 1). Features with more NaNs than this threshold in x_train will be removed in both datasets.
    
    Returns:
        filtered_x_train: NumPy array with filtered features based on the NaN threshold for x_train.
        filtered_x_test: NumPy array with filtered features from x_test (using the same columns as x_train).
        filtered_headers: Updated headers after removing columns.
    """
    
    nan_counts = np.isnan(x_train).sum(axis=0) # Number of NaN values per feature in x_train
    
    nan_proportions = nan_counts / x_train.shape[0] # Proportion of NaN values for each feature in x_train
    
    valid_columns = nan_proportions <= nan_threshold # Mask to filter out features with NaN proportions greater than the threshold
    
    filtered_x_train = x_train[:, valid_columns] # Filter x_train using the mask
    filtered_x_test = x_test[:, valid_columns] # Filter x_test using the same mask
    
    filtered_headers = [header for i, header in enumerate(headers) if valid_columns[i]] # Filter out the headers
    
    return filtered_x_train, filtered_x_test, filtered_headers

def check_variance(data, x_test, headers, threshold):
    """
    Checks if features have sufficient variance and prints headers of low variance features.
    Also removes the same low variance features from the testing data.

    Args:
        data: NumPy array of shape (N, D) for training
        x_test: NumPy array of shape (N, D) for testing
        headers: List of feature names
        threshold: Minimum variance for a feature to be considered useful
    
    Returns:
        filtered_data: NumPy array with low variance features removed from training data.
        filtered_headers: List of headers after removing low variance features.
        filtered_x_test: NumPy array with low variance features removed from testing data.
    """

    variances = np.var(data, axis=0) # Variance of each feature
    
    low_variance_features = np.where(variances < threshold)[0] # Identify low variance features
    removed_headers = [headers[i] for i in low_variance_features] # Identify headers with low variance features
    
    filtered_data = np.delete(data, low_variance_features, axis=1) # Filter out low variance features from training data
    filtered_headers = [header for i, header in enumerate(headers) if i not in low_variance_features] # Filter out the headers
    
    filtered_x_test = np.delete(x_test, low_variance_features, axis=1) # Filter out low variance features from testing data
    
    # Print removed headers
    # print("Removed low variance features:", removed_headers)
    
    return filtered_data, filtered_headers, filtered_x_test

def min_max_normalize(data):
    """Normalizes the data using Min-Max scaling.
    
    Args:
        data: NumPy array of shape (N, D)

    Returns:
        normalized_data: NumPy array of shape (N, D)
    """

    min_vals = np.nanmin(data, axis=0)
    max_vals = np.nanmax(data, axis=0)

    normalized_data = (data - min_vals) / (max_vals - min_vals)

    return normalized_data

def target_feature_selection(data, target, headers, mean_threshold, std_ratio_threshold):
    """
    Measures the mean difference (bias) and the ratio of standard deviations (variance) of each feature
    based on the target variable and filters features based on specified thresholds.

    Args:
        data: NumPy array of shape (N, D)
        target: NumPy array of shape (N, )
        headers: List of feature names (headers)
        mean_threshold: Minimum mean difference for a feature to be considered useful
        std_ratio_threshold: Threshold for the ratio of standard deviations

    Returns:
        filtered_data: NumPy array with features that meet the mean difference and standard deviation ratio thresholds
        filtered_headers: Updated headers after removing low mean difference and standard deviation ratio features
        mean_diffs: Dictionary with mean difference per feature based on target values
        std_ratios: Dictionary with standard deviation ratios per feature based on target values
    """

    normalized_data = min_max_normalize(data) # Perform min-max normalization on data

    mean_diffs = {} # Initialize mean difference dictionary
    std_ratios = {} # Initialize stander deviation ratio dictionary
    target_classes = np.unique(target)

    # Calculate mean differences and standard deviation ratios for each feature
    for i in range(normalized_data.shape[1]):
        means = [
            np.nanmean(normalized_data[target == -1, i]) if np.any(target == -1) else 0,
            np.nanmean(normalized_data[target == 1, i]) if np.any(target == 1) else 0
        ]
        mean_diff = abs(means[0] - means[1])
        mean_diffs[headers[i]] = mean_diff

        std_values = [
            np.nanstd(normalized_data[target == -1, i]) if np.any(target == -1) else 0,
            np.nanstd(normalized_data[target == 1, i]) if np.any(target == 1) else 0
        ]

        # Calculate standard deviation ratio
        std_ratio = std_values[0] / (std_values[1] + 1e-10)  # Add a small value to avoid division by zero
        std_ratios[headers[i]] = std_ratio

    # Filter features based on the single threshold for std ratio
    valid_features = [
        header for header in headers
        if mean_diffs[header] >= mean_threshold or (std_ratios[header] <= 1 / std_ratio_threshold or std_ratios[header] >= std_ratio_threshold)
    ]

    valid_mask = np.isin(headers, valid_features) # Create a mask for the valid features

    filtered_data = data[:, valid_mask] # Filter the data
    filtered_headers = [header for header in headers if header in valid_features] # Filter the headers

    # Print removed features
    # removed_features = [header for header in headers if header not in valid_features]
    # print("Removed features with low mean difference or out-of-bound standard deviation ratio:")
    # for header in removed_features:
    #     print(f"{header}: Mean Diff = {mean_diffs[header]:.4f}, Std Ratio = {std_ratios[header]:.4f}")

    # retained_features = [header for header in headers if header in valid_features]
    # print("\nRetained features:")
    # for header in retained_features:
    #     print(f"{header}: Mean Diff = {mean_diffs[header]:.4f}, Std Ratio = {std_ratios[header]:.4f}")

    return filtered_data, filtered_headers, mean_diffs, std_ratios

def replace_values_with_nan(data, headers):
    """
    Replaces specified values in the dataset with NaNs and performs actions based on max value ranges.

    Args
        data: NumPy array of shape (N, D)
        headers: List of features names (headers)
        values_to_replace: List of values to be replaced with NaN

    Returns:
        updated_data: NumPy array with specified values replaced by NaNs
    """

    # Create a copy of the data to avoid modifying the original dataset
    updated_data = data.copy()

    # Check max values and perform actions
    for i, header in enumerate(headers):
        max_value = np.nanmax(updated_data[:, i])  # Ignore NaNs in max calculation
        
        if 0 <= max_value < 10:
            updated_data[(updated_data[:, i] == 7) | (updated_data[:, i] == 8) | (updated_data[:, i] == 9), i] = np.nan
        elif 10 <= max_value <= 99:
            updated_data[(updated_data[:, i] == 77) | (updated_data[:, i] == 88) | (updated_data[:, i] == 99), i] = np.nan
        elif 100 <= max_value <= 999:
            updated_data[(updated_data[:, i] == 777) | (updated_data[:, i] == 888) | (updated_data[:, i] == 999), i] = np.nan
        elif 1000 <= max_value <= 9999:
            updated_data[(updated_data[:, i] == 7777) | (updated_data[:, i] == 9999), i] = np.nan
        elif 10000 <= max_value:
            updated_data[(updated_data[:, i] == 99999) | (updated_data[:, i] == 999999) | (updated_data[:, i] == 99900) | (updated_data[:, i] == 777777), i] = np.nan

    return updated_data

def load_headers_extract_features(filename):
    """
    Loads the csv. file that contains the filtered features to be hand-picked and classed with respect to their type

    Args: 
        filename: .csv filepath

    Returns:
        masked_headers: list containing the headers of the kept features
        masked_second_row: contains the kept features
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader) 
        first_row = next(reader) 
        second_row = next(reader)
        
        # Mask the columns
        masked_headers = [headers[i] for i in range(len(second_row)) if float(second_row[i]) != 1]
        masked_second_row = [second_row[i] for i in range(len(second_row)) if float(second_row[i]) != 1]
        
    
    return masked_headers, masked_second_row

def variable_type_separation(filename, filtered_headers):
    """
    Function that separates the variables by their type

    Args:
        filename: .csv filepath
        filtered_headers: list containing the filtered features headers

    Returns:
        masked_headers_continuous: list of continuous features headers
        masked_first_row_continuous: contains the continuous features
        masked_headers_categorical: list of categorical features headers
        masked_first_row_categorical: contains the categorical features
        masked_headers_ordinal: list of ordinal features headers
        masked_first_row_ordinal: contains the ordinal features
    """

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Extract headers
        first_row = next(reader)  # Extract only the first row

        # Continuous masks
        masked_headers_continuous = []
        masked_first_row_continuous = []
        
        # Categorical masks
        masked_headers_categorical = []
        masked_first_row_categorical = []
        
        # Ordinal masks
        masked_headers_ordinal = []
        masked_first_row_ordinal = []

        for i, header in enumerate(headers):
            if header in filtered_headers:
                value = float(first_row[i]) 
                if value == 1:
                    masked_headers_continuous.append(header)
                    masked_first_row_continuous.append(first_row[i])
                elif value == 2:
                    masked_headers_categorical.append(header)
                    masked_first_row_categorical.append(first_row[i])
                elif value == 3:
                    masked_headers_ordinal.append(header)
                    masked_first_row_ordinal.append(first_row[i])

    return masked_headers_continuous, masked_first_row_continuous, masked_headers_categorical, masked_first_row_categorical, masked_headers_ordinal, masked_first_row_ordinal

def filter_dataset1(X_sampled, headers, filtered_headers):
    """
    Extract the chosen features from the original dataset

    Args: 
        X_sampled: NumPy array containing the dataset
        headers: list containing the headers of the dataset
        filtered_headers: list containing the filtered headers

    Returns:
        X_filtered: NumPy array containing the filtered dataset
    """

    filtered_indices = [headers.index(header) for header in filtered_headers]
    
    X_filtered = np.array(X_sampled[:, filtered_indices])
    
    return X_filtered

def filter_dataset2(x_filtered, filtered_headers):
    """
    Filter the dataset with respect to each feature

    Args:
        x_filtered: NumPy array containing the filtered dataset
        filtered_headers: list containing the filtered headers

    Returns:
        x_filtered: Numpy array containing the modified dataset
    """

    for header in filtered_headers:
        index = filtered_headers.index(header)
        if header in ['PHYSHLTH', 'MENTHLTH', 'POORHLTH', 'DRNK3GE5']:

            mask = np.isin(x_filtered[:, index], [77, 88, 99]) | np.isnan(x_filtered[:, index]) # Mask for the conditions
            average = np.sum(x_filtered[~mask, index]) / x_filtered[~mask, index].size # Compute mean of feature
            x_filtered[mask, index] = average # Impute with mean

        elif header in ['_AGE80', '_LLCPWT', 'FC60_', 'PA1VIGM_']:

            mask = np.isin(x_filtered[:, index], [99900]) | np.isnan(x_filtered[:, index]) # Mask for the conditions
            average = np.sum(x_filtered[~mask, index]) / x_filtered[~mask, index].size # Compute mean of feature
            x_filtered[mask, index] = average # Impute with mean

        elif header in ['MAXVO2_']:

            mask = np.isin(x_filtered[:, index], [999]) | np.isnan(x_filtered[:, index]) # Mask for the conditions
            average = np.sum(x_filtered[~mask, index]) / x_filtered[~mask, index].size # Compute mean of feature
            x_filtered[mask, index] = average # Impute with mean

        elif header in ['WEIGHT2']:

            mask_kg = (x_filtered[:, index] >= 9000) & (x_filtered[:, index] < 9998)  # Mask for the condition
            x_filtered[mask_kg, index] = (x_filtered[mask_kg, index] - 9000) * 2.2  # Convert the weight
            mask = np.isin(x_filtered[:, index], [7777,9999]) | np.isnan(x_filtered[:, index]) # Mask for the condition
            average = np.sum(x_filtered[~mask, index]) / x_filtered[~mask, index].size # Compute mean of feature
            x_filtered[mask, index] = average # Impute with mean

        elif header in ['HEIGHT3']:

            mask_m = (x_filtered[:, index] >= 9000) & (x_filtered[:, index] < 9998)  # Mask for the condition
            x_filtered[mask_m, index] = (x_filtered[mask_m, index] - 9000) * 3.281  # Convert the height
            mask = np.isin(x_filtered[:, index], [7777,9999]) | np.isnan(x_filtered[:, index]) # Mask for the condition
            average = np.sum(x_filtered[~mask, index]) / x_filtered[~mask, index].size # Compute mean of feature
            x_filtered[mask, index] = average # Impute with mean

        elif header in ['AGE65YR']:

            mask = np.isin(x_filtered[:, index], [3]) | np.isnan(x_filtered[:, index]) # Mask for the condition
            x_filtered[mask, index] = 0 # Impute with 0

        else:

            mask = np.isin(x_filtered[:, index], [7, 8, 9]) | np.isnan(x_filtered[:, index]) # Mask for the condition
            x_filtered[mask, index] = 0 # Impute with 0
            
    return x_filtered

def standardize(data):
    """
    Function that performs Z-score normalization on each feature of the dataset

    Args:
        data: NumPy array containing the dataset

    Returns:
        Z-score
    """

    if np.std(data) != 0:
        return (data - np.mean(data))/np.std(data)
    else:
        return 0
    
def standardize_filtered_headers(filtered_headers, masked_headers_continuous, x_filtered2, x_te_filtered2):
    """
    Standardizes the specified continuous headers in the input arrays.

    Parameters:
    - filtered_headers: List of headers to be filtered.
    - masked_headers_continuous: List of headers to be standardized.
    - x_filtered2: 2D NumPy array for training data.
    - x_te_filtered2: 2D NumPy array for testing data.

    Returns:
    - x_filtered2: Standardized training data.
    - x_te_filtered2: Standardized testing data.
    """
    
    for header in filtered_headers:
        if header in masked_headers_continuous:
            index = filtered_headers.index(header)
            # Standardize the training data
            mean = np.mean(x_filtered2[:, index])
            std = np.std(x_filtered2[:, index])
            x_filtered2[:, index] = (x_filtered2[:, index] - mean) / std
            
            # Standardize the testing data using the same mean and std
            x_te_filtered2[:, index] = (x_te_filtered2[:, index] - mean) / std
    
    return x_filtered2, x_te_filtered2

def identify_highly_correlated_features(x_data, filtered_headers, masked_headers_continuous, threshold=0.8):
    """
    Functions that identifies the highly correlated features using the correlation matrix

    Args:
        x_data: NumPy array containing the dataset
        filtered_headers: list containing the filtered headers
        masked_headers_continuous: list containing the headers of continuous features
        threshold: value for eliminating features

    Returns:
        highly_correlated: highly correlated features
    """
    highly_correlated = {}
    
    x_data = np.array(x_data)

    continuous_indices = [filtered_headers.index(header) for header in masked_headers_continuous] # Get indices of continuous features
    
    correlation_matrix = np.corrcoef(x_data[:, continuous_indices], rowvar=False) # Compute the correlation matrix
    
    # Loop through each continuous header to check for correlation
    for idx, header in enumerate(masked_headers_continuous):

        correlations = correlation_matrix[idx]
        
        correlated_indices = np.argwhere(np.abs(correlations) > threshold).flatten() # Get indices of highly correlated features
        
        correlated_indices = correlated_indices[correlated_indices != idx] # Exclude self correlation
        
        if correlated_indices.size > 0:
            highly_correlated[header] = [masked_headers_continuous[i] for i in correlated_indices]

    return highly_correlated

def chi2(x, y):
    """
    Computes the chi-squared statistic
    
    Args:
    x and y

    Returns: 
    chi-squared statistic
    """

    if len(x) != len(y):
        raise ValueError("Input arrays must have the same length")

    categories_x = np.unique(x)
    categories_y = np.unique(y)
    num_categories_x = len(categories_x)
    num_categories_y = len(categories_y)

    contingency_table = np.zeros((num_categories_x, num_categories_y)) # Create a contingency table

    for i in range(num_categories_x):
        for j in range(num_categories_y):
            contingency_table[i, j] = np.sum(
                (x == categories_x[i]) & (y == categories_y[j])
            )

    observed = contingency_table
    expected = np.outer(np.sum(observed, axis=1), np.sum(observed, axis=0)) / np.sum(observed) # Calculate the chi-squared statistic

    # To avoid division by zero, we filter the expected values
    with np.errstate(divide='ignore', invalid='ignore'):
        chi2_statistic = np.nansum((observed - expected) ** 2 / expected)

    return chi2_statistic

def cramers_v(x, y):
    """
    Computes Cramer's V

    Args: 
    x and y

    Return:
    Cramer's V
    """
    chi2_statistic = chi2(x, y) # Get the chi-sqaured
    
    n = len(x)

    categories_x = np.unique(x).size # Number of categories for x
    categories_y = np.unique(y).size # Number of categories for y

    phi2 = chi2_statistic / n
    cramers_v = np.sqrt(phi2 / min(categories_x - 1, categories_y - 1))

    return cramers_v

def cramers_v_with_target(categorical_features, target, headers):
    """
    Computes Cramer's V between the categorical features and the target variable

    Args:
    categorical_features: NumPy array containing the categorical features
    target: NumPy array containing the target variable
    headers: list containing the headers of each feature

    Returns:
    results
    """

    num_features = categorical_features.shape[1]
    results = {}

    # Calculate Cramér's V for each feature with respect to the target
    for i in range(num_features):
        cramers_statistic = cramers_v(categorical_features[:, i], target)
        results[headers[i]] = cramers_statistic

    # Print results
    # print("Cramér's V values for each feature with the target:")
    # for feature, value in results.items():
    #     print(f"{feature}: Cramér's V = {value:.3f}")

    return results

def chi2_2arrays(x, y):
    """
    Computes chi-squared between two arrays

    Args: 
    x and y

    Returns: 
    chi-squared statistic, num_categories_x, num_categories_y
    """

    if len(x) != len(y):
        raise ValueError("Input arrays must have the same length")

    categories_x = np.unique(x)
    categories_y = np.unique(y)
    num_categories_x = len(categories_x)
    num_categories_y = len(categories_y)

    contingency_table = np.zeros((num_categories_x, num_categories_y))

    for i in range(num_categories_x):
        for j in range(num_categories_y):
            contingency_table[i, j] = np.sum((x == categories_x[i]) & (y == categories_y[j]))

    observed = contingency_table
    expected = np.outer(np.sum(observed, axis=1), np.sum(observed, axis=0)) / np.sum(observed)

    with np.errstate(divide='ignore', invalid='ignore'):
        chi2_statistic = np.nansum((observed - expected) ** 2 / expected)

    return chi2_statistic, num_categories_x, num_categories_y

def cramers_v_2arrays(x, y):
    """
    Computes Cramer's between two arrays

    Args: 
    x and y

    Returns:
    Cramer's V
    """

    chi2_statistic, k1, k2 = chi2_2arrays(x, y)
    n = len(x)

    if n == 0 or min(k1 - 1, k2 - 1) == 0:
        return 0.0

    return np.sqrt(chi2_statistic / (n * min(k1 - 1, k2 - 1)))

def calculate_cramers_v_all_pairs(categorical_features):
    """
    Computes Cramer's V between all categorical features

    Args: 
    categorical_features

    Returns:
    results
    """

    num_features = categorical_features.shape[1]
    results = np.zeros((num_features, num_features))

    for i in range(num_features):
        for j in range(i + 1, num_features):
            cramers_v_statistic = cramers_v_2arrays(categorical_features[:, i], categorical_features[:, j])
            results[i, j] = cramers_v_statistic
            results[j, i] = cramers_v_statistic

    return results

def print_cramers_v(results, feature_names):
    """
    Print Cramer's V
    """

    # Print header
    print(f"{'Feature':<20}", end='')
    for name in feature_names:
        print(f"{name:<20}", end='')
    print()
    
    # Print each row of results
    for i, row in enumerate(results):
        print(f"{feature_names[i]:<20}", end='')
        for value in row:
            print(f"{value:<20.4f}", end='')
        print()

def print_combinations_above_threshold(results, feature_names, threshold):
    """
    Print the combinations from Cramer's V above the threshold
    """

    print(f"Combinations with Cramér's V > {threshold}:")
    found = False
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            if results[i, j] > threshold:
                print(f"{feature_names[i]} - {feature_names[j]}: {results[i, j]:.4f}")
                found = True
    if not found:
        print("No combinations found above the threshold.")

def get_correlated_features(data, results, headers, threshold):
    """
    Returns a dictionary of correlated features based on Cramér's V values.

    Args:
        data: NumPy array of the original dataset with categorical features
        results: NumPy array or matrix of Cramér's V values
        headers: List of feature names
        threshold: Threshold for Cramér's V above which features are considered correlated.

    Returns:
        dict: Dictionary where keys are correlated feature headers, and values are lists of correlated features
    """

    correlated_dict = {}

    # Identify pairs of correlated features
    for i in range(results.shape[0]):
        for j in range(i + 1, results.shape[1]):
            if results[i, j] > threshold:
                feature_i = headers[i]
                feature_j = headers[j]

                # Add to the correlated features dictionary
                if feature_i not in correlated_dict:
                    correlated_dict[feature_i] = []
                correlated_dict[feature_i].append(feature_j)

                if feature_j not in correlated_dict:
                    correlated_dict[feature_j] = []
                correlated_dict[feature_j].append(feature_i)

    return correlated_dict

def select_redundant_features(correlated_dict):
    """
    Selects features to remove based on correlation while keeping one representative from each correlated pair.

    Args:
        correlated_dict: Dictionary where keys are feature names and values are lists of correlated features

    Returns:
        list: List of redundant features to remove
    """

    features_to_remove = set()
    processed_features = set()

    for feature, correlated in correlated_dict.items():
        if feature not in processed_features:
            
            processed_features.add(feature)

            
            for correlated_feature in correlated:
                if correlated_feature not in processed_features:
                    features_to_remove.add(correlated_feature)
            processed_features.add(feature)

    return list(features_to_remove)

def one_hot_encode_batches(X, headers, masked_headers_categorical, batch_size=1000):
    """
    One-hot encodes the categorical columns in the dataset in batches.

    Args:
        X: NumPy array containing the dataset
        headers: list of the feature headers
        masked_headers_categorical: List of headers for categorical features to encode
        batch_size: Number of rows to process at a time

    Returns:
        encoded_data: the one-hot encoded dataset
    """

    num_rows = X.shape[0] # Number of rows
    unique_values_dict = {} # Initialize dictionary containing unique values

    # Collect unique values for categorical features
    for i, header in enumerate(headers):
        if header in masked_headers_categorical:
            unique_values_dict[i] = set()  # Collect unique values

    for start in range(0, num_rows, batch_size):
        end = min(start + batch_size, num_rows)
        batch = X[start:end]
        
        for i in range(batch.shape[1]):
            if headers[i] in masked_headers_categorical:
                unique_values_dict[i].update(np.unique(batch[:, i]))

    # Convert sets to sorted lists for consistent ordering
    for key in unique_values_dict:
        unique_values_dict[key] = sorted(unique_values_dict[key])

    # One-hot encode based on collected unique values
    processed_data = []
    
    for start in range(0, num_rows, batch_size):
        end = min(start + batch_size, num_rows)
        batch = X[start:end]
        batch_processed_data = []

        for i in range(batch.shape[1]):
            if headers[i] in masked_headers_categorical:
                unique_vals = unique_values_dict[i]
                one_hot_col = np.zeros((batch.shape[0], len(unique_vals)), dtype=int)

                for j, val in enumerate(unique_vals):
                    one_hot_col[:, j] = (batch[:, i] == val).astype(int)

                batch_processed_data.append(one_hot_col)
            else:
                batch_processed_data.append(batch[:, i].reshape(-1, 1).astype(float))

        # Concatenate the processed batch columns and append to the main data
        processed_data.append(np.hstack(batch_processed_data))

    # Concatenate all processed batches into a single array
    encoded_data = np.vstack(processed_data)

    return encoded_data

# ==============================================================================
# SECTION: Model Building
# ------------------------------------------------------------------------------
# Purpose  : This section defines functions that set up, configure, and train
#            the machine learning model for predictive analysis. 
#
# Usage    : Use these functions to construct and initialize models following
#            data preprocessing. Call the primary model training function to
#            fit the model to the preprocessed dataset, then access prediction 
#            and evaluation functions to assess model performance on test data.
# ------------------------------------------------------------------------------
# Function List:
#    - logistic_regression_medical(y_train, tx_train, y_test, tx_test, initial_w, gamma, batch_size=None, lambda_=0.0, patience=5)
#    - logistic_regression_no_early_stopping(y_train, tx_train, initial_w, gamma, batch_size=None, lambda_=0.0, max_iter=5000)
# ==============================================================================

def sigmoid(t):
    """ apply sigmoid function on t
        
        Args: 
            t: scalar or numpy array
        Returns:
            sig: scalar or numpy array
    """

    sig = np.exp(t)/(1 + np.exp(t))
    
    return sig



def logistic_regression_medical(y_train, tx_train, y_test, tx_test, initial_w, gamma, batch_size=None, lambda_=0.0, patience=5):
    """
    Performs logistic regression with mini-batch training and stopping criteria
    
    Args:
        y_train: NumPy array containing target variable
        tx_train: NumPy array containing training features
        y_test: NumPy array containing target variable for testing
        tx_test: NumPy array containing testing features
        initial_w: initial guess for weight vector
        gamma: scalar denoting the step-size
        batch_size: scalar denoting the batch size 
        lambda_: regularization parameter
        patience: early stopping criterion

    Returns:
        w: optimal weights vector
        losses: losses on training data
        test_losses: losses on test data
    """

    N_train = y_train.shape[0] # Number of samples
    w = initial_w # Initial weight vector
    
    losses = [] # Initialize list for training data losses
    test_losses = [] # Initialize list for testing data losses
    n_iter = 0 # Initialize iteration counter
    no_improvement_count = 0  # Initialize no improvement counter
    first_pass = True  # Flag for the first iteration

    while True:
        # Shuffle the training data
        indices = np.arange(N_train)
        np.random.shuffle(indices)
        
        # Mini-batch training
        if batch_size is not None:
            for start_idx in range(0, N_train, batch_size):
                end_idx = min(start_idx + batch_size, N_train)
                batch_indices = indices[start_idx:end_idx]
                
                tx_batch = tx_train[batch_indices]
                y_batch = y_train[batch_indices]
                
                gradient = (1 / len(batch_indices)) * np.dot(tx_batch.T, sigmoid(tx_batch @ w) - y_batch) # Compute gradient for the mini-batch
                gradient += lambda_ * w # Add regularization term (if applicable)
                
                w -= gamma * gradient # Weight vector update
                
        else:
            gradient = (1 / N_train) * np.dot(tx_train.T, sigmoid(tx_train @ w) - y_train) # Compute gradient for entire data set
            gradient += lambda_ * w # Add regularization term (if applicable)

            w -= gamma * gradient # Weight vector update
        
        # Loss calculation on training data
        train_loss = (1 / N_train) * (-np.dot(y_train.T, tx_train @ w) + np.sum(np.log(1 + np.exp(tx_train @ w))))
        losses.append(train_loss)

        # Loss calculation on test data
        test_loss = (1 / y_test.shape[0]) * (-np.dot(y_test.T, tx_test @ w) + np.sum(np.log(1 + np.exp(tx_test @ w))))
        test_losses.append(test_loss)

        # Check for early stopping after the first pass
        if not first_pass:
            if n_iter >= patience:
                if test_loss > test_losses[-2]:  # Compare with previous test loss
                    no_improvement_count += 1
                    print(f"No improvement for {no_improvement_count} iterations.")
                    
                    # Check if we reached the patience limit
                    if no_improvement_count >= patience:
                        print(f"Early stopping at iteration {n_iter}, test loss increased from {test_losses[-2]} to {test_loss}.")
                        break
                else:
                    no_improvement_count = 0  # Reset count if there's improvement
        
        # Set the flag to false after the first iteration
        first_pass = False

        n_iter += 1  # Increment iteration count

        # Check if the maximum number of iterations (5000) has been reached
        if n_iter >= 5000:
            print(f"Reached maximum iterations at {n_iter}. Stopping training.")
            break

    return w, losses, test_losses

def logistic_regression_no_early_stopping(y_train, tx_train, initial_w, gamma, batch_size=None, lambda_=0.0, max_iter=5000):
    """
    Logistic regression function with no early stopping criterion

    Args:
        y_train: NumPy array containing target variable
        tx_train: NumPy array containing training features
        initial_w: initial guess for weight vector
        gamma: scalar denoting the step-size
        batch_size: scalar denoting the batch size 
        lambda_: regularization parameter
        max_iter: scalar denoting maximum number of iterations

    Returns:
        w: optimal weights vector
        losses
    """

    N_train = y_train.shape[0] # Number of samples
    w = initial_w # Initial guess for weight vector

    losses = [] # Initialize list for losses
    n_iter = 0 # Initialize iteration counter

    while n_iter < max_iter:
        indices = np.arange(N_train)
        np.random.shuffle(indices)

        if batch_size is not None:
            for start_idx in range(0, N_train, batch_size):
                end_idx = min(start_idx + batch_size, N_train)
                batch_indices = indices[start_idx:end_idx]

                tx_batch = tx_train[batch_indices]
                y_batch = y_train[batch_indices]

                gradient = (1 / len(batch_indices)) * np.dot(tx_batch.T, sigmoid(tx_batch @ w) - y_batch) # Compute gradient for the mini-batch
                gradient += lambda_ * w # Add regularization term (if applicable)

                w -= gamma * gradient # Weight vector update

        else:
            gradient = (1 / N_train) * np.dot(tx_train.T, sigmoid(tx_train @ w) - y_train) # Compute gradient for entire dataset
            gradient += lambda_ * w # Add regularization term (if applicable)

            w -= gamma * gradient # Weight vector update

        # Loss calculation
        train_loss = (1 / N_train) * (-np.dot(y_train.T, tx_train @ w) + np.sum(np.log(1 + np.exp(tx_train @ w))))
        losses.append(train_loss)

        print(f"Iteration {n_iter}, Train Loss: {train_loss}")

        n_iter += 1  # Increment iteration count

    print(f"Reached maximum iterations at {n_iter}. Stopping training.")

    return w, losses