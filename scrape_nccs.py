from bs4 import BeautifulSoup
import requests
import textwrap
from pprint import pprint

tw = textwrap.TextWrapper(width=500, max_lines=1)


def normalize_address(addr):
    text_lines = [line.rstrip(",") for line in addr.strip().split()]
    return tw.fill(", ".join(text_lines))


def main():
    base_url = "https://www.ripe.net"
    url = "https://www.ripe.net/membership/indices/"
    index_page = BeautifulSoup(requests.get(url).text, "html.parser")

    collected_data = []
    country_urls = [link["href"] for link in index_page.select("#external > a")]
    for country_url in country_urls:
        full_country_url = f"{base_url}{country_url}"
        country_page = BeautifulSoup(requests.get(full_country_url).text, "html.parser")
        ncc_urls = [link["href"] for link in country_page.select("#external li a")]
        for ncc_url in ncc_urls:
            full_ncc_url = f"{base_url}{ncc_url}"
            ncc_page = BeautifulSoup(requests.get(full_ncc_url).text, "html.parser")
            ncc_name = ncc_page.select_one("#external h1").text
            ncc_data = normalize_address(ncc_page.select_one("#external h1+p").text)
            collected_data.append((full_ncc_url, ncc_name, ncc_data))
            if len(collected_data) >= 10:
                break
        break
    pprint(collected_data)
    print(f"Addresses: {len(collected_data)}")


if __name__ == "__main__":
    main()