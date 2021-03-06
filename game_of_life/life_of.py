import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0


# example
def random_grid(N):
    return np.random.choice([OFF, ON], N*N, p=[0.9, 0.1]).reshape(N, N)


def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[OFF, OFF, ON], [ON, OFF, ON],
                       [OFF, ON, ON]])
    grid[i:i + 3, j:j + 3] = glider
    return grid


def update(frame_num, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            count = 0
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if x == 0 and y == 0: continue #don't check our own square

                    if grid[(i+x)%N, (j+y)%N] == ON:
                        count += 1
            if count == 3:
                new_grid[i,j] = ON
            elif count < 2 or count > 3:
                new_grid[i,j] = OFF
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

# main() function
def main():
    # command line argumentss are in sys.argv[1], sys.argv[2], ...
    # sys.argv[0] is the script name and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    # add arguments
    parser.add_argument('--grid-size', dest='N', type=int, default=100, required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', default=50, type=int, required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    N = max(args.N, 9)

    # set animation update interval
    update_interval = max(args.interval, 50)

    # declare grid
    grid = np.array([])

    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(N * N).reshape(N, N)
        add_glider(1, 1, grid)
    else:
        # populate grid with random on/off - more off than on
        grid = random_grid(N)

    # set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                  frames=10,
                                  interval=update_interval,
                                  save_count=50)

    if args.movfile:
        ani.save(args.movfile, fps=60,  extra_args=['-vcodec',  'libx264'])

    plt.show()

if __name__ == '__main__':
    main()
