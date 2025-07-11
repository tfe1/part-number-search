from flask import Flask, render_template, request, redirect
import sources
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"

        # Get meta description
        desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else "No description"

        # Get image
        img_tag = soup.find("meta", property="og:image")
        image = img_tag["content"].strip() if img_tag and img_tag.get("content") else ""

        return {
            "title": title,
            "description": description,
            "image": image,
            "url": url
        }
    except Exception as e:
        return {
            "title": "Error",
            "description": str(e),
            "image": "",
            "url": url
        }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        part_number = request.form.get("part_number", "").strip()
        selected_sources = request.form.getlist("sources")

        if part_number and selected_sources:
            results = []
            for name in selected_sources:
                template = sources.SOURCES.get(name)
                if template:
                    url = template.format(part_number)
                    scraped = scrape_data(url)
                    scraped["source"] = name
                    results.append(scraped)
            return render_template("results.html", results=results)
    return render_template("index.html", sources=sources.SOURCES.keys())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
