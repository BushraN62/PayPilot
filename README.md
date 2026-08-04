# PayPilot

## Authors
- Zayba Syed
- Bushra Naveed

---

## Project Description

PayPilot is a Python web application built with Flask that helps prospective college students evaluate the financial value of higher education. Using live data from the U.S. Department of Education College Scorecard API, the application allows users to search for colleges and compare metrics such as tuition, graduation rates, median earnings after graduation, and average student debt. Users can filter colleges by state, school type, major, degree level, and financial preferences to find schools that best match their goals. The application will calculate a Return on Investment (ROI) score to help users compare the long-term financial value of different colleges and programs. Interactive charts and visualizations will make it easier to analyze salary outcomes and educational costs before making college decisions.

---

## Project Outline / Plan

The project will include the following components:

- Build a Flask web interface with multiple pages
- Connect to the College Scorecard API
- Retrieve college information based on user-selected filters
- Store retrieved data locally for faster access
- Display college statistics in an organized table
- Calculate an ROI score using salary, tuition, and debt information
- Create interactive charts comparing earnings, tuition, and debt
- Test and document the application

---

## Interface Plan

The application will feature a user-friendly Flask web interface where users can search for colleges using filters such as state, major, school type, degree level, minimum median earnings, maximum student debt, and maximum tuition. Search results will display important information including tuition, graduation rate, median earnings after graduation, average student debt, acceptance rate, and the calculated ROI score. Users will also be able to view charts and graphs that compare colleges based on salary outcomes and educational costs.

---

## Data Collection and Storage Plan

### Author #1: Zayba Syed

The application will collect data from the U.S. Department of Education College Scorecard API. Information including college names, tuition costs, graduation rates, student debt, median earnings after graduation, acceptance rates, and degree information will be retrieved through API requests. The collected data will be cleaned and stored locally using CSV files or an SQLite database to improve performance and reduce unnecessary API requests. Author #1 will also develop the Flask web interface and integrate it with the data collection and storage components.

---

## Data Analysis and Visualization Plan

### Author #2: Bushra Naveed

The collected data will be analyzed using Python and the Pandas library to compare colleges based on earnings, debt, tuition, and graduation rates. An ROI score will be calculated to estimate the financial value of attending each college. The application will generate visualizations such as bar charts, scatter plots, and histograms using Plotly or Matplotlib to help users compare schools and identify trends in salary outcomes and educational costs. These visualizations will be integrated into the web interface for users to explore.


---

## Installation & Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd PayPilot
```

### 2. (Optional) Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

In the project root, create a file named `.env` containing your College Scorecard API key:

```text
COLLEGE_SCORECARD_API_KEY=your_api_key_here
```

### 5. Run the application

```bash
python app.py
```

Flask will display the local URL in the terminal. Open that URL in your web browser (typically `http://127.0.0.1:5000`).

---

## Notes

- The `.env` file is excluded from Git for security and must be created manually.
- The `data/` CSV files are generated automatically the first time the application retrieves data from the College Scorecard API.
- The initial search may take longer while the local data cache is created. Subsequent searches will be significantly faster.