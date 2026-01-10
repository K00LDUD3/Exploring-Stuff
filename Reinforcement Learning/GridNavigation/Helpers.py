import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from LogTracker import *

VERSION_FILE = "VersionControl.txt"

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

def plot_path_on_grid(grid, path, episodes):
    """
    Plots the grid and overlays the path taken.

    :param grid: A 2D PyTorch tensor representing the grid (0 = free, 1 = obstacle).
    :param path: A 2D PyTorch tensor of shape (N, 2) representing the path coordinates.
    """
    # Convert the grid and path to NumPy arrays (if they are on CUDA, move them to CPU first)
    if grid.is_cuda:
        grid = grid.cpu()
    if path.is_cuda:
        path = path.cpu()
    grid = grid.numpy()
    path = path.numpy()

    # Create a plot
    plt.figure(figsize=(8, 8))

    # Plot the grid
    cmap = ListedColormap(['white', 'grey'])
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=1)  # 0 = white, 1 = black

    # Overlay the path
    plt.plot(path[:, 1], path[:, 0], marker='o', linestyle='-', color='red')
    plt.xticks([])  # Remove x-axis ticks
    plt.yticks([])  # Remove y-axis ticks
    # Add labels and title
    plt.title("Path on Grid")

    #Saving the plot
    tracker = IntegerTracker(VERSION_FILE)
    version = tracker.read_value()
    plt.savefig(f"Path_plot-v{version}_{grid.shape[0]}x{grid.shape[1]}_eps-{episodes}.png", dpi=300, bbox_inches='tight')
    tracker.increment_value()

    print("Figure Saved..")

    # Show the plot
    plt.show()

    
def plot_rewards(array, title="Rewards Over Episodes", xlabel="Episode", ylabel="Reward Per Episode"):
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

    #Saving the plot
    tracker = IntegerTracker(VERSION_FILE)
    version = tracker.read_value()
    plt.savefig(f"Reward_per_episode-v{version}.png", dpi=300, bbox_inches='tight')
    tracker.increment_value()

    print("Figure Saved..")

    
    # Show the plot
    plt.show()