import requests
from bs4 import BeautifulSoup

# Define the target URL and page limit (adjust if needed)
url = "https://stackoverflow.com/questions/tagged/reactjs"
page_limit = 5

def get_reactjs_queries(url, page_limit):
  """
  Extracts React.js queries from Stack Overflow tagged page using Beautiful Soup.

  Args:
      url: The URL of the Stack Overflow tagged page.
      page_limit: The maximum number of pages to scrape (avoid overloading servers).

  Returns:
      A list of extracted React.js queries.
  """

  extracted_queries = []

  # Loop through pagination pages
  for page_number in range(1, page_limit + 1):
    # Build URL with page number
    paginated_url = f"{url}?page={page_number}"

    # Make a GET request and parse the HTML response
    response = requests.get(paginated_url)
    soup = BeautifulSoup(response.content, "lxml")

    # Find all elements containing queries (question titles)
    queries = soup.findAll("div", class_="questions")

    # Extract and store the query text
    for query in queries:
      title_element = query.find("a", class_="question-hyperlink")
      if title_element:
        extracted_queries.append(title_element.text.strip())

  return extracted_queries

# Extract queries from multiple pages
reactjs_queries = get_reactjs_queries(url, page_limit)

# Print the extracted queries
print("Extracted React.js queries:")
for query in reactjs_queries:
  print(f"- {query}")

# You can further store the queries in a file or database for later use
