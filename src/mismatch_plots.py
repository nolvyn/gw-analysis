import matplotlib.pyplot as plt
import numpy as np

import utils

def collect_mismatches(waveform_data):
    mismatches = []
    for dataset in waveform_data.values():
        for point in dataset:
            mismatches.append(point['mismatch'])
    return mismatches

def run(waveform_data):
    mismatches = collect_mismatches(waveform_data)

    utils.init_plot()
    plt.hist(mismatches, bins=100)
    plt.xlabel('Mismatch')
    plt.ylabel('Count')
    plt.title('Mismatch Histogram')
    plt.savefig("../outputs/mismatch/mismatch_histogram.png")
    plt.show()

    utils.init_plot()
    plt.hist(mismatches, bins=100)
    plt.xscale('log')
    plt.xlabel('Mismatch')
    plt.ylabel('Count')
    plt.title('Mismatch Histogram')
    plt.savefig("../outputs/mismatch/mismatch_histogram_logx.png")
    plt.show()
