# 📊 WikiRate ESG Data Extractor

This project extracts ESG-related metrics from the WikiRate API and transforms them into a structured dataset suitable for machine learning training and evaluation pipelines. It was developed as part of a technical assessment for Briink.

## Navigating the module
```
.
├── results.json           # Final structured dataset
│── README.md              # Project documentation
│── .env.sample            # Storing environment variables
wiki_data_extractor/
│── extract_info.py        # Fetches metric and company data from WikiRate
│── utils.py               # Helper utilities (e.g., regex parsing)
└── create_database.py     # Main script to generate the dataset

```
File Descriptions:
 - `extract_info.py`:
    - `get_metric_info()`: Retrieves metadata for a WikiRate metric.
    - `get_company_info()`: Extracts company-specific metric data, sources, and structured values.
 - `utils.py`:
    - `page_number_parser()`: Extracts page references from source comments using regex.
- `create_database.py`:
  - `get_all_company_metric()`: Aggregates data for multiple companies and formats it into the required schema.
  - Serves as the main entry point for generating the dataset.

## 🌐 Accessing WikiRate’s Data

Data was retrieved via the WikiRate API using the `requests` package with JSON responses. Endpoints were dynamically constructed using metric and company identifiers:

``` python
https://wikirate.org/~{metric}
https://wikirate.org/~{metric}+~{company}+{year}
```
More information on accessing WikiRate's data can be found in `wiki_data_extractor/extract_info.py` .
The API key is stored as an environment variable `WIKI_RATE_KEY` see `.env.sample`.

If the environment variable is set, run the script with:
``` bash
python -m wiki_data_extractor.create_database
```

## 📈 Selected ESG Metrics & Selected Companies

Three ESG-related metrics were selected based on relevance and data availability:
 - Total Number of Employees
 - Percentage of Female Employees
 - Social Metrics Disclosure Rate

Data was collected for the following ten companies:
H&M, Unilever, Nike Inc., Puma, Adidas AG, Kering, Fast Retailing, Marks and Spencer Group plc, Burberry Group plc, and Nestlé.


## ⚠️ Data Quality Issues and Challenges

 - Unknown Values: WikiRate occasionally returns `"Unknown"`, which cannot be converted to numeric values.
 - Most Recent Year Selection: When no data existed for a certain company, the program breaks.
 - Source Availability: Scarcity of sources
 - Metric Constraints: The implementation supports only numerical metrics (value_type = Number), as required by the assignment.
 - Metric Selection: Metrics were manually chosen to ensure sufficient data quality across companies.

## ❓ Questions for Clarification

 - Should `file_url` reference the original document instead of a WikiRate JSON source?
 - Since WikiRate does not provide a formatted `answer` field, is reconstructing the answer from `value` and `unit` acceptable?
 - Should the same ten companies be used consistently across all metrics?


## 🛠️ Assumptions and Trade-Offs

 - Only numerical metrics were included to align with the specification.
 - The most recent available year was selected for all metrics.
 - Page numbers were extracted from comments using regex when available.
 - Metrics were manually curated to ensure coverage across companies.


## 🤖 AI and Tool Usage

AI assistance was used for:
 - Writing module and function docstrings and README.md.
 - Designing the regex pattern for page number extraction.
 - Reviewing schema compliance and potential improvements.
 - Identifying possible improvements (e.g. float conversion handling, reusable API parameters)

Additional tools used:
 - **Pylint** for static code analysis (which flagged missing request timeouts).
 - **Requests** for API communication.
 - **Regex** (`re`) for parsing page numbers.


## 🔧 Future Improvements

With more time, the following enhancements would be implemented:
 - Support for boolean and categorical metrics.
 - Improved handling of "Unknown" and missing values.
 - Automated filtering for entries with valid sources.


## 📄 Deliverables
 - **Codebase**: Python module for extracting and transforming WikiRate data.
 - **Dataset**: `results.json` containing ESG metrics for 10 companies.
 - **Documentation**: This README describing methodology, challenges, and insights.

Author: Technical Assessment Submission for Briink
