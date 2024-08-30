import numpy as np
import matplotlib.pyplot as plt

#2a
np.random.seed(0)  # For reproducibility
N = 100
mean = np.array([1, 2])
cov = np.eye(2)  # Identity matrix as covariance

# Generate standard normal random variables
Z = np.random.randn(2, N)

# Transform the data to have the desired mean and covariance
X = cov @ Z + mean.reshape(-1, 1)

#2b
# Plot the original data
plt.figure(figsize=(10, 8))
plt.scatter(X[0, :], X[1, :], marker='.')
plt.title('Original Data')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid(True)
plt.show()

#2c
A = np.array([[0.5, 0], [0, 1]])
X_A = A @ X

#2d
plt.figure(figsize=(10, 8))
plt.scatter(X_A[0, :], X_A[1, :], marker='.')
plt.title('Data after Applying A')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid(True)
plt.show()

#2e
B = np.array([[-1, 0], [0, 1]])
X_BA = B @ X_A

#2f
plt.figure(figsize=(10, 8))
plt.scatter(X_BA[0, :], X_BA[1, :], marker='.')
plt.title('Data after Applying B')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid(True)
plt.show()

#2g
C = np.array([[0, 1], [1, 0]])
X_CBA = C @ X_BA

#2h
plt.figure(figsize=(10, 8))
plt.scatter(X_CBA[0, :], X_CBA[1, :], marker='.')
plt.title('Data after Applying C')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid(True)
plt.show()

#2i
theta = np.radians(45)
D = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
X_DCBA = D @ X_CBA

#2j
plt.figure(figsize=(10, 8))
plt.scatter(X_DCBA[0, :], X_DCBA[1, :], marker='.')
plt.title('Data after Applying D')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid(True)
plt.show()

#2k
E = D @ C @ B @ A
X_E = E @ X

#2l
plt.figure(figsize=(10, 8))
plt.scatter(X_E[0, :], X_E[1, :], marker='.')
plt.title('Data after Applying E')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid(True)
plt.show()

#2m
F = A @ B @ C @ D
X_F = F @ X

#2n
plt.figure(figsize=(10, 8))
plt.scatter(X_F[0, :], X_F[1, :], marker='.')
plt.title('Data after Applying F')
plt.xlabel('X1')
plt.ylabel('X2')
plt.grid(True)
plt.show()

###################################################################################################
#3a and 3b

def load_and_plot_data(filename):
    # Initialize lists to hold the data
    x_coords = []
    y_coords = []
    
    # Read the file
    with open(filename, 'r') as file:
        for line in file:
            # Strip leading/trailing whitespace and split by tabs
            parts = line.strip().split('\t')
            
            # Ensure that there are exactly two values per line
            if len(parts) == 2:
                try:
                    # Convert strings to floats and append to lists
                    x_coords.append(float(parts[0]))
                    y_coords.append(float(parts[1]))
                except ValueError:
                    # Handle any value conversion errors
                    print(f"Warning: Skipping line with invalid data: {line.strip()}")
    
    # Convert lists to numpy arrays and transpose
    X = np.array([x_coords, y_coords])
    
    # Plot the data
    plt.figure(figsize=(8, 6))
    plt.scatter(X[0, :], X[1, :], marker='.')
    plt.title('2D Coordinates from File')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.grid(True)
    plt.show()



load_and_plot_data("handpositions.txt")

#######################################################################################################
#4a)

def load_data(filename):
    x_coords = []
    y_coords = []
    
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                try:
                    x_coords.append(float(parts[0]))
                    y_coords.append(float(parts[1]))
                except ValueError:
                    print(f"Warning: Skipping line with invalid data: {line.strip()}")
    
    return np.array([x_coords, y_coords])


#4b and c
def z_score_standardize(data):
    means = np.mean(data, axis=1, keepdims=True)
    std_devs = np.std(data, axis=1, keepdims=True)
    standardized_data = (data - means) / std_devs
    return standardized_data

def plot_data(data):
    plt.figure(figsize=(8, 6))
    plt.scatter(data[0, :], data[1, :], marker='.')
    plt.title('Standardized 2D Coordinates')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.grid(True)
    plt.show()

# Main workflow
filename = 'handpositions.txt' 
data = load_data(filename)
standardized_data = z_score_standardize(data)
plot_data(standardized_data)
