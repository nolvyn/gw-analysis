import matplotlib.pyplot as plt
import numpy as np

import constants
import utils

PLOT_CONFIG = [
    ('d_A',     '$dA$',       'Amplitude Difference',        'amp_diff_envelope'),
    ('d_phi',   '$d\\phi$',   'Phase Difference',            'phase_diff_envelope'),
    ('d_phi_R', '$d\\phi_R$', 'Residual Phase Difference',   'residual_phase_diff_envelope'),
]

def collect_data(grid, x_key, x_label, x_min, x_max, suffix, waveform_data):
    for data_key, y_label, title, file_base in PLOT_CONFIG:
        x_values = []
        y_values = []

        for _, dataset in waveform_data.items():
            for point in dataset:
                x_values.append(point[x_key])
                y_values.append(point[data_key])

        interpolated_values = []
        for x_point, y_point in zip(x_values, y_values):
            y_grid = np.interp(grid, x_point, y_point, left=np.nan, right=np.nan)
            interpolated_values.append(y_grid)

        all_data = np.stack(interpolated_values, axis=0)

        percentile_values = np.nanpercentile(all_data, [2.5, 16, 50, 84, 97.5], axis=0)
        two_sigma_low = percentile_values[0]
        one_sigma_low = percentile_values[1]
        median = percentile_values[2]
        one_sigma_high = percentile_values[3]
        two_sigma_high = percentile_values[4]

        utils.init_plot()
        plt.plot(grid, median, label='Median')
        plt.fill_between(grid, one_sigma_low, one_sigma_high, alpha=0.75, label='1-$\\sigma$')
        plt.fill_between(grid, two_sigma_low, two_sigma_high, alpha=0.25, label='2-$\\sigma$')

        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.xlim(x_min, x_max)
        plt.legend()
        plt.savefig(f"../out/spread/{file_base}{suffix}.png")
        plt.show()

def run(waveform_data):
    collect_data(
        grid = constants.F_GRID,
        x_key = 'freqs',
        x_label = 'Frequency (Hz)',
        x_min = constants.F_LOWER,
        x_max = constants.F_HIGHER,
        suffix = '',
        waveform_data = waveform_data,
    )

    collect_data(
        grid = constants.DF_GRID,
        x_key = 'freqs_dimless',
        x_label = 'Dimensionless Frequency',
        x_min = constants.DF_GRID[0],
        x_max = constants.DF_GRID[-1],
        suffix = '_df',
        waveform_data = waveform_data,
    )
