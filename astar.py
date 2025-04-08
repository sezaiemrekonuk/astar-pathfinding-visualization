import heapq
import pygame
import math

def h(p1, p2):
    """Calculate the diagonal distance between two points"""
    x1, y1 = p1
    x2, y2 = p2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

def reconstruct_path(came_from, current, draw):
    """Reconstruct the path from end to start"""
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    """A* Pathfinding Algorithm"""
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    
    # Initialize scores for all nodes
    for row in grid:
        for node in row:
            node.g_score = float('inf')
            node.h_score = float('inf')
            node.f_score = float('inf')
    
    start.g_score = 0
    start.h_score = h(start.get_pos(), end.get_pos())
    start.f_score = start.h_score

    open_set_hash = {start}

    while open_set:
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        current = heapq.heappop(open_set)[2]
        if current not in open_set_hash:  # Skip if this node was already processed
            continue
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            # Use the stored cost for this neighbor
            temp_g_score = current.g_score + current.neighbor_costs[neighbor]

            if temp_g_score < neighbor.g_score:
                came_from[neighbor] = current
                neighbor.g_score = temp_g_score
                neighbor.h_score = h(neighbor.get_pos(), end.get_pos())
                neighbor.f_score = neighbor.g_score + neighbor.h_score
                
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (neighbor.f_score, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False 