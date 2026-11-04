# Premier Card Customer Profitability Framework
### Amex Campus Challenge 2026 | Strategy Track

## Overview

This project was developed as part of the **American Express Campus Challenge 2026**. The objective was to identify the top 20% most profitable customers among **500,000 Premier Cardmembers** using 23 anonymised customer attributes.

Rather than ranking customers solely by their spending, the framework estimates customer profitability by considering multiple revenue streams, associated costs, customer risk, and engagement.

The solution combines exploratory data analysis, business-driven missing-value treatment, financial feature engineering, and rank-based aggregation to generate a unified customer profitability score.

## Problem Statement

A customer's spending does not necessarily reflect their actual value to a financial institution.

While high-spending customers generate revenue, they may also incur substantial costs through reward redemptions, premium benefits, and lending-related risks.

The challenge was to develop a framework that could:

- Estimate customer value using anonymised financial and behavioural attributes.
- Account for revenue from spending, revolving balances, and lending.
- Incorporate costs associated with rewards and premium benefits.
- Adjust profitability estimates based on customer risk and distress signals.
- Rank customers and identify the actual top 20% most profitable cardmembers.

## Dataset

The dataset contains approximately **500,000 cardmembers** and 23 anonymised attributes (`f1`–`f23`).

The attributes cover the following broad categories:

| Category | Attributes | Description |
|---|---|---|
| Financial activity | f1, f4, f5 | Revolving balances, rewards balance, total spending |
| Spending breakdown | f6–f10 | Airline, other, entertainment, lodging, and dining expenditure |
| Risk indicators | f11 | Average customer risk score |
| Customer engagement | f12, f19, f20 | Website logins, supplementary accounts, active cards |
| Benefit utilisation | f13–f16 | Lounge access, airline credits, cab benefits, entertainment credits |
| Lending | f17, f18 | Lending facility amounts |
| Rewards | f21 | Rewards points redeemed |
| Email engagement | f22, f23 | Email opens and clicks |
| Customer identifier | id | Unique cardmember identifier |

## Methodology

### 1. Exploratory Data Analysis

Performed exploratory analysis to understand feature distributions, data types, missing-value patterns, and relationships between attributes.

Key investigations included:

- Feature-level descriptive statistics and missing-value percentages.
- Identification of groups of attributes sharing identical missingness patterns.
- Analysis of logical relationships between features.
- Statistical testing to determine whether missingness was associated with other observed customer characteristics.

### 2. Structured Missing-Value Analysis

A key finding was that missingness was not simply random.

Several groups of attributes exhibited block-structured missingness:

- Spending attributes (`f6`–`f10`) were missing together.
- Rewards attributes (`f4`, `f21`) exhibited identical missingness patterns.
- Benefit utilisation attributes (`f13`–`f16`) were also missing together.

Additional analysis examined the relationship between email opens (`f22`) and clicks (`f23`), as well as differences in spending distributions between customers with and without rewards information.

A Mann–Whitney U test was used to investigate whether missingness in rewards-related information was associated with differences in observed total spending.

These findings motivated a business-driven imputation strategy rather than blanket mean or median imputation.

### 3. Business-Driven Imputation

Missing values were handled according to the economic meaning of each attribute.

Examples include:

- Lending attributes: Missing lending facilities were treated as zero.
- Benefit utilisation: Missing usage records were treated as zero where appropriate.
- Customer engagement: Median imputation was used for attributes such as website logins and active account counts.
- Entertainment credit usage: Median imputation was used because the observed values indicated that zero was not an appropriate assumption.

For spending, missing category-level information was estimated using the median ratio between total spending and the available category-wise spending.

This preserved useful customer information while avoiding assumptions that all missing values represented the same underlying situation.

### 4
