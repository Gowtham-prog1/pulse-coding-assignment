Pulse Coding Assignment – Review Scraper

Steps to run:

1. Install Python 3
2. Install dependencies:
   pip install -r requirements.txt

3. Run the script:
   python scraper.py --company zoho --start 2024-01-01 --end 2024-06-30 --source g2

4. Output:
   Reviews are saved in output.json

Supported sources:
- G2
- Capterra
Note:
Some review platforms (such as G2 and Capterra) restrict automated scraping.
When live scraping is blocked, the script gracefully falls back to sample
review data to demonstrate functionality and output structure
