"""
This module provides functions to retrieve and parse metric and company
information from the WikiRate API. It extracts metadata about metrics,
company-specific values, and supporting source documents.

The module requires an API key stored in the environment variable
`WIKI_RATE_KEY`.

Functions:
    - get_metric_info(metric): Fetch metadata about a specific metric.
    - get_company_info(metric, company, year=None): Retrieve metric values
      for a specific company and year.
"""



import os
import requests

from wiki_data_extractor.utils import page_number_parser

API_KEY = os.environ["WIKI_RATE_KEY"]
DEFAULT_PARAMS = {
    "api_key": API_KEY,
    "format": "json"
}

def get_metric_info(metric: str) -> dict:
    """
    Retrieve metadata for a specified WikiRate metric.

    This function queries the WikiRate API to obtain details about a given
    metric, including its question text, identifier, and data type.

    Args:
        metric (str): The WikiRate metric identifier.

    Returns:
        dict: A dictionary containing:
            - question (str): The metric question or description.
            - custom_id (str): The unique identifier of the metric.
            - data_type (str): The type of data ("Metric" if numeric,
              otherwise an empty string).

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        KeyError: If the required environment variable is missing.

    Example:
        >>> get_metric_info("3341341")
        {
            "question": "How many employees does the company have?",
            "custom_id": "Number of Employees",
            "data_type": "Metric"
        }
    """
    url =  f"https://wikirate.org/~{metric}"


    response_metric = requests.get(url, params=DEFAULT_PARAMS, timeout=10)
    question = ""
    custom_id = ""
    data_type = ""
    if response_metric.status_code == 200:
        response_metric = response_metric.json()
        question = response_metric.get("question", {}).get("content", "")
        custom_id = response_metric.get("name", "")
        if response_metric.get("value_type", {}).get("content") == "Number":
            data_type = "Metric"
        else:
            data_type = ""

    return {"question": question,
            "custom_id": custom_id,
            "data_type": data_type
    }


def get_company_info(metric: str, company: str, year=None) -> dict:
    """
    Retrieve metric data for a specific company from WikiRate.

    If no year is provided, the function fetches the most recent available
    year for the selected metric and company.

    Args:
        metric (str): The WikiRate metric identifier.
        company (str): The WikiRate company identifier.
        year (int, optional): The reporting year. Defaults to the most recent.

    Returns:
        dict: A dictionary containing:
            - company (str): The company name.
            - file_metas (list[dict]): Source document metadata with:
                - file_name (str)
                - file_url (str)
            - answer (str): The metric value with its unit.
            - structured_data (list[dict]): Structured metric data including:
                - unit (str)
                - value (float)
                - time_period (int)
            - page_number (list[str]): Extracted page references from comments.

    Raises:
        requests.exceptions.RequestException: If the API request fails.

    Example:
        >>> get_company_info("3341341", "5590", 2023)
        {
            "company": "Nike Inc",
            "file_metas": [...],
            "answer": "83000 employees",
            "structured_data": [...],
            "page_number": ["p. 45"]
        }
    """

    if not year:
        # Retrieve most recent year the metric is available for selected company
        url = f"https://wikirate.org/~{metric}+~{company}"

        response = requests.get(url, params=DEFAULT_PARAMS, timeout=10)

        if response.status_code == 200:
            response = response.json()
            year = response.get("items")[-1]["year"]


    url = f"https://wikirate.org/~{metric}+~{company}+{year}"


    response = requests.get(url, params=DEFAULT_PARAMS, timeout=10)

    company_name = ""
    file_metas = []
    answer = ""
    structured_data = []
    page_number = []

    if response.status_code == 200:
        response = response.json()
        company_name = response.get("company", "")
        sources = response.get("sources", [])
        for source in sources:
            file_metas.append(
                {"file_name": source.get("title", ""),
                "file_url": source.get("url", "")}
            )
        answer = response.get("value", "").strip() + " " + response.get("unit", "").strip()
        structured_data = [
            {"unit": response.get("unit", ""),
             ### For value there could be different ways to handle it
             # you could have the code break,
             # import math and return math nan
             # or return None
             # as it is the code will break for non numerical values (eg booleans and categorical)
            "value": float(response.get("value")) if response.get("value") else None,
            "time_period": response.get("year")}
        ]

        # Keeping all of the comments to have a look at them for future parsing
        comments = response.get("comments", "")
        if comments:
            page_number = page_number_parser(comments)



    return {"company": company_name,
            "file_metas": file_metas,
            "answer": answer,
            "structured_data": structured_data,
            "page_number": page_number
    }
