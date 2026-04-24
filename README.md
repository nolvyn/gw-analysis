# gw-analysis

Code to analyze and quantify differences between gravitational waveform models across events in GWTC-2.1, GWTC-3, and GWTC-4.

This project makes extensive use of PyCBC to generate and compare waveforms using posterior samples from LIGO/Virgo/KAGRA catalogs. The main outputs are plots characterizing amplitude differences, phase differences, and mismatches between model pairs across frequency and parameter space.

---

## Requirements

- Python 3.11 - 3.13 (It is not required to download Python separately when using uv)
- [uv](https://docs.astral.sh/uv/) (recommended)
- Git

> **Alternative:** If you'd rather use conda/mamba, IGWN maintains an official conda environment that includes LALSuite, PyCBC, and most dependencies. See the [IGWN conda guide](https://computing.docs.ligo.org/conda/) for setup instructions.

---

## Installing uv

Pick the installation that matches your operating system.

### Linux

Official
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Specific distributions and package managers

```bash
# Debian/Ubuntu
apt install uv

# Fedora/RHEL
dnf install uv

# Arch
pacman -S uv

# NixOS
Add pkgs.uv to your environment.systemPackages
```
> **NixOS Note:** You may need to set **programs.nix-ld.enable = true;** for uv to work.

### macOS

Official
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Homebrew
```bash
brew install uv
```

### Windows

Official
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Winget
```bash
winget install --id=astral-sh.uv  -e
```

---

## Cloning and Setting Up

```bash
git clone https://github.com/nolvyn/gw-analysis.git
cd gw-analysis
uv sync
```

---

## Downloading Data

Two sets of data are required, the posterior samples from the GWTC catalogs, and the waveform model files. Ensure you have enough storage as the waveform model files and posterior sample files take up ~77 gigabytes.

> **Note:** Both scripts use Zenodo and can take a while due to rate limiting. You might need to run them more than once if downloads get cut off.

### Event Data (Posterior Samples)

```bash
bash ~/gw-analysis/scripts/event-setup.sh
```

This downloads the posterior sample files for GWTC-2.1, GWTC-3, and GWTC-4 into `data/events/`.

Alternatively, you can grab them manually from [GWOSC](https://gwosc.org/eventapi/html/GWTC/).

### Waveform Model Files

```bash
bash ~/gw-analysis/scripts/model-setup.sh
```

This downloads the waveform data files needed for SEOBNR and NR models into `data/models/`.

Alternatively, you can grab them manually from:
- https://git.ligo.org/lscsoft/lalsuite-extra
- https://git.ligo.org/waveforms/software/lalsuite-waveform-data

> **Windows Note:** The setup scripts above are bash scripts so you need WSL or Git Bash to run them. Alternatively, you can download the files manually from the links above and drop them in `data/events/` and `data/models/`.

---

## Running the Analysis

Edit `src/constants.py` to configure which model pairs to compare, how many posterior samples to draw per event, and which plots to generate.

To run this code, one can either use the included jupyter notebook or run the following commands:

```bash
cd ~/gw-analysis/src
uv run python main.py
```

Output plots go to `out/spread/`, `out/vary/`, and `out/mismatch/` depending on which analyses you have enabled in constants.

---

## Troubleshooting

**`LAL_DATA_PATH/XLAL` Errors**: Make sure the waveform model files are actually in `data/models/` and that you are running this code from either the accompanied jupyter notebook, or using `uv run` from the `src` directory.

**Zenodo downloads keep failing**: Keep running the scripts as Zenodo will not redownload what it has already downloaded. Or obtain the files manually from the links above.
