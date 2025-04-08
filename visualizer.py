import pygame
from grid import Grid
from astar import algorithm

def main(win, width):
    ROWS = 20
    grid = Grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        grid.draw(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if started:
                continue

            # Left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                node = grid.grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            # Right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                node = grid.grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    started = True
                    for row in grid.grid:
                        for node in row:
                            node.update_neighbors(grid.grid)

                    # Run the algorithm
                    if not algorithm(lambda: (grid.draw(win), pygame.display.update()), grid.grid, start, end):
                        print("No path found!")
                    
                    started = False

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid.reset()
                    started = False 