# Protein Length Explorer

An interactive Streamlit dashboard for visualising the length distribution of protein sequences. Given a precomputed TSV of `(length, count)` pairs it renders an
interactive Plotly histogram with three binning strategies and a logarithmic-scale toggle.

## Features

- **Linear histogram** — fixed-width bins; bin width is adjustable via sidebar slider (10 – 2 000 aa)
- **Logarithmic histogram** — bins spaced evenly on a log scale; number of bins is adjustable (10 – 100)
- **Focused view (5 – 1 000 aa)** — zoomed-in linear histogram for the short-protein region; fine-grained bin width slider (1 – 50 aa)
- **Log-scale Y axis** — optional toggle to handle the wide dynamic range typical of proteome-scale data
- Fully interactive charts (pan, zoom, hover tooltips) powered by Plotly

## Requirements

| Package | Minimum version |

| Python  | 3.9            |
| streamlit | 1.30        |
| pandas  | 2.0            |
| plotly  | 5.0            |
| numpy   | 1.24           |

## Installation

```bash
# 1. Clone the repository
git clone https://github.com//.git
cd 

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

