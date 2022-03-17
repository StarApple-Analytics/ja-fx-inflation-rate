import requests
import pandas as pd
import json 

from bs4 import BeautifulSoup
from celery import shared_task
from urllib.parse import urlparse
from datetime import datetime

from api.constant import RATES_URL, RESOURCES_DIR, celeryLogger as logger
from api.store.rts import rts

url = RATES_URL
r = requests.get(url)
html_content = r.text
soup = BeautifulSoup(html_content, "html.parser")




@shared_task()
def scrape():

    try:
        doc_url = None

        accordion_items = soup.find_all(match_class(["elementor-accordion-item"]))

        for item in accordion_items:
            children = item.findChildren("div", {"class": "elementor-tab-title"})
            for child in children:
                if child.find("a").getText() == "Headline Inflation":
                    content = item.find("div", {"class": "elementor-tab-content"})
                    doc = content.find("a")["href"]
                    doc_url = doc

        parse_object = urlparse(url)
        excel_url = f"{parse_object.scheme}://{parse_object.netloc}{doc_url}"

        df = pd.read_excel(excel_url, parse_dates=True)

        timeseries_df = timeseries_to_df(df)
        timeseries = df_to_timestamps(timeseries_df)
        
        rts.madd(timeseries)
        return [timeseries]
    except Exception as e:
        logger.error(e)
        print(e)


def match_class(target):
    def do_match(tag):
        classes = tag.get("class", [])
        return all(c in classes for c in target)

    return do_match


def timeseries_to_df(df):
    date_idx = None
    for idx, row in df.iterrows():
        if row["BANK OF JAMAICA STATISTICS DEPARTMENT"] == "Date":
            date_idx = idx

    df = df.iloc[date_idx + 2 :]
    timeseries_df = df[["BANK OF JAMAICA STATISTICS DEPARTMENT", "Unnamed: 1"]]
    timeseries_df = timeseries_df.rename(
        columns={
            "BANK OF JAMAICA STATISTICS DEPARTMENT": "date",
            "Unnamed: 1": "inflation",
        }
    )
    return timeseries_df


def df_to_timestamps(timeseries_df):
    timestamps = []
    for _, row in timeseries_df.iterrows():
        if row["date"].year >= 2012:
            dt = datetime.strptime(str(row["date"]), "%Y-%m-%d %H:%M:%S")
            timestamps.append(
                tuple(["MONTHLYINFLATION:JA", int(dt.timestamp()), row["inflation"]]),
            )
    return timestamps


if __name__ == "__main__":
    print(scrape())
