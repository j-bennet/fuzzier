import sys

from bs4 import BeautifulSoup
import requests
import textwrap
import pandas as pd
from os import path


tw = textwrap.TextWrapper(width=500, max_lines=1)


def normalize_address(addr):
    text_lines = [line.rstrip(",") for line in addr.strip().split()]
    return tw.fill(" ".join(text_lines)).strip().lower()


def main():
    base_url = "https://www.ripe.net"
    url = "https://www.ripe.net/membership/indices/"
    index_page = BeautifulSoup(requests.get(url).text, "html.parser")

    collected_data = []
    country_urls = [link["href"] for link in index_page.select("#external > a")]
    for country_url in country_urls:
        full_country_url = f"{base_url}{country_url}"
        print(f"Collecting data from {full_country_url}")
        country_page = BeautifulSoup(requests.get(full_country_url).text, "html.parser")
        ncc_urls = [link["href"] for link in country_page.select("#external li a")]
        for ncc_url in ncc_urls:
            full_ncc_url = f"{base_url}{ncc_url}"
            ncc_page = BeautifulSoup(requests.get(full_ncc_url).text, "html.parser")
            ncc_name = ncc_page.select_one("#external h1").text
            ncc_addr = normalize_address(ncc_page.select_one("#external h1+p").text)
            print(f" * {ncc_addr}")
            collected_data.append((full_ncc_url, ncc_name, ncc_addr))
    df = pd.DataFrame(collected_data, columns=["url", "name", "address"])
    df = df.drop_duplicates()
    df.to_csv("nccs.csv", index=False)
    print(f"Total: {df.shape}")


if __name__ == "__main__":
    if path.exists("nccs.csv"):
        reply = input("The file nccs.csv exists. Overwrite? [y/n]: ")
        if reply not in ("y", "Y"):
            print("Not retrieving data.")
            sys.exit(0)
    main()
