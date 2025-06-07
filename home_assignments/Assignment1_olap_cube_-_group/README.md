# Business Intelligence Assignment 1 - OLAP Cube

## Group Members

* Hamna Inam Abro (27113)
* Zara Masood (26928)
* Zuha Aqib (26106)

## Table of Contents

1. [Introduction & Dataset](#introduction--dataset)
2. [Data Understanding](#data-understanding)
3. [Facts, Dimensions, and Useless Variables](#facts-dimensions-and-useless-variables)
4. [Business Problems & Analysis](#business-problems--analysis)

   * Business Problem #1: Customer Retention (Hamna)
   * Business Problem #2: Shipping & Warehouse Optimization (Zara)
   * Business Problem #3: Shipping Mode Effectiveness (Zuha)
5. [Summary of Results](#summary-of-results)
6. [Business Recommendations](#business-recommendations)

## Introduction & Dataset

**Requirement:**
The assignment required us to analyze a selected dataset to apply OLAP cube concepts, drill-down techniques, and BI problem-solving strategies. We needed to identify facts, dimensions, and irrelevant variables, then solve specific business problems with detailed analyses and process diagrams.

**Dataset:**
We used the [Customer Analytics dataset from Kaggle](https://www.kaggle.com/datasets/prachi13/customer-analytics), which contains customer shipment data including warehouse info, shipment mode, customer interactions, product details, and delivery performance.

## Data Understanding

The dataset includes the following key columns:

| Column                 | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| ID                     | Unique customer identifier (excluded from analysis)      |
| Warehouse\_block       | Warehouse divisions (A, B, C, D, E)                      |
| Mode\_of\_Shipment     | Shipment methods (Ship, Flight, Road)                    |
| Customer\_care\_calls  | Number of customer inquiries                             |
| Customer\_rating       | Customer satisfaction rating (1 lowest, 5 highest)       |
| Cost\_of\_the\_Product | Product cost in USD                                      |
| Prior\_purchases       | Number of prior purchases per customer                   |
| Product\_importance    | Categorized as low, medium, or high                      |
| Gender                 | Customer gender                                          |
| Discount\_offered      | Discount percentage on product                           |
| Weight\_in\_gms        | Weight of product in grams                               |
| Reached.on.Time\_Y.N   | Target variable: 1 = late delivery, 0 = on-time delivery |

## Facts, Dimensions, and Useless Variables

**Facts:**
Quantitative measures used for analysis:

* Cost\_of\_the\_Product
* Discount\_offered
* Weight\_in\_gms
* Customer\_care\_calls
* Customer\_rating
* Prior\_purchases
* Reached.on.Time\_Y.N

**Dimensions:**
Categorical variables used to slice data:

* Warehouse\_block
* Mode\_of\_Shipment
* Product\_importance
* Gender

**Useless Variables:**

* ID (unique row identifier, no analytical value)

## Business Problems & Analysis

### Business Problem #1: Customer Retention (Hamna Inam Abro)

**Problem:**
Understand customer behavior and factors influencing long-term engagement and retention after multiple purchases.

**Analysis Summary:**

* Customer engagement drops significantly after 3 prior purchases and declines further after 6.
* Customer care calls decrease as prior purchases increase, suggesting silent churn.
* Higher discounts are given to customers with 7+ purchases, but engagement still falls.
* Late deliveries correlate strongly with customer disengagement.

**Insights:**

* Late delivery is a key churn driver.
* Silent disengagement makes churn detection difficult.
* Discounts delay churn but don’t prevent it long-term.

### Business Problem #2: Shipping & Warehouse Optimization (Zara Masood)

**Problem:**
Identify the best performing warehouse block and shipment mode to optimize on-time delivery and customer satisfaction.

**Analysis Summary:**

* Shipping mode “Ship” delivers most products on time, especially low-importance products.
* Warehouse Block F leads in on-time deliveries, even when discounts are applied.
* Medium importance products shipped via “Ship” with discounts had the highest on-time counts.

**Insights:**

* Prioritize “Ship” for low-importance and medium-importance products.
* Warehouse F’s operational practices could be a benchmark for others.
* Discounts are effective in improving on-time delivery for medium-importance products.

### Business Problem #3: Shipping Mode Effectiveness (Zuha Aqib)

**Problem:**
Analyze the usage and effectiveness of shipping modes and identify causes of delays.

**Analysis Summary:**

* “Ship” is the most used shipping mode, especially for low and medium priority goods.
* Warehouse F is the highest performing warehouse in terms of sales.
* Nearly 60% of shipments via “Ship” are late, negatively impacting customer satisfaction.
* Road and Flight modes have less discrepancy between on-time and late deliveries but still show delays.

**Insights:**

* Although cost-effective, the “Ship” mode suffers from poor punctuality.
* Late deliveries harm the company’s reputation.
* Need to investigate internal processes and logistics to improve overall shipment timeliness.

## Summary of Results

| Problem Area                      | Key Finding                                                                   | Business Impact                                     |
| --------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------- |
| Customer Retention                | Engagement drops after 3-6 purchases; late deliveries are major churn reasons | Need for improved delivery and proactive engagement |
| Shipping & Warehouse Optimization | “Ship” mode and Warehouse F excel in on-time deliveries                       | Focus on shipping mode and warehouse best practices |
| Shipping Mode Effectiveness       | “Ship” mode most used but 60% shipments late                                  | Urgent need to improve “Ship” reliability           |

## Business Recommendations

1. Implement proactive customer engagement and personalized retention strategies.
2. Redesign discount policies to focus on loyalty rewards rather than generic discounts.
3. Use data analytics to detect silent disengagement early.
4. Prioritize “Ship” mode for low- and medium-importance products; reserve “Flight” for urgent deliveries.
5. Study Warehouse F’s operations to replicate success in other warehouses.
6. Investigate causes of delays across all warehouses and shipping modes.
7. Target discounts mainly on medium-importance products to improve delivery and satisfaction.
8. Allocate more resources to improve the “Ship” mode’s delivery performance.
9. Communicate realistic delivery timelines to customers, accounting for shipping delays.
10. Explore improvements in Road and Flight shipping modes to diversify risk and improve overall delivery performance.
