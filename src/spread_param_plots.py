import matplotlib.pyplot as plt
import numpy as np

import constants
import utils

PLOT_CONFIG = [
    ('d_A',     '$dA$',       'Amplitude Difference',),
    ('d_phi',   '$d\\phi$',   'Phase Difference',),
    ('d_phi_R', '$d\\phi_R$', 'Residual Phase Difference',)
]

BINS_BY_PARAM = {
    'mass_ratio': [
        (0,    0.25,  '0-0.25',   'blue'),
        (0.25, 0.5,   '0.25-0.5', 'red'),
        (0.5,  0.75,  '0.5-0.75', 'green'),
        (0.75, 1.0,   '0.75-1',   'yellow'),
    ],
    'total_mass': [
        (0,   30,    '<30',     'blue'),
        (30,  60,    '30-60',   'red'),
        (60,  100,   '60-100',  'green'),
        (100, 1e6,   '>=100',   'yellow'),
    ],
    'chi_eff': [
        (-1.0, -0.25, '<-0.25',  'blue'),
        (-0.25, 0.0,  '-0.25-0', 'red'),
        (0.0,   0.25, '0-0.25',  'green'),
        (0.25,  1.0,  '>0.25',   'yellow'),
    ],
}

def collect_param_data(grid, x_key, x_label, x_min, x_max, suffix, waveform_data, param_key, bins, file_tag):
    for data_key, y_label, title in PLOT_CONFIG:
        utils.init_plot()

        for low, high, bin_label, color in bins:
            x_values = []
            y_values = []

            for _, dataset in waveform_data.items():
                for point in dataset:
                    val = point[param_key]
                    if low <= val < high:
                        x_values.append(point[x_key])
                        y_values.append(point[data_key])

            if not x_values:
                continue

            interpolated_values = []
            for x_arr, y_arr in zip(x_values, y_values):
                y_grid = np.interp(grid, x_arr, y_arr, left=np.nan, right=np.nan)
                interpolated_values.append(y_grid)

            all_data = np.stack(interpolated_values, axis=0)
            percentile_values = np.nanpercentile(all_data, [16, 50, 84], axis=0)
            one_sigma_low = percentile_values[0]
            median = percentile_values[1]
            one_sigma_high = percentile_values[2]

            plt.plot(grid, median, color = color, label = bin_label)
            plt.fill_between(grid, one_sigma_low, one_sigma_high, color = color, alpha = constants.ALPHA)

        if param_key == 'mass_ratio':
            title_suffix = ' by Mass Ratio'
        elif param_key == 'total_mass':
            title_suffix = ' by Total Mass'
        elif param_key == 'chi_eff':
            title_suffix = ' by Effective Spin'

        plt.title(title + title_suffix)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.xlim(x_min, x_max)
        plt.legend()
        plt.savefig(f"../out/spread/{file_tag}_{data_key}{suffix}.png")
        plt.show()

def run(waveform_data):
    collect_param_data(
        grid = constants.F_GRID,
        x_key = 'freqs',
        x_label = 'Frequency (Hz)',
        x_min = constants.F_LOWER,
        x_max = constants.F_HIGHER,
        suffix = '',
        waveform_data = waveform_data,
        param_key = 'mass_ratio',
        bins = BINS_BY_PARAM['mass_ratio'],
        file_tag = 'spread_bins_massratio',
    )

    collect_param_data(
        grid = constants.F_GRID,
        x_key = 'freqs',
        x_label = 'Frequency (Hz)',
        x_min = constants.F_LOWER,
        x_max = constants.F_HIGHER,
        suffix = '',
        waveform_data = waveform_data,
        param_key = 'total_mass',
        bins = BINS_BY_PARAM['total_mass'],
        file_tag = 'spread_bins_totalmass',
    )

    collect_param_data(
        grid = constants.F_GRID,
        x_key = 'freqs',
        x_label = 'Frequency (Hz)',
        x_min = constants.F_LOWER,
        x_max = constants.F_HIGHER,
        suffix = '',
        waveform_data = waveform_data,
        param_key = 'chi_eff',
        bins = BINS_BY_PARAM['chi_eff'],
        file_tag = 'spread_bins_chieff',
    )

    collect_param_data(
        grid = constants.DF_GRID,
        x_key = 'freqs_dimless',
        x_label = 'Dimensionless Frequency',
        x_min = constants.DF_GRID[0],
        x_max = constants.DF_GRID[-1],
        suffix = '_df',
        waveform_data = waveform_data,
        param_key = 'mass_ratio',
        bins = BINS_BY_PARAM['mass_ratio'],
        file_tag = 'spread_bins_df_massratio',
    )

    collect_param_data(
        grid = constants.DF_GRID,
        x_key = 'freqs_dimless',
        x_label = 'Dimensionless Frequency',
        x_min = constants.DF_GRID[0],
        x_max = constants.DF_GRID[-1],
        suffix = '_df',
        waveform_data = waveform_data,
        param_key = 'total_mass',
        bins = BINS_BY_PARAM['total_mass'],
        file_tag = 'spread_bins_df_totalmass',
    )

    collect_param_data(
        grid = constants.DF_GRID,
        x_key = 'freqs_dimless',
        x_label = 'Dimensionless Frequency',
        x_min = constants.DF_GRID[0],
        x_max = constants.DF_GRID[-1],
        suffix = '_df',
        waveform_data = waveform_data,
        param_key = 'chi_eff',
        bins = BINS_BY_PARAM['chi_eff'],
        file_tag = 'spread_bins_df_chieff',
    )
