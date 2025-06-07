# BI Activity 2
in this activity we had to refer to our previous course (Database Management Systems) project and first review the project (what it was), identify the business, grain, facts, dimensions, and finally, the star schema.

my team members were: Zehra, Farah & I.

our project was a travel management system for users and vendors. 

---

# Business Intelligence

**Activity 02: From Database to Data Warehouse (DB to DWH)**
**Spring 2025**

**Instructor:** Miss Abeera Tariq

**Group Members:**

* Zehra Ahmed (ERP: 26965) – Group Leader
* Farah Inayat (ERP: 26912)
* Zuha Aqib (ERP: 26106)

---

## Objective

The purpose of this activity was to transition a transactional database system into a dimensional data warehouse using a **star schema**. The focus was to identify a core business process within an existing database project and design a data mart suitable for analytical purposes. This involved defining the business grain, selecting appropriate facts and dimensions, and building a star schema structure that supports meaningful business intelligence insights.

---

## Project Background

### Original Database Project: **Travel Management System (TMS)**

The TMS was designed to manage travel bookings, payments, vendor collaboration, customer feedback, and package offerings. It supports multiple stakeholders including customers, vendors, and administrators. Core features of the database included:

* **Customer registration and login with validations**
* **Package creation and approval by vendors and admins**
* **Real-time booking with seat availability checks**
* **Payment tracking, refunds, and booking confirmations**
* **Feedback collection after travel completion**
* **Automation via triggers and stored procedures**

This transactional system ensures data integrity and operational smoothness by handling business rules such as payment status, dynamic pricing, booking deadlines, and cancellation policies.

---

## Task Overview

### Task 1: Review the Database Project

A comprehensive summary of the **Travel Management System** was prepared, reviewing key entities such as `Customers`, `Bookings`, `Payments`, `Packages`, and `Feedback`. The project ensured structured booking and payment processing with automated validations and real-time updates.

---

### Task 2: Identify the Business Process

**Chosen Process:** **Booking and Payment Workflow**

This process was selected because it produces the most critical and voluminous transactional data in the system. It involves:

* Booking validation based on seat availability.
* Payment confirmation and tracking.
* Automatic status updates for bookings.
* Refunds, cancellations, and booking changes.
* Collection of customer feedback after the trip.

This workflow is central to business operations and provides valuable insights for **revenue forecasting, customer behavior, vendor performance, and seasonal trends**, making it ideal for a **data mart**.

---

### Task 3: Specify the Grain

**Grain (Level of Detail):**
Each row in the fact table represents **a single individual traveler** per booking.

> For example, if a family booking includes 5 members, the fact table will have 5 rows—**one for each person**. This atomic level of detail enables precise analysis on customer spending, travel frequency, and booking behavior.

---

### Task 4: Facts & Dimensions

A combination of facts (numerical values for analysis) and dimensions (descriptive attributes) were identified and justified:

| Attribute             | Type                   | Description                          | Purpose                                               |
| --------------------- | ---------------------- | ------------------------------------ | ----------------------------------------------------- |
| **ID**                | Degenerate Dimension   | Unique row identifier                | Tracks each traveler's record                         |
| **Customer**          | Foreign Key            | Links to customer data               | Enables demographic-based analysis                    |
| **Package**           | Foreign Key            | Links to travel packages             | Allows insight into package performance               |
| **Date**              | Foreign Key            | Links to date table                  | Supports time-series analysis                         |
| **Booking**           | Foreign Key            | Links to booking table               | Tracks booking behavior                               |
| **Payment**           | Foreign Key            | Links to payment details             | Helps analyze payment trends                          |
| **Total Price**       | Fact                   | Total amount for booking             | Revenue computation                                   |
| **Amount Paid**       | Fact                   | Amount paid by the customer          | Identifies outstanding payments and forecasts revenue |
| **Booking Count**     | Fact (running count)   | Number of bookings per customer      | Identifies new vs returning customers                 |
| **Commission Earned** | Fact                   | Commission collected by admin        | Assesses profitability and admin earnings             |
| **Average Spending**  | Fact (running average) | Average amount spent by the customer | Guides pricing and marketing strategies               |

---

### Task 5: Star Schema Design

The final deliverable was a **star schema**, representing a dimensional model ideal for querying and BI applications. The schema includes:

* **One Fact Table:** Travel\_Fact
* **Multiple Dimensions:**

  * Customer\_Dim
  * Package\_Dim
  * Booking\_Dim
  * Payment\_Dim
  * Date\_Dim

Relationships were clearly defined using **primary (PK)** and **foreign keys (FK)**, with cardinalities designed for optimized performance in OLAP-style queries.

---

## Business Intelligence Value

By converting the transactional database into a dimensional data warehouse:

* Businesses can perform **revenue and commission forecasting**.
* Analysts can monitor **customer retention** via booking frequency.
* Real-time BI tools can **track outstanding receivables**.
* Seasonal booking trends can be analyzed for **marketing and vendor planning**.
* Admins can evaluate **vendor performance and package popularity**.
* Alerts for **fraud detection or unusual payment patterns** can be created.

---

## Conclusion

This activity successfully translated a complex, transactional travel booking system into a well-structured star schema for business intelligence purposes. The focus on the **Booking and Payment** process provided high-value analytical potential, laying the foundation for actionable insights and data-driven decision-making. The detailed grain, carefully selected facts and dimensions, and the logical schema design reflect a deep understanding of data warehousing principles and practical BI applications.