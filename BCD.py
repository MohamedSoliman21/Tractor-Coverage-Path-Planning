import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib
from typing import Tuple, List
import random
from PIL import Image
import sk_dsp_comm.sigsys as ss
import scipy.signal as signal
from IPython.display import Image, SVG
from Graph import *

def x3_func(t):
    """
    Create a piecewise function for plotting x3
    """
    x3 = np.zeros_like(t)
    for k,tk in enumerate(t):
        x3[k] = 1 + tk**2

    return x3

Slice = List[Tuple[int, int]]

def calc_connectivity(slice: np.ndarray) -> Tuple[int, Slice]:
    connectivity = 0
    last_data = 0
    open_part = False
    connective_parts = []
    for i, data in enumerate(slice):
        if last_data == 0 and data == 1:
            open_part = True
            start_point = i
        elif last_data == 1 and data == 0 and open_part:
            open_part = False
            connectivity += 1
            end_point = i
            connective_parts.append((start_point, end_point))
        last_data = data
    return connectivity, connective_parts


def get_adjacency_matrix(parts_left: Slice, parts_right: Slice) -> np.ndarray:
    adjacency_matrix = np.zeros([len(parts_left), len(parts_right)])
    for l, lparts in enumerate(parts_left):
        for r, rparts in enumerate(parts_right):
            if min(lparts[1], rparts[1]) - max(lparts[0], rparts[0]) > 0:
                adjacency_matrix[l, r] = 1
    return adjacency_matrix


def bcd(erode_img: np.ndarray) -> Tuple[np.ndarray, int]:
    assert len(erode_img.shape) == 2
    last_connectivity = 0
    last_connectivity_parts = []
    current_cell = 1
    current_cells = []
    separate_img = np.copy(erode_img)
    
    vertices = []
    vertices_no = 0
    graph = []

    for col in range(erode_img.shape[1]):
        current_slice = erode_img[:, col]
        connectivity, connective_parts = calc_connectivity(current_slice)
        print ('conn: ',connectivity)
        if last_connectivity == 0:
            current_cells = []
            for i in range(connectivity):
                current_cells.append(current_cell)
                add_vertex(current_cell)
                add_edge(current_cell - 1, current_cell, 1)
                current_cell += 1
                
        elif connectivity == 0:
            current_cells = []
            continue
        else:
            adj_matrix = get_adjacency_matrix(last_connectivity_parts, connective_parts)
            new_cells = [0] * len(connective_parts)
            for i in range(adj_matrix.shape[0]):
                if np.sum(adj_matrix[i, :]) == 1:
                    new_cells[np.argwhere(adj_matrix[i, :])[0][0]] = current_cells[i]
                elif np.sum(adj_matrix[i, :]) > 1:
                    for idx in np.argwhere(adj_matrix[i, :]):
                        new_cells[idx[0]] = current_cell
                        add_vertex(current_cell)
                        add_edge(current_cell- 1, current_cell, 1)
                        current_cell = current_cell + 1
                      
            for i in range(adj_matrix.shape[1]):
                if np.sum(adj_matrix[:, i]) > 1:
                    new_cells[i] = current_cell
                    add_vertex(current_cell)
                    add_edge(current_cell- 1, current_cell, 1)
                    current_cell = current_cell + 1
                    
                elif np.sum(adj_matrix[:, i]) == 0:
                    new_cells[i] = current_cell
                    add_vertex(current_cell)
                    add_edge(current_cell - 1, current_cell, 1)
                    current_cell = current_cell + 1
                    
            current_cells = new_cells
            
        for cell, slice in zip(current_cells, connective_parts):
            separate_img[slice[0]:slice[1], col] = cell 
            print(separate_img[slice[0]:slice[1]])
            
        last_connectivity = connectivity
        last_connectivity_parts = connective_parts
    print('Cells: ', current_cell)
    
    return separate_img, current_cell


def display_separate_map(separate_map, cells):
    display_img = np.empty([*separate_map.shape, 3], dtype=np.uint8)
    random_colors = np.random.randint(0, 255, [cells, 3])
    for cell_id in range(1, cells):
        display_img[separate_map == cell_id, :] = random_colors[cell_id, :]
    return display_img 


def Cell_Movement(seperate_map, cells):
    display_img = np.empty([*separate_map.shape, 3], dtype=np.uint8)
    for cell_id in range(1, cells):
        display_img[separate_map == cell_id, :] = random_colors[cell_id, :]
