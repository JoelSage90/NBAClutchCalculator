# 🏀 NBA Clutch Calculator
NBA Clutch Calculator is a Streamlit web app that evaluates and compares NBA players' clutch performance based on shot data. The app provides intuitive visualizations—heatmaps and gauges—allowing users to compare two players side-by-side. Deployed at: nbaclutchcalculator.streamlit.app

## 🚀 Live Demo
Visit the app live:

 ▶️ nbaclutchcalculator.streamlit.app

## 📋 Features
**Player Selection:** Select any one/two NBA players to compare.

**Clutch Heatmap:** Visualize shot performance under clutch situations.

**Clutchness Gauge:** Quantitative gauge (0–100 scale) reflecting clutch ability.

**Overall Stats:** Displays overall field goal percentage (FGP) and best-performing court section.

**Side-by-Side Comparison:** View both players in parallel to assess performance differences.

## 📁 Project Structure

```text
NBAClutchCalculator/
├── data/                  # Cached clutch shot data (CSV files)
├── src/
│   ├── collect_data.py    # NBA API data fetcher
│   ├── shot_plot.py       # Heatmap generator
│   ├── clutch_score.py    # Clutch metric calculator
│   ├── Clutchness.py      # Shared utilities
│   └── pages/
│       └── compare_players.py  # Comparison interface
├── streamlit_app.py       # Main application entry
└── requirements.txt       # Python dependencies
```
## 🧩 Installation & Running Locally
**Prerequisites:**

Python 3.8+

**Install dependencies:**
```bash
git clone https://github.com/JoelSage90/NBAClutchCalculator.git
cd NBAClutchCalculator
pip install -r requirements.txt
```
**Run the app:**
```bash
streamlit run streamlit_app.py
```
📷 Screenshots
Web App Interface

Side-by-Side Player Comparison

## 🧪 Model Evaluation
The clutchness metric was tested against historical data to assess reliability. Below are examples of model output for key players:

Example Evaluation Outputs


🎓 Authors & Acknowledgments
Created by Joel Sage. Based on publicly available NBA statistics. Special thanks to the Streamlit and streamviz teams for building interactive components and layout utilities.
