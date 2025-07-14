from bs4 import BeautifulSoup
import requests
import html2text
from ddgs import DDGS
import sys
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import sys
sys.stdout.reconfigure(encoding='utf-8')
from urllib.parse import urlparse
import unicodedata
from urllib.parse import urlparse
from bs4 import NavigableString





sys.stdout.reconfigure(encoding='utf-8')

import requests






def get_domain_url(url):
        
        result=urlparse(url)
        domain=result.netloc
        if domain.startswith("www."):
                domain=domain[4:]
        domain_name=domain.split('.')[0]
        print(domain_name)
        return domain_name







def get_description(iframe_url):
    print(f"Fetching URL for Iframe {iframe_url}")
    response = requests.get(iframe_url)

    if response.status_code != 200:
        print(f"Failed to fetch URL for Iframe {iframe_url}")
        return None
    
    response.encoding = response.apparent_encoding 

    soup = BeautifulSoup(response.text, "html.parser")
    description_tag = soup.find("meta", attrs={"name": "description"})
    if description_tag and description_tag.get("content"):
        return description_tag.get("content")

    return get_domain_url(iframe_url)







def scrape_and_convert_to_markdown(url, smart_mode=False):
    if not url.startswith("http"):
        url = "http://" + url
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Failed to fetch URL {url}")
        return f"Failed to fetch URL {url}"

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup.find_all(["style", "script"]):
        tag.decompose()

    for img_tag in soup.find_all("img"):
        img_tag.decompose()

    iframes = soup.find_all("iframe")

    for iframe in iframes:
        src = iframe.get("src")

        if src:
            description = get_description(src)
            iframe_link = f"[Iframe Link: {src}]({src})"
            if description:
                iframe_link += f" - Description: {description}"
            iframe.replace_with(iframe_link)

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    markdown = converter.handle(str(soup.body))
    if smart_mode:
        print("Cleaning markdown")


    return markdown














# on va extraire id du link youtube depui url et recupurer le soutitrage puis formater le script en texte dans fichier jason
def get_youtube_script(url):
    if "youtube.com/embed/ " in url :
          youtube_id=url.split("youtube.com/embed/")[1].split("?")[0]
    elif "youtube.com/watch?v=" in url:
            youtube_id = url.split("youtube.com/watch?v=")[1].split("&")[0]
    else:
        print("Could not find youtube id in url")
        return 
    try:
        transcript = YouTubeTranscriptApi.get_transcript(youtube_id)
    except Exception as e:
        print(f"Could not get transcript for YouTube ID {youtube_id}: {e}")
        return

    text = "\n".join([item['text'] for item in transcript])
    return text
     








def search_urls_and_preview(keywords, limit=None):
    num_results = 0
    with DDGS(timeout=20) as ddgs:
        for r in ddgs.text(keywords):
            yield r
            num_results += 1
            if limit and num_results >= limit:
                break












url="https://www.sfmtechnologies.com/"

description=get_description(url)

print("description_fixed",description)

markdown=scrape_and_convert_to_markdown(url)
with open("output.md", "w", encoding="utf-8") as f:
        f.write(markdown)


url2= "https://www.youtube.com/watch?v=EbRHq4bdxl0"
transcript=get_youtube_script(url2)
if transcript:
    with open("transcript_output.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

for result in search_urls_and_preview("SFM Technologies", limit=5):
    print("titllllllllles",result["title"])
    print("whay fddddddddddd",result["href"])
    print("boddddddddddddddddddy",result["body"])
    print("-" * 50)