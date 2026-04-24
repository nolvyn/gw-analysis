import warnings
import os
import sys

import constants as C
import gwtc
import utils

warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")
warnings.filterwarnings("ignore", "pkg_resources is deprecated as an API")


sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))

# Set up proper LAL Data Path (Needed for accessing SEOBNR and NR files)
os.environ["LAL_DATA_PATH"] = os.path.expanduser("~/gw-analysis/data/models")

# Main Stuff
waveform_data = {}

for event in gwtc.ALL_EVENTS:
    samples = utils.get_parameters(event)

    for wfm_a, wfm_b in C.MODEL_PAIRS:
        label = f"{event} {wfm_a} vs {wfm_b}"
        waveform_data[label] = []

        for parameter in samples:
            (
                waveforms,
                h1,
                h2,
                mass_ratio,
                total_mass,
                spin1z,
                spin2z,
                chi_eff,
                distance,
                inclination,
            ) = utils.generate_waveform(parameter, wfm_a, wfm_b)

            characteristics = utils.compute_characteristics(
                h1, h2, waveforms, wfm_a, total_mass
            )

            waveform_data[label].append(
                {
                    "spin1z": spin1z,
                    "spin2z": spin2z,
                    "distance": distance,
                    "inclination": inclination,
                    "freqs": characteristics["freqs"],
                    "amp": characteristics["amp"],
                    "d_A": characteristics["d_A"],
                    "d_phi": characteristics["d_phi"],
                    "d_phi_R": characteristics["d_phi_R"],
                    "freqs_dimless": characteristics["freqs_dimless"],
                    "mass_ratio": mass_ratio,
                    "total_mass": total_mass,
                    "chi_eff": chi_eff,
                    "mismatch": characteristics["mismatch"],
                }
            )

if C.RUN_SPREAD_PLOTS:
    import spread_plots

    spread_plots.run(waveform_data)

if C.RUN_SPREAD_PARAM_PLOTS:
    import spread_param_plots

    spread_param_plots.run(waveform_data)

if C.RUN_MISMATCH_PLOTS:
    import mismatch_plots

    mismatch_plots.run(waveform_data)

if C.RUN_VARY_PLOTS:
    import vary_param_plots

    percentiles = utils.collect_percentiles(gwtc.ALL_EVENTS)
    vary_param_plots.run(percentiles)

if C.RUN_OAT_PLOTS:
    import oat_plots

    percentiles = utils.collect_percentiles(gwtc.ALL_EVENTS)
    oat_plots.run(percentiles)
