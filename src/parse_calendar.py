from bs4 import BeautifulSoup
import csv

# Load the HTML content from the file
with open("test_2.html", "r") as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the specific table based on the description
# Assuming the table with "Contract Month" and "CL" is uniquely identifiable
table = soup.find('table', {'class': 'htable'})

# Extracting data from the table
data = []
if table:
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skipping the header row
        cols = row.find_all('td')
        if len(cols) == 2:  # Ensure the row has two columns
            data.append([col.text.strip() for col in cols])

# print(data[2:])
print(data[3])

# # Preparing to write the data to a CSV file
# csv_filename = "extracted_table.csv"
# with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(data)

# csv_filename

