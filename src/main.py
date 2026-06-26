import warnings

warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")
warnings.filterwarnings("ignore", "pkg_resources is deprecated as an API")

import os
import sys

for var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ.setdefault(var, "1")

import numpy as np
from joblib import Parallel, delayed

import constants as C
import gwtc
import lal
import utils

lal.swig_redirect_standard_output_error(False)

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))

# Set up proper LAL Data Path (Needed for accessing SEOBNR and NR files)
os.environ["LAL_DATA_PATH"] = os.path.expanduser("~/projects/gw-analysis/data/models")


def process_event(event):
    samples = utils.get_parameters(event)
    waveform_data = {}

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
                    "freqs": np.asarray(characteristics["freqs"], dtype=np.float32),
                    "amp": np.asarray(characteristics["amp"], dtype=np.float32),
                    "d_A": np.asarray(characteristics["d_A"], dtype=np.float32),
                    "d_phi": np.asarray(characteristics["d_phi"], dtype=np.float32),
                    "d_phi_R": np.asarray(characteristics["d_phi_R"], dtype=np.float32),
                    "freqs_dimless": np.asarray(
                        characteristics["freqs_dimless"], dtype=np.float32
                    ),
                    "mass_ratio": mass_ratio,
                    "total_mass": total_mass,
                    "chi_eff": chi_eff,
                    "mismatch": characteristics["mismatch"],
                }
            )

    return waveform_data


sample = utils.get_parameters(gwtc.ALL_EVENTS[0])[0]
for wfm_a, wfm_b in C.MODEL_PAIRS:
    utils.generate_waveform(sample, wfm_a, wfm_b)

waveform_data = {}

for result in Parallel(n_jobs=16, backend="multiprocessing")(
    delayed(process_event)(event) for event in gwtc.ALL_EVENTS
):
    waveform_data.update(result)

if C.RUN_SPREAD_PLOTS:
    import spread_plots

    spread_plots.run(waveform_data)

if C.RUN_SPREAD_PARAM_PLOTS:
    import spread_param_plots

    spread_param_plots.run(waveform_data)

if C.RUN_MISMATCH_PLOTS:
    import mismatch_plots

    mismatch_plots.run(waveform_data)

if C.RUN_VARY_PLOTS or C.RUN_OAT_PLOTS:
    percentiles = utils.collect_percentiles(gwtc.ALL_EVENTS)

if C.RUN_VARY_PLOTS:
    import vary_param_plots

    vary_param_plots.run(percentiles)

if C.RUN_OAT_PLOTS:
    import oat_plots

    oat_plots.run(percentiles)
