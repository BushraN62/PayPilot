# PayPilot

## Authors

- **Zayba Syed** : Implemented the Flask web application, API integration, backend development, data collection, local data storage/caching, search and filtering functionality, application testing, and debugging.
- **Bushra Naveed** : Implemented data analysis, ROI calculations, college financial comparisons, data visualizations, and integration of analytical results into the application.

---

## Project Description

PayPilot is a Python web application built with Flask that helps prospective college students evaluate the financial value of higher education. Using data from the U.S. Department of Education College Scorecard API, the application allows users to search for colleges and compare metrics such as tuition, graduation rates, median earnings after graduation, acceptance rates, and average student debt.

Users can filter colleges by state, school type, area of interest, degree level, minimum earnings, maximum student debt, and maximum tuition to find schools that best match their academic and financial goals. The application calculates a Return on Investment (ROI) score to help users compare the potential financial value of different colleges and programs.

PayPilot also provides sorting options, popular searches, college comparison functionality, and financial summary statistics. The ROI Analysis page provides a detailed breakdown of estimated educational cost, student debt, median earnings, estimated ten-year earnings, net return, and ROI. Interactive charts and visualizations make it easier to analyze salary outcomes, educational costs, and student debt before making college decisions.

---

## Project Outline / Implementation

The project was implemented as a Flask-based web application with the following components:

- Built a Flask web interface with Home, How It Works, ROI Explained, and Search Results pages
- Connected the application to the U.S. Department of Education College Scorecard API
- Retrieved college information based on user-selected filters
- Stored retrieved data locally to improve performance and reduce unnecessary API requests
- Displayed college statistics in an organized search results table
- Implemented filtering by state, school type, area of interest, and degree level
- Implemented financial filters for minimum earnings, maximum debt, and maximum tuition
- Implemented college search functionality
- Implemented sorting options for search results
- Implemented popular searches for common student searches
- Calculated an ROI score using tuition, student debt, and median earnings
- Added the ability to select up to 10 schools for ROI comparison
- Created a dedicated ROI Analysis page for detailed college comparisons
- Added ROI rankings for selected schools
- Added estimated total cost, estimated ten-year earnings, and estimated net return calculations
- Added visual comparisons of earnings versus tuition
- Added visual comparisons of debt versus earnings
- Added summary statistics for displayed search results
- Tested and debugged the application to ensure the backend and Flask application run successfully

---

## Interface

The application features a user-friendly Flask web interface where users can search for colleges using filters such as state, school type, area of interest, degree level, minimum median earnings, maximum student debt, and maximum tuition.

The home page allows users to begin a college search and includes popular searches for common combinations such as:

- Computer Science in California
- Nursing in Texas
- Business in Florida

Search results display important information including:

- College name
- State
- Tuition
- Median earnings
- Student debt
- Graduation rate
- Acceptance rate
- ROI score

Users can sort search results by:

- Highest Earnings
- Lowest Tuition
- Lowest Debt
- Highest Acceptance Rate
- Highest ROI

Users can also search through displayed colleges and select up to 10 schools for ROI comparison.

The search results page provides summary statistics, including:

- Average tuition
- Average earnings
- Average student debt

These statistics summarize the colleges currently displayed in the search results.

---

## Data Collection and Storage

### Author #1: Zayba Syed

The application collects data from the U.S. Department of Education College Scorecard API. Information including college names, tuition costs, graduation rates, student debt, median earnings after graduation, acceptance rates, and degree information is retrieved through API requests.

The following functionality was implemented:

- College Scorecard API integration
- API request and response handling
- College data retrieval
- Data processing, cleaning and organization
- Local data storage and caching
- Environment variable support for the API key
- College search functionality
- State filtering
- School type filtering
- Area of interest filtering
- Degree level filtering
- Minimum earnings filtering
- Maximum debt filtering
- Maximum tuition filtering
- Search result sorting
- Popular search functionality
- College selection and comparison workflow
- Flask backend routes
- Integration between backend functionality and the web interface
- Application testing and debugging


---

## Data Analysis and Visualization

### Author #2: Bushra Naveed

The collected data is analyzed using Python and the Pandas library to compare colleges based on earnings, debt, tuition, and other educational outcomes. The application uses these metrics to calculate estimated financial returns and provide meaningful comparisons between schools.

The following functionality was implemented:

- College data processing and cleaning
- Financial metric comparisons
- Tuition analysis
- Student debt analysis
- Median earnings analysis
- ROI calculation
- Estimated educational cost calculation
- Estimated ten-year earnings calculation
- Estimated net return calculation
- ROI ranking
- Earnings versus tuition visualization
- Debt versus earnings visualization
- College ROI comparison
- Integration of analytical results into the Flask web interface

### ROI Analysis

PayPilot estimates the financial return of attending a college using annual tuition, median student debt, and median annual earnings.

The estimated total educational cost is calculated using four years of annual tuition plus median student debt:

```text
Estimated Total Cost = (Annual Tuition × 4) + Median Student Debt
```

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

### 4. Obtain a College Scorecard API Key

PayPilot requires a U.S. Department of Education College Scorecard API key.

Visit the College Scorecard API documentation:

https://collegescorecard.ed.gov/data/api-documentation/

Follow the instructions to request a free API key through Data.gov.

### 5. Create a `.env` file

In the project root, create a file named `.env` and add your API key:

```text
COLLEGE_SCORECARD_API_KEY=your_api_key_here
```

### 6. Run the application

```bash
python app.py
```

Flask will display the local URL in the terminal. Open that URL in your web browser (typically `http://127.0.0.1:5000`).

---

## Notes

- The `.env` file is excluded from Git for security and must be created manually.
- The `data/` CSV files are generated automatically the first time the application retrieves data from the College Scorecard API.
- The initial search may take longer while the local data cache is created. Subsequent searches will be significantly faster.