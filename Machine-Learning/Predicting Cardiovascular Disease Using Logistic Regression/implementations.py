# CS-433 Machine Learning
# Project 1 - Model for predicting MICHD

# Group Pandas
    # Ali Elkilesly - 345334
    # Selim Sherif - 346035
    # Roy Turk - 345573

# "implementations.py"
# Python script containing all required functions

# Header declaration
import numpy as np

# ==============================================================================
# Function List:
#    - sigmoid(t)
#    - mean_squared_error_gd(y, tx, initial_w, max_iters, gamma)
#    - mean_squared_error_sgd(y, tx, initial_w, max_iters, gamma)
#    - least_squares(y, tx)
#    - ridge_regression(y, tx, lambda_)
#    - logistic_regression(y, tx, initial_w, max_iters, gamma)
#    - reg_logistic_regression(y, tx, lambda_, initial_w, max_iters, gamma)
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

def mean_squared_error_gd(y, tx, initial_w, max_iters, gamma):
    """ the gradient descent (GD) algorithm

        Args: 
            y: numpy array of shape (N, )
            tx: numpy array of shape (N, D)
            initial_w: numpy array of shape (D, ) 
            max_iters: scalar denoting the maximum number of iterations
            gamma: scalar denoting the step-size

        Returns:
            w: numpy array of shape (D, )
            loss: scalar denoting the final loss value
    """

    N = y.shape[0] # number of samples
    w = initial_w # initial weight vector
    
    if max_iters == 0:
        return w, 1/(2*N) * np.sum((y - tx @ w)**2)

    for n_iter in range(max_iters):

        gradient = (-1/N) * np.dot(tx.T, y - tx @ w) # gradient of the MSE loss function

        w = w - gamma * gradient # weight vector update
        loss = 1/(2*N) * np.sum((y - tx @ w)**2) # MSE loss function

    return w, loss

def mean_squared_error_sgd(y, tx, initial_w, max_iters, gamma):
    """ the stochastic gradient descent (SGD) algorithm 

        Args: 
            y: numpy array of shape (N, )
            tx: numpy array of shape (N, D)
            initial_w: numpy array of shape (D, ) 
            max_iters: scalar denoting the maximum number of iterations
            gamma: scalar denoting the step-size

        Returns:
            w: numpy array of shape (D, )
            loss: scalar denoting the final loss value
    """

    N = y.shape[0] # number of samples
    w = initial_w # initial weight vector

    for n_iter in range(max_iters):

        batch_index = np.random.randint(N)
        y_batch = y[batch_index:batch_index + 1]  # numpy array of shape (1, )
        tx_batch = tx[batch_index:batch_index + 1]  # numpy array of shape (1, D)

        gradient = - np.dot(tx_batch.T, y_batch - tx_batch@w) # gradient

        w = w - gamma * gradient # weight vector update

    loss = 1 / (2 * N) * np.sum((y - tx @ w) ** 2)  # MSE loss function over entire dataset

    return w, loss

def least_squares(y, tx):
    """ least squares solution

        Args:
            y: numpy array of shape (N, )
            tx: numpy array of shape (N, D)
        
        Returns:
            w: numpy array of shape (D, )
            loss: scalar denoting the loss value
    """

    N = y.shape[0] # number of samples

    gram_matrix = np.dot(tx.T, tx) # Gram matrix

    w = np.linalg.solve(gram_matrix, np.dot(tx.T, y)) # weight vector
    loss = 1/(2*N) * np.sum((y - tx @ w)**2) # MSE loss function

    return w, loss

def ridge_regression(y, tx, lambda_):
    """ ridge regression using normal equations

        Args:
            y: numpy array of shape (N, )
            tx: numpy array of shape (N, D)
            lambda_: scalar
        
        Returns:
            w: numpy array of shape (D, )
            loss: scalar denoting the loss value
    """

    N, D = tx.shape # number of samples and features

    lambda_eye = 2 * lambda_ * N * np.eye(D) # scaled identity matrix
    gram_matrix = np.dot(tx.T, tx) # Gram matrix

    w = np.linalg.solve((gram_matrix + lambda_eye), np.dot(tx.T, y)) # weight vector
    loss = 1/(2*N) * np.sum((y - tx @ w)**2) # MSE loss function

    return w, loss

def logistic_regression(y, tx, initial_w, max_iters, gamma):
    """ logistic regression using gradient descent (GD) algorithm

        Args: 
            y: numpy array of shape (N, )
            tx: numpy array of shape (N, D)
            initial_w: numpy array of shape (D, ) 
            max_iters: scalar denoting the maximum number of iterations
            gamma: scalar denoting the step-size

        Returns:
            w: numpy array of shape (D, )
            loss: scalar denoting the final loss value
    """

    N = y.shape[0] # number of samples
    w = initial_w # initial weight vector
    
    if max_iters == 0:
        return w, (1 / N) * np.sum(- y * (tx @ w) + np.log(1 + np.exp(tx @ w)))

    for n_iter in range(max_iters):

        gradient = (1 / N) * np.dot(tx.T, sigmoid(tx @ w) - y) # gradient of loss function
        
        w = w - gamma * gradient # weight vector update
        loss = (1 / N) * np.sum(- y * (tx @ w) + np.log(1 + np.exp(tx @ w))) # loss function
    
    return w, loss

def reg_logistic_regression(y, tx, lambda_, initial_w, max_iters, gamma):
    """ regularized logistic regression using gradient descent (GD) algorithm

        Args: 
            y: numpy array of shape (N, )
            tx: numpy array of shape (N, D)
            lambda_: scalar
            initial_w: numpy array of shape (D, ) 
            max_iters: scalar denoting the maximum number of iterations
            gamma: scalar denoting the step-size

        Returns:
            w: numpy array of shape (D, )
            loss: scalar denoting the final loss value
    """

    N = y.shape[0] # number of samples
    w = initial_w # initial weight vector

    if max_iters == 0:
        return w, (1 / N) * np.sum(- y * (tx @ w) + np.log(1 + np.exp(tx @ w)))

    for n_iter in range(max_iters):

        gradient = (1 / N) * np.dot(tx.T, sigmoid(tx @ w) - y) + 2 * lambda_ * w # gradient of loss function
        
        w = w - gamma * gradient # weight vector update
        loss = (1 / N) * np.sum(- y * (tx @ w) + np.log(1 + np.exp(tx @ w))) # loss function

    return w, loss



