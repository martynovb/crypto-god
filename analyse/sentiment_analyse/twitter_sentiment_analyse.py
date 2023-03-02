import requests
from bs4 import BeautifulSoup

url = "https://twitter.com/search?q=bitcoin&src=typed_query"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all the div elements with class "css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"
divs = soup.find_all("div", {"class": "css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"})

# Print the text content of each div
for div in divs:
    print(div.get_text())