import matplotlib.pyplot as plt
import numpy as np

import constants as C
import utils


PLOT_CONFIG = [
    ("d_A", "$dA$", "Amplitude Difference"),
    ("d_phi", "$d\\phi$", "Phase Difference"),
    ("d_phi_R", "$d\\phi_R$", "Residual Phase Difference"),
]

OAT_PARAMS = {
    "total_mass": [
        ("mass_ratio", "Mass Ratio"),
        ("spin1z", "$s_{1z}$"),
        ("spin2z", "$s_{2z}$"),
    ],
    "mass_ratio": [
        ("total_mass", "Total Mass"),
        ("spin1z", "$s_{1z}$"),
        ("spin2z", "$s_{2z}$"),
    ],
    "chi_eff": [
        ("total_mass", "Total Mass"),
        ("mass_ratio", "Mass Ratio"),
    ],
}


def generate_oat_curve(
    sweep_name, sweep_val, oat_name, oat_val, percentiles, wfm_a, wfm_b
):
    if sweep_name == "total_mass":
        total_mass = sweep_val
        if oat_name == "mass_ratio":
            mass_ratio = oat_val
        else:
            mass_ratio = percentiles["mass_ratio_p50"]
        mass1 = total_mass / (1.0 + mass_ratio)
        mass2 = total_mass * mass_ratio / (1.0 + mass_ratio)
        if oat_name == "spin1z":
            spin1z = oat_val
        else:
            spin1z = percentiles["spin1z_p50"]
        if oat_name == "spin2z":
            spin2z = oat_val
        else:
            spin2z = percentiles["spin2z_p50"]

    elif sweep_name == "mass_ratio":
        mass_ratio = sweep_val
        if oat_name == "total_mass":
            total_mass = oat_val
        else:
            total_mass = percentiles["total_mass_p50"]
        mass1 = total_mass / (1.0 + mass_ratio)
        mass2 = total_mass * mass_ratio / (1.0 + mass_ratio)
        if oat_name == "spin1z":
            spin1z = oat_val
        else:
            spin1z = percentiles["spin1z_p50"]
        if oat_name == "spin2z":
            spin2z = oat_val
        else:
            spin2z = percentiles["spin2z_p50"]

    elif sweep_name == "chi_eff":
        spin1z = sweep_val
        spin2z = sweep_val
        if oat_name == "total_mass":
            oat_total_mass = oat_val
        else:
            oat_total_mass = percentiles["mass1_p50"] + percentiles["mass2_p50"]
        if oat_name == "mass_ratio":
            mass_ratio = oat_val
        else:
            mass_ratio = percentiles["mass2_p50"] / percentiles["mass1_p50"]
        mass1 = oat_total_mass / (1.0 + mass_ratio)
        mass2 = oat_total_mass * mass_ratio / (1.0 + mass_ratio)
        total_mass = mass1 + mass2

    parameter = {
        "mass_1": mass1,
        "mass_2": mass2,
        "luminosity_distance": percentiles["distance_p50"],
        "iota": percentiles["inclination_p50"],
        "spin_1x": 0,
        "spin_1y": 0,
        "spin_1z": spin1z,
        "spin_2x": 0,
        "spin_2y": 0,
        "spin_2z": spin2z,
    }

    waveforms, h1, h2, _, _, _, _, _, _, _ = utils.generate_waveform(
        parameter, wfm_a, wfm_b
    )

    characteristics = utils.compute_characteristics(
        h1, h2, waveforms, wfm_a, total_mass
    )

    return characteristics


def run_oat_sweep(sweep_values, sweep_name, sweep_label, percentiles, wfm_a, wfm_b):
    oat_params = OAT_PARAMS[sweep_name]
    pair_tag = f"{wfm_a}_vs_{wfm_b}"

    all_sweep_results = []

    for sweep_val in sweep_values:
        per_param_curves = {}

        for oat_name, oat_label in oat_params:
            oat_low = percentiles[f"{oat_name}_p16"]
            oat_high = percentiles[f"{oat_name}_p84"]
            oat_values = np.linspace(oat_low, oat_high, C.OAT_RESOLUTION)

            param_curves = []
            for oat_val in oat_values:
                curve = generate_oat_curve(
                    sweep_name, sweep_val, oat_name, oat_val, percentiles, wfm_a, wfm_b
                )
                param_curves.append(curve)

            per_param_curves[oat_name] = param_curves

        all_sweep_results.append(
            {
                "sweep_val": sweep_val,
                "per_param_curves": per_param_curves,
            }
        )

    for data_key, y_label, title in PLOT_CONFIG:
        utils.init_plot()

        for result in all_sweep_results:
            sweep_val = result["sweep_val"]

            all_y = []
            for oat_name, oat_label in oat_params:
                for curve in result["per_param_curves"][oat_name]:
                    curve_freqs = np.array(curve["freqs"])
                    curve_y = np.array(curve[data_key])
                    y_interp = np.interp(
                        C.F_GRID, curve_freqs, curve_y, left=np.nan, right=np.nan
                    )
                    all_y.append(y_interp)

            all_y = np.stack(all_y, axis=0)
            env_min = np.nanmin(all_y, axis=0)
            env_max = np.nanmax(all_y, axis=0)

            plt.fill_between(
                C.F_GRID, env_min, env_max, alpha=C.ALPHA, label=f"{sweep_val}"
            )

        plt.title(f"{title} OAT by varying {sweep_label}")
        plt.ylabel(y_label)
        plt.xlabel("Frequency (Hz)")
        plt.xlim(C.F_LOWER, C.F_HIGHER)
        plt.legend()
        plt.savefig(f"../out/oat/{pair_tag}_oat_{sweep_name}_{data_key}_main.png")
        plt.show()

    for result in all_sweep_results:
        sweep_val = result["sweep_val"]

        for data_key, y_label, title in PLOT_CONFIG:
            utils.init_plot()

            for oat_name, oat_label in oat_params:
                param_y = []
                for curve in result["per_param_curves"][oat_name]:
                    curve_freqs = np.array(curve["freqs"])
                    curve_y = np.array(curve[data_key])
                    y_interp = np.interp(
                        C.F_GRID, curve_freqs, curve_y, left=np.nan, right=np.nan
                    )
                    param_y.append(y_interp)

                param_y_stacked = np.stack(param_y, axis=0)
                param_min = np.nanmin(param_y_stacked, axis=0)
                param_max = np.nanmax(param_y_stacked, axis=0)

                plt.fill_between(
                    C.F_GRID,
                    param_min,
                    param_max,
                    alpha=C.ALPHA,
                    label=oat_label,
                )

            plt.title(f"{title} OAT at {sweep_label} = {sweep_val}")
            plt.ylabel(y_label)
            plt.xlabel("Frequency (Hz)")
            plt.xlim(C.F_LOWER, C.F_HIGHER)
            plt.legend()
            plt.savefig(
                f"../out/oat/{pair_tag}_{sweep_name}_{data_key}_{sweep_val}.png"
            )
            plt.show()


def run(percentiles):
    for wfm_a, wfm_b in C.MODEL_PAIRS:
        run_oat_sweep(
            C.VARY_TOTAL_MASS,
            "total_mass",
            "Total Mass",
            percentiles,
            wfm_a,
            wfm_b,
        )

        run_oat_sweep(
            C.VARY_MASS_RATIO,
            "mass_ratio",
            "Mass Ratio",
            percentiles,
            wfm_a,
            wfm_b,
        )

        run_oat_sweep(
            C.VARY_CHI_EFF,
            "chi_eff",
            "Effective Spin",
            percentiles,
            wfm_a,
            wfm_b,
        )
