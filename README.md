# Project Title: PayPilot

## Authors: 
Zayba Syed, Bushra Naveed

---

## Project Description

PayPilot is a Python desktop application designed to help prospective college students evaluate the financial value of higher education. Using live data from the U.S. Department of Education College Scorecard API, the application allows users to search colleges and compare metrics such as tuition, graduation rates, median earnings after graduation, and average student debt. Users will be able to filter colleges by state, school type, major, degree level, and financial preferences to find schools that best match their goals. The application will calculate a Return on Investment (ROI) score to help users compare the long-term financial value of different colleges and programs. Interactive charts and visualizations will make it easier to analyze salary outcomes and educational costs before making college decisions.

---

## Project Outline / Plan

- Connect to the College Scorecard API
- Retrieve college information based on user-selected filters
- Store retrieved data locally for faster access
- Display college statistics in an organized table
- Calculate an ROI score using salary, tuition, and debt information
- Create interactive charts comparing earnings, tuition, and debt
- Build an intuitive desktop graphical user interface
- Test and document the application

---

## Interface Plan

The application will feature a user-friendly desktop interface where users can search for colleges using filters such as state, major, school type, degree level, minimum salary, and maximum debt. Search results will display important information including tuition, graduation rate, median earnings after graduation, average student debt, and the calculated ROI score. Users will also be able to view charts and graphs that compare colleges based on salary outcomes and educational costs.

---

## Data Collection and Storage Plan (Author #1)

The application will collect data from the U.S. Department of Education College Scorecard API. Information including college names, tuition costs, graduation rates, student debt, median earnings after graduation, acceptance rates, and degree information will be retrieved through API requests. The data will be stored locally using CSV files or an SQLite database to improve performance and reduce unnecessary API requests.

---

## Data Analysis and Visualization Plan (Author #2)

The collected data will be analyzed using Python and the Pandas library to compare colleges based on earnings, debt, tuition, and graduation rates. An ROI score will be calculated to estimate the financial value of attending each college. The application will generate visualizations such as bar charts, scatter plots, and histograms using Plotly or Matplotlib to help users compare schools and identify trends in salary outcomes and educational costs.
