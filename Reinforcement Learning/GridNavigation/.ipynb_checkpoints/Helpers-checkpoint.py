import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def visualize_grid(grid, title="Grid", cmap='gray'):
    """
    Visualizes a binary tensor `grid` with whitespace for zeros and black/grey for ones.

    :param grid: A 2D PyTorch tensor of binary values (0s and 1s).
    :param cmap: Colormap to use (default: 'gray'). Use 'custom' for a custom black/grey colormap.
    :param colorbar: Whether to display a color bar (default: True).
    """
    # Ensure the grid is a 2D tensor
    grid = grid.cpu()
    
    if grid.dim() != 2:
        raise ValueError("Input grid must be a 2D tensor.")

    # Create custom colormap
    cmap = ListedColormap(['white', 'grey'])  # 0 -> white, 1 -> grey

    # Create the plot
    plt.figure(figsize=(5, 5))
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=1)
    plt.title(title)
    
    plt.xticks([])  # Remove x-axis ticks
    plt.yticks([])  # Remove y-axis ticks


    # Show the plot
    plt.show()

def plot_simple(array, title="Values vs Indices", xlabel="Index", ylabel="Value"):
    """
    Plots the values of a 1D array against their indices.

    :param array: A 1D array (list, NumPy array, or PyTorch tensor).
    :param title: Title of the plot (default: "Values vs Indices").
    :param xlabel: Label for the x-axis (default: "Index").
    :param ylabel: Label for the y-axis (default: "Value").
    """
    # Convert the array to a NumPy array if it's a PyTorch tensor
    if hasattr(array, 'numpy'):  # Check if it's a PyTorch tensor
        array = array.numpy()
    elif not isinstance(array, (list, np.ndarray)):  # Ensure it's a list or NumPy array
        raise ValueError("Input must be a list, NumPy array, or PyTorch tensor.")

    # Create the plot
    plt.figure(figsize=(8, 5))  # Set the figure size
    plt.plot(array, marker='o', linestyle='-', color='b')  # Plot the values
    plt.title(title)  # Add a title
    plt.xlabel(xlabel)  # Add an x-axis label
    plt.ylabel(ylabel)  # Add a y-axis label
    plt.grid(True)  # Add a grid for better readability

    # Show the plot
    plt.show()