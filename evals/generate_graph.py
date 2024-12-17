from matplotlib import pyplot as plt

from run_astar_testing import data_collect as astar_data
from run_hamilton_testing import data_collect as hamilton_data
from run_hybrid_testing import data_collect as our_data

if __name__ == '__main__':
    all_hamilton_tracks = hamilton_data()
    all_astar_tracks = astar_data()
    all_our_tracks = our_data()

    avgs = all_astar_tracks.avg_track()
    plt.plot(list(range(len(avgs))), avgs, label = 'A*')

    avgs = all_hamilton_tracks.avg_track()
    plt.plot(list(range(len(avgs))), avgs, label = 'Hamiltonian')

    avgs = all_our_tracks.avg_track()
    plt.plot(list(range(len(avgs))), avgs, label = 'Hybrid')

    plt.legend()
    plt.title('Average Snake Length Trials in 6x6 Grid')

    plt.xlabel('Game Step')
    plt.ylabel('Average Length')

    plt.show()


    # plt.hist(all_tracks.max_lengths())
    # plt.title('Histogram of Snake Lengths over A* Trials at Game completion in 6x6 Grid')
    # plt.show()