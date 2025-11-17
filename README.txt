<div align="center">

# 📈 Financial Web Scraping & Analysis

Automated extraction and analysis of ETF, mutual fund, and stock data from Morningstar using **Selenium** and **Pandas**.

---

### 🔧 Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen?logo=selenium)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter)

</div>

---

## 📁 Project Structure

financial-webscraping-analysis/
├── src/ # Selenium scraping scripts
├── notebooks/ # Analysis, cleaning, and question-answer notebooks
├── data/ # Raw scraped data and processed datasets
└── README.md


### **src/**
Python scripts for automated web scraping using Selenium WebDriver.

### **notebooks/**
Includes analysis notebooks (`.ipynb`), data cleaning steps, and responses to project questions.

### **data/**
Contains the raw scraped datasets and all processed/cleaned data used in the analysis.

---

## 📊 Overview

This project extracts financial data from Morningstar and performs an exploratory and comparative analysis of:

- **ETFs**
- **Mutual Funds**
- **Stocks**

Key metrics analyzed include:

- Performance  
- Volatility  
- Expense ratios  
- Management fees  

The goal is to identify investment insights and compare products based on risk, cost, and returns.

---

## 🚀 Features

- 🔄 Automated scraping of Morningstar data  
- 🧹 Structured cleaning of scraped datasets  
- 📊 Comparative analysis of performance metrics  
- 📉 Volatility evaluation and risk profiling  
- 💸 Expense ratio & management fee comparison  
- 🎯 Insights for different investor profiles  

---

## ▶️ How to Run

### **1. Scraping scripts (src/)**
The scraping scripts can be executed directly from the terminal or any Python environment.

### **2. Notebooks (`notebooks/`)**

Open any notebook in Jupyter or VS Code and run all cells:

> ⚠️ Recommended: use **"Run All"**.  
> Running individual cells more than once may duplicate preprocessing steps or alter results.

---

## ⚠️ Important (Web Scraping)

For Selenium to work properly:

- The **chromedriver** must be placed in the **project root directory** (same level as `src/`, `data/`, `notebooks/`).
- Ensure your `chromedriver` version matches your installed Chrome version.

---

## 🧠 What I Learned

- Automating dynamic web scraping with Selenium  
- Managing driver sessions and avoiding scraping errors  
- Cleaning and structuring financial datasets with Pandas  
- Financial metric comparison across ETFs, funds, and stocks  
- Building reproducible analytical workflows  

---

<div align="center">

✨ _If you’re reading this from my CV, thanks for taking a look!_  
Feel free to explore, clone the project, or reach out.

</div>
