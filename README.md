# 📊 Laptop Reviews Analysis Dashboard

## Overview
This project presents a **comprehensive analysis of 24,000 laptop reviews**, utilizing **interactive visualizations and data exploration tools**. The dashboard provides insights into rating distributions, popular products, review content patterns, and sentiment analysis.

The dataset used in this project is sourced from **Kaggle** and is processed using Python libraries such as **pandas, plotly, and preswald**.

You can access the live dashboard here: [Laptop Reviews Analysis Dashboard](https://laptop-reviews-analysis-project-946230-vxem2hz4-ndjz2ws6la-ue.a.run.app/)

## Features
### 1️⃣ **Data Loading & Dynamic View**
- Connects to the dataset using `preswald.connect()`.
- Displays a **sample of review data** for a quick glance.
- Allows users to filter reviews dynamically based on a **ratings threshold slider**.

### 2️⃣ **Rating Distribution Analysis**
- **Histogram of Ratings:** Shows how ratings are distributed.
- **Average Rating Line:** Highlights the mean rating across all reviews.
- **Dynamic Review Filtering:** Allows filtering of data above a selected rating.

### 3️⃣ **Product Analysis**
- **Top 10 Most Reviewed Laptops:** Bar chart ranking laptops by review count.
- **Top-Rated Laptops:** Visualization of the **highest average-rated** laptops with at least 20 reviews.
- **Rating Distribution of Top 5 Products:** Grouped histogram displaying how ratings vary for the most reviewed laptops.

### 4️⃣ **Review Content Analysis**
- **Review Length Distribution:** Shows how long typical reviews are.
- **Review Length by Rating:** Analyzes whether **higher/lower ratings** are linked to longer/shorter reviews.
- **Common Words in Reviews:** Extracts and visualizes the most frequently mentioned words (excluding stopwords).

### 5️⃣ **Correlation & Relationship Analysis**
- **Relationship Between Review Count & Average Rating:** Scatter plot examining trends.
- **Rating Trends Over Time:** Time-based analysis of how ratings fluctuate.

### 6️⃣ **Title & Sentiment Analysis**
- **Average Title Length by Rating:** Analyzes whether longer titles indicate different rating trends.
- **Sentiment Distribution Pie Chart:** Categorizes ratings into **Positive, Neutral, and Negative Sentiments**.

### 7️⃣ **Insights Summary**
A detailed text summary that provides key statistics:
- Total number of products and reviews analyzed.
- Overall average rating.
- Average review length in words.
- Highest-rated laptop model.
- Most common rating and percentage of 5-star reviews.

## Technologies Used
- **Python** (Data Analysis & Visualization)
- **pandas** (Data Processing)
- **plotly** (Interactive Charts & Graphs)
- **preswald** (Dashboard & Data Connection)
- **re** (Regular Expressions for Text Processing)

## How to Run the Dashboard
1. **Install Dependencies**
   ```sh
   pip install pandas plotly preswald
   ```
2. **Ensure Data Availability**
   - The dataset should be accessible through `preswald.get_df('reviews_csv')`.
3. **Run the Script**
   - Execute the Python script in a Jupyter Notebook or Python environment using
     ```sh
   preswald run
   ```
4. **Interact with the Dashboard**
   - Utilize **filters, charts, and insights** to explore the laptop reviews dataset.

---
📌 *This project provides valuable insights into customer feedback on laptops, helping users make informed purchasing decisions based on extensive review analysis.*

