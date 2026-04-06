import matplotlib.pyplot as plt

import constants as C
import utils


PLOT_CONFIG = [
    ("d_A", "$dA$", "Amplitude Difference"),
    ("d_phi", "$d\\phi$", "Phase Difference"),
    ("d_phi_R", "$d\\phi_R$", "Residual Phase Difference"),
]


def vary_parameter(sweep_values, sweep_name, sweep_label, medians, wfm_a, wfm_b):
    results = []

    for val in sweep_values:
        if sweep_name == "total_mass":
            total_mass = val
            mass_ratio = medians["mass_ratio"]
            mass1 = total_mass / (1.0 + mass_ratio)
            mass2 = total_mass * mass_ratio / (1.0 + mass_ratio)
            spin1z = medians["spin1z"]
            spin2z = medians["spin2z"]
        elif sweep_name == "mass_ratio":
            total_mass = medians["total_mass"]
            mass_ratio = val
            mass1 = total_mass / (1.0 + mass_ratio)
            mass2 = total_mass * mass_ratio / (1.0 + mass_ratio)
            spin1z = medians["spin1z"]
            spin2z = medians["spin2z"]
        elif sweep_name == "chi_eff":
            mass1 = medians["mass1"]
            mass2 = medians["mass2"]
            total_mass = mass1 + mass2
            spin1z = val
            spin2z = val

        parameter = {
            "mass_1": mass1,
            "mass_2": mass2,
            "luminosity_distance": medians["distance"],
            "iota": medians["inclination"],
            "spin_1x": 0,
            "spin_1y": 0,
            "spin_1z": spin1z,
            "spin_2x": 0,
            "spin_2y": 0,
            "spin_2z": spin2z,
        }

        (
            waveforms,
            h1,
            h2,
            _,
            _,
            _,
            _,
            _,
            _,
            _,
        ) = utils.generate_waveform(parameter, wfm_a, wfm_b)

        characteristics = utils.compute_characteristics(
            h1, h2, waveforms, wfm_a, total_mass
        )

        results.append((val, characteristics))

    pair_tag = f"{wfm_a}_vs_{wfm_b}"

    for data_key, y_label, title in PLOT_CONFIG:
        utils.init_plot()

        for val, characteristics in results:
            freqs = characteristics["freqs"]
            y_data = characteristics[data_key]
            plt.plot(freqs, y_data, label=val)

        plt.title(f"{title} by varying {sweep_label}")
        plt.ylabel(y_label)
        plt.xlabel("Frequency (Hz)")
        plt.xlim(C.F_LOWER, C.F_HIGHER)
        plt.legend()
        plt.savefig(f"../out/vary/{pair_tag}_vary_{sweep_name}_{data_key}.png")
        plt.show()


def run(medians):
    for wfm_a, wfm_b in C.MODEL_PAIRS:
        vary_parameter(
            C.VARY_TOTAL_MASS,
            "total_mass",
            "Total Mass",
            medians,
            wfm_a,
            wfm_b,
        )

        vary_parameter(
            C.VARY_MASS_RATIO,
            "mass_ratio",
            "Mass Ratio",
            medians,
            wfm_a,
            wfm_b,
        )

        vary_parameter(
            C.VARY_CHI_EFF,
            "chi_eff",
            "Effective Spin",
            medians,
            wfm_a,
            wfm_b,
        )
