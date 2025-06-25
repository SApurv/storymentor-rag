from scrape_utils import scrape_article_to_file

urls = [
    "https://www.writerstreasure.com/creative-writing-101/",
    "https://www.agnesscott.edu/center-for-writing-and-speaking/handouts/guide-to-creative-writing.html",
    "https://www.enchantingmarketing.com/creative-writing-techniques/",
    "https://writers.com/the-art-of-storytelling",
    "https://www.writersdigest.com/whats-new/how-to-write-vivid-descriptions",
    "https://nationalcentreforwriting.org.uk/writing-hub/how-to-write-a-short-story-2/",
    "https://web.uri.edu/graduate-school/strategies-to-overcome-writers-block/"
]

for url in urls:
    scrape_article_to_file(url)