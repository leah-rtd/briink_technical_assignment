"""


This script retrieves WikiRate metric data for a predefined list of
companies and stores the results in a JSON file.

It combines metric metadata, company-specific values, and structured
source information to produce a dataset suitable for downstream
processing, analytics, or machine learning applications.

Constants:
    METRICS (dict): Mapping of metric names to WikiRate IDs.
    COMPANIES (dict): Mapping of company names to WikiRate IDs.

Functions:
    get_all_company_metric(metric, companies, year=None):
        Fetch data for all specified companies for a given metric.
"""




import json
import time

from wiki_data_extractor.extract_info import get_metric_info, get_company_info

METRICS = {"Nb_employes": "3341341",
           "Percent_female_employees": "19856286",
           "Social_metrics_disclosure_rate": "7343129"}

COMPANIES = {"H&M": "5590",
             "Unilever": "8906",
             "Nike Inc": "5800",
             "Puma": "18109",
             "Adidas AG": "7217",
             "Kering": "8362",
             "Fast Retailing": "56584",
             "Marks and Spencer Group plc": "9269",
             "Burberry Group plc": "9139",
             "Nestle": "6373"
             }


def get_all_company_metric(metric: str, companies: str, year=None) -> dict:
    """
    Retrieve metric data for multiple companies from WikiRate.

    This function gathers metric metadata and company-specific data,
    consolidating them into a structured format suitable for storage
    or analysis.

    Args:
        metric (str): The WikiRate metric identifier.
        companies (Iterable[str]): An iterable of WikiRate company IDs.
        year (int, optional): The reporting year. If None, the most
                              recent year is used.

    Returns:
        list[dict]: A list of dictionaries containing:
            - input (dict): Metadata and context for the query.
            - reference_output (dict): The answer and source documents.
            - structured_data (list[dict]): Structured metric values.

    Example:
        >>> get_all_company_metric("3341341", ["5590", "8906"])
        [
            {
                "input": {...},
                "reference_output": {...},
                "structured_data": [...]
            }
        ]
    """

    print("Getting Metric Info")

    metric_info = get_metric_info(metric)

    print("Metric info gathered successfully")
    print(metric_info)


    result = []
    for company in companies:
        print(f"Getting Info for {company}")

        company_info = get_company_info(metric, company, year)

        source_documents = []

        # If there is no page number then the source_documents
        # is the same as file_metas in the input
        if not company_info["page_number"]:
            source_documents = company_info["file_metas"]

        else:
            # Comments where the page_number is included is not in the same
            # result as the file data
            # which means that if there is more than 1 file it would be
            # unclear which file is being referred to in the comments
            if len(company_info["file_metas"]) == 1:
                source_documents = [
                    {"file_name": company_info["file_metas"][0]["file_name"],
                     "file_url": company_info["file_metas"][0]["file_url"],
                     "page_number": company_info["page_number"]}
                ]


        result.append(
            {
                "input": {
                    "question": metric_info["question"],
                    "custom_id": metric_info["custom_id"],
                    "data_type": metric_info["data_type"],
                    "company": company_info["company"],
                    "file_metas": company_info["file_metas"]
                },
                "reference_output": {
                    "answer": company_info["answer"],
                    "source_documents": source_documents
                },
                "structured_data": company_info["structured_data"]
            }
        )
        time.sleep(0.3)

    return result


if __name__ == "__main__":

    final_result = []
    for metric_id in METRICS.values():
        metric_result = get_all_company_metric(metric_id, COMPANIES.values())

        final_result.extend(metric_result)
        time.sleep(1)

    with open("results.json", "w") as file:
        json.dump(final_result, file)
