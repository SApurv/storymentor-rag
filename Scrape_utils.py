import requests, os, re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def clean_filename(title_or_url):
    """Generate a safe filename from title or fallback URL"""
    filename = re.sub(r'[^\w\s-]', '', title_or_url).strip().lower()
    return re.sub(r'[\s]+', '_', filename)[:80] + ".txt"

def scrape_article_to_file(url, output_dir="Data/Writing_guides"):
    try:
        # Fetch the webpage
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Try to extract main content (adjust based on site)
        article = (
            soup.find("article")
            or soup.find("div", class_=re.compile("entry-content|post-content|main|article|content"))
            or soup.body
        )
        if not article:
            raise Exception("Couldn't find main content block")

        # Extract text and clean
        text = article.get_text(separator="\n", strip=True)

        # Generate filename
        title_tag = soup.find("title")
        title = title_tag.text if title_tag else urlparse(url).netloc
        filename = clean_filename(title)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)

        # Save the content
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Source: {url}\n\n{text}")

        print(f"✅ Saved article to: {output_path}")

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
