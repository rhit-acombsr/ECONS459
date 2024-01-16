import requests
from bs4 import BeautifulSoup
import time
import csv

def save_as_html(response, filename):
    """
    Saves the content of a response object as an HTML file.

    Parameters:
    response (requests.Response): The response object from a requests call.
    filename (str): The name of the file to save the HTML content.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

def get_calendar_for(year):

    cookies = {
        'ASP.NET_SessionId': '1um2rfx32etiq2hs3ytfwvqi',
        'cookieconsent_status': 'dismiss',
        'pdfcc': '16',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'ASP.NET_SessionId=1um2rfx32etiq2hs3ytfwvqi; cookieconsent_status=dismiss; pdfcc=16',
        'Origin': 'https://www.energygps.com',
        'Referer': 'https://www.energygps.com/HomeTools/ExpiryCalendar',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # data = {
    #     'startDate': '1/13/2020',
    #     'endDate': '12/31/2024',
    #     'regions': [
    #         'CL',
    #         'NG',
    #         'HO',
    #         'RB',
    #     ],
    #     'action': 'View',
    # }
    data = {
        'startDate': '12/31/'+str(year),
        'endDate': '12/31/'+str(year+6),
        'regions': [
            'CL',
        ],
        'action': 'View',
    }

    response = requests.post('https://www.energygps.com/HomeTools/ExpiryCalendar', cookies=cookies, headers=headers, data=data)
    return response

def get_data(response):
    html_content = response.text
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
    return data

def save_data(data_in,file_name):
    # Preparing to write the data to a CSV file
    csv_filename = file_name + ".csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_in)
    return

def get_all_data():
    for year in [2020,2014,2008,2002,1996,1990,1984]:
        response = get_calendar_for(year)
        data_out = get_data(response)
        save_data(data_out,str(year))
        time.sleep(1)
        

# response = get_calendar_for(2020)
# data_out = get_data(response)
# print(data_out)
# save_as_html(response, "test.html")

get_all_data()