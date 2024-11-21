import numpy as np

def weighted_ellipse(points, weights):
    """
    Calculate the weighted standard deviational ellipse for a set of points.

    Parameters
    ----------
    points : arraylike
             (n,2), (x,y) coordinates of a series of event points.
    weights : arraylike
              (n,) weights corresponding to each point.
    
    Returns
    -------
    semi_major : float
                 semi-major axis of the ellipse.
    semi_minor : float
                 semi-minor axis of the ellipse.
    theta      : float
                 clockwise rotation angle of the ellipse in radians.
    """
    points = np.asarray(points)
    weights = np.asarray(weights)

    # Calculate the weighted mean (center of the ellipse)
    weighted_mean_x = np.sum(weights * points[:, 0]) / np.sum(weights)
    weighted_mean_y = np.sum(weights * points[:, 1]) / np.sum(weights)

    # Centralize the points (subtract weighted mean)
    centered_points = points - np.array([weighted_mean_x, weighted_mean_y])

    # Calculate weighted covariance matrix
    cov_matrix = np.cov(centered_points.T, aweights=weights)

    # Calculate the eigenvalues and eigenvectors of the covariance matrix
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # Semi-major and semi-minor axes are the square roots of the eigenvalues
    semi_major = np.sqrt(np.max(eigenvalues))
    semi_minor = np.sqrt(np.min(eigenvalues))

    # The rotation angle of the ellipse is the angle of the eigenvector corresponding to the largest eigenvalue
    theta = np.arctan2(eigenvectors[1, np.argmax(eigenvalues)], eigenvectors[0, np.argmax(eigenvalues)])

    return semi_major, semi_minor, theta

# Example usage
points = np.array([
    [1, 1],
    [2, 2],
    [3, 3],
    [4, 5],
    [5, 5]
])

weights = np.array([1, 2, 1, 1, 2])  # Example weights

semi_major, semi_minor, theta = weighted_ellipse(points, weights)

print(f"Semi-major axis: {semi_major}")
print(f"Semi-minor axis: {semi_minor}")
print(f"Rotation angle (radians): {theta}")
print(f"Rotation angle (degrees): {np.degrees(theta)}")
