from wiki_data_extractor.extract_info import get_metric_info, get_company_info
import json
import time

METRICS = {"Nb_employes": "3341341"}

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


def get_all_company_metric(metric, companies, year=None):

    print("Getting Metric Info")

    metric_info = get_metric_info(metric)

    print("Metric info gathered successfully")
    print(metric_info)


    result = []
    for company in companies:
        print(f"Getting Info for {company}")

        company_info = get_company_info(metric, company, year)
        # Checking if the comments exist for future parsing
        if not company_info["comments"]:
            source_documents = company_info["file_metas"]
        else:
            # The comment with page number will only work if there is only one source file
            if len(company_info["file_metas"]) == 1:
                source_documents = [
                    {"file_name": company_info["file_metas"][0]["file_name"],
                     "file_url": company_info["file_metas"][0]["file_url"],
                     "comments": company_info["comments"]}
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
                    "source_documtents": source_documents
                },
                "structured_data": company_info["structured_data"]
            }
        )
        time.sleep(0.3)

    return result


if __name__ == "__main__":
    result = get_all_company_metric(METRICS["Nb_employes"], COMPANIES.values())

    with open("results_any_year.json", "w") as file:
        json.dump(result, file)
