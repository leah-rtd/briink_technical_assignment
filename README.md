# 📊 WikiRate ESG Data Extractor

This project extracts ESG-related metrics from the WikiRate API and transforms them into a structured dataset suitable for machine learning training and evaluation pipelines. It was developed as part of a technical assessment for Briink.

## 🚀 Overview

The objective of this project was to:

Access and explore data from WikiRate.
Extract ESG-related metrics for at least 10 companies.
Transform the data into a structured format suitable for AI systems.
Save the resulting dataset as a JSON file.


## 🌐 Accessing WikiRate’s Data

Data was retrieved via the WikiRate API using the `requests` package with JSON responses. Endpoints were dynamically constructed using metric and company identifiers:

https://wikirate.org/~{metric}
https://wikirate.org/~{metric}+~{company}+{year}

The requests library was used for API communication, with the API key stored securely as an environment variable (WIKI_RATE_KEY).

## 📈 Selected ESG Metrics & Selected Companies

Three ESG-related metrics were selected based on relevance and data availability:

Category	Metric
Social	Total Number of Employees
Social (Diversity & Inclusion)	Percentage of Female Employees
Governance/Social Transparency	Social Metrics Disclosure Rate

Data was collected for the following ten companies:

H&M, Unilever, Nike Inc., Puma, Adidas AG, Kering, Fast Retailing, Marks and Spencer Group plc, Burberry Group plc, and Nestlé.


## ⚠️ Data Quality Issues and Challenges

 - Unknown Values: WikiRate occasionally returns `Unknown`, which cannot be converted to numeric values.
 - Most Recent Year Selection: When no data existed for a certain company, the program breaks.
 - Source Availability: Scarcity of sources
 - Metric Constraints: The implementation supports only numerical metrics (value_type = Number), as required by the assignment.
 - Metric Selection: Metrics were manually chosen to ensure sufficient data quality across companies.

## ❓ Questions for Clarification

 - Should file_url reference the original document instead of a WikiRate JSON source?
 - Since WikiRate does not provide a formatted answer field, is reconstructing the answer from value and unit acceptable?
 - Should the same ten companies be used consistently across all metrics?


## 🛠️ Assumptions and Trade-Offs

 - Only numerical metrics were included to align with the specification.
 - The most recent available year was selected when unspecified.
 - Page numbers were extracted from comments using regex when available.
 - Metrics were manually curated to ensure coverage across companies.
 - Missing or "Unknown" values were identified as limitations rather than excluded automatically.


## 🤖 AI and Tool Usage

AI tools were used to support development while maintaining independent problem-solving.
Assistance included:
 - Creating module and function docstrings.
 - Designing the regex pattern for page number extraction.
 - Reviewing schema compliance and potential improvements.
 - Writing the README.md

Additional tools used:
 - Pylint for static code analysis (which flagged missing request timeouts).
 - Requests for API communication.
 - Regex (re) for parsing page numbers.


## 🔧 Future Improvements

With more time, the following enhancements would be implemented:
 - Support for boolean and categorical metrics.
 - Improved handling of "Unknown" and missing values.
 - Automated filtering for entries with valid sources.


## 📄 Deliverables
Codebase: Python module for extracting and transforming WikiRate data.
Dataset: `results.json` containing ESG metrics for 10 companies.
Documentation: This README describing methodology, challenges, and insights.

Author: Technical Assessment Submission for Briink
