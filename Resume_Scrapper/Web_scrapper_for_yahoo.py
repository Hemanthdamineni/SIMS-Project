import requests as req
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

ranks = []
names = []
start = "0"
while start != "255000":
  link = "https://sg.finance.yahoo.com/research-hub/screener/equity/?start="+start+"&count=250"
  html_text = req.get(link, headers=header).text
  # print(html_text.status_code)
  soup = bs(html_text, 'lxml')

  sections = soup.find_all('section', class_="main yf-cfn520")
  # print(f"Found {len(sections)} sections")
  for section in sections:
      # print(section.prettify())  # Print the HTML content of the section
      table = section.find('table', class_="yf-fanlnn bd")
      if table:
          rows = table.find_all('tr', class_="row yf-fanlnn")
          for row in rows:
              rank = row.find('td', class_="yf-fanlnn lpin").text
              name = row.find('td', class_="tw-text-left tw-max-w-32 yf-fanlnn").text
              # market_cap = row.find('td', class_="yf-fanlnn").text
              ranks.append(rank)
              names.append(name)
      else:
          print("Table not found in section")
  start = str(int(start) + 250)
  print(f"Scrapped {start} records")

# Create a DataFrame from the ranks and names lists
data = {'Rank': ranks, 'Name': names}
df = pd.DataFrame(data)

# Export the DataFrame to a CSV file
df.to_csv('companies_details_large.csv', index=False)
print("Data exported to companies_details.csv")