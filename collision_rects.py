# Loading json file
import json
from constants import *

def group_horizontal_blocks(json_data, block_size):
    """
    Groups horizontal blocks into rectangles based on their x and y coordinates.
    Blocks that are not adjacent horizontally form separate rectangles.
    """
    # Extract only the coordinates and sort by row (y), then by column (x)
    wall_blocks = [block[0] for block in json_data]
    wall_blocks.sort(key=lambda coord: (coord[1], coord[0]))

    grouped_rectangles = []
    current_row = []
    current_y = None

    for block in wall_blocks:
        x, y = block

        # If we're on a new row, finalize the current row and start a new one
        if current_y is not None and y != current_y:
            if current_row:
                grouped_rectangles.append({
                    "x": current_row[0][0] * block_size,
                    "y": current_y * block_size,
                    "width": len(current_row) * block_size,
                    "height": block_size
                })
            current_row = []

        # Check if the block is adjacent to the previous one in the same row
        if current_row and x != current_row[-1][0] + 1:
            # Finalize the current rectangle and start a new one
            grouped_rectangles.append({
                "x": current_row[0][0] * block_size,
                "y": current_y * block_size,
                "width": len(current_row) * block_size,
                "height": block_size
            })
            current_row = []

        # Add the block to the current row
        current_row.append(block)
        current_y = y

    # Finalize the last row
    if current_row:
        grouped_rectangles.append({
            "x": current_row[0][0] * block_size,
            "y": current_y * block_size,
            "width": len(current_row) * block_size,
            "height": block_size
        })

    return grouped_rectangles



def merge_vertical_rectangles(rectangles):
    """
    Merges vertically adjacent rectangles that share the same x and width.
    """
    # Sort rectangles by x, then by y
    rectangles.sort(key=lambda rect: (rect['x'], rect['y']))

    merged_rectangles = []
    current_rect = None

    for rect in rectangles:
        if current_rect is None:
            current_rect = rect
        else:
            # Check if the current rectangle can merge with the new one
            if (rect['x'] == current_rect['x'] and 
                rect['width'] == current_rect['width'] and 
                rect['y'] == current_rect['y'] + current_rect['height']):
                # Merge by extending the height
                current_rect['height'] += rect['height']
            else:
                # No merge possible, finalize the current rectangle
                merged_rectangles.append(current_rect)
                current_rect = rect

    # Add the last rectangle
    if current_rect:
        merged_rectangles.append(current_rect)

    return merged_rectangles

