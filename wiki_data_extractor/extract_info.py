import requests
import os

API_KEY = os.environ["WIKI_RATE_KEY"]


def get_metric_info(metric):
    url =  f"https://wikirate.org/~{metric}"


    params = {"api_key": API_KEY,
            "format": "json"
    }

    response_metric = requests.get(url, params=params)
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


def get_company_info(metric, company, year=None):

    if not year:
        # Retrieve most recent year the metric is available for selected company
        url = f"https://wikirate.org/~{metric}+~{company}"
        params = {"api_key": API_KEY,
            "format": "json"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            response = response.json()
            year = response.get("items")[-1]["year"]


    url = f"https://wikirate.org/~{metric}+~{company}+{year}"

    params = {"api_key": API_KEY,
            "format": "json"
    }

    response = requests.get(url, params=params)

    company = ""
    file_metas = []
    answer = ""
    structured_data = []
    comments = ""
    if response.status_code == 200:
        response = response.json()
        company = response.get("company", "")
        sources = response.get("sources", [])
        for source in sources:
            file_metas.append(
                {"file_name": source.get("title", ""),
                "file_url": source.get("url", "")}
            )
        answer = response.get("value", "") + " " + response.get("unit", "")
        structured_data = [
            {"unit": response.get("unit", ""),
            "value": float(response.get("value", "")),
            "time_period": response.get("year")}
        ]

        # Keeping all of the comments to have a look at them for future parsing
        comments = response.get("comments", "")

    return {"company": company,
            "file_metas": file_metas,
            "answer": answer,
            "structured_data": structured_data,
            "comments": comments
    }
