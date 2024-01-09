import os
import requests
import tkinter as tk
from tkinter import filedialog

def download_futures_data():
    cookies = {
        'ak_bmsc': '8B98D98F4383E3C03F63FBAA95471769~000000000000000000000000000000~YAAQHMIcuJij4WeMAQAAnzXL7haNoOJ3LhQrvQ+7UA7tBcUtgDPDyeeZ38hnSy7np5eCh7OnnWFnvNAqPpb8lHqKrkIr6KnCgG4UJusA7qAjZh5L3ZNcefV4dYFLnikOZ6ZsPm/qlJHprkHSZXB9GFlkLl0wO1yCkvP9E6IAJzS7gVXorKH2s9+tMZYAXxIlMmXyRYfKtIdT92RTwQw90pfzMVIwRlQOr9JcfW+/R1hdEv1EpRgXJl1hTg595cFwLRyngJczsU4dgcgVAojm3IfSweL3hVaO6LKpVsy2sARQImGDsckyBkBXBJG2O9fliODRohsNbp/9UXZh/jHp91kdAW/pyFWFbrLZASjV9/Juft1AMKIh7bCN5mMm',
        'bm_mi': '068BCE439C8DDC698826CC3C0EEACCD6~YAAQHMIcuJuj4WeMAQAAIzbL7haWCOA7Vr7/1X8+VHgMS6OGmsmm45fop4hpi3vtLFSgEpmj1381ixaUg46ed1pmxUVlS88g6lPknTOJxFEW80yurTTDLwniGnzZGqOPJicK0jtmlTXWXabZVFrxCKxKF0MALt5jPH5vxCeCKnvw+86tQQIax/iFBuNNf7UpUTfY71AeDGfUGkhPYYlHCIeacq66HS60Y5wZ9oOMyRSHRCVpJiEcvRB4kawOfXv8SsBDMwpnu2lj/5skCdIni7lBF353stXHH/7T2RWT2Er0vt7zlNeZi0sAR8lhasojXSvmTCDFFzbzYNQk1u/umT2FKKPL+9FDPRU4z0D150tv~1',
        'pdfcc': '1',
        'bm_sv': '815483752A6830B02040956EDBF9B5D9~YAAQHMIcuKaj4WeMAQAAIjfL7haokwMZ6HotaGXIlVLm7r357sI4uQFVDMQBOmIkzXLjMmNxupllicGxtknf52BzmWmVheqRwPxp5nPnHDNuhBv8TtWrpYGyHnXKEYF/PbMHkTHQ1FABntnzx8Ddx8hOZe+WWKeJjTQ/sqKYwElcNQX1thg6yp9O9plGxEHSK/JJeQt94AWy+VxEdU82EjZQyl8CDCDn7Ig/VKy1xTtQecLuSfNtfItP9GvD~1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'ak_bmsc=8B98D98F4383E3C03F63FBAA95471769~000000000000000000000000000000~YAAQHMIcuJij4WeMAQAAnzXL7haNoOJ3LhQrvQ+7UA7tBcUtgDPDyeeZ38hnSy7np5eCh7OnnWFnvNAqPpb8lHqKrkIr6KnCgG4UJusA7qAjZh5L3ZNcefV4dYFLnikOZ6ZsPm/qlJHprkHSZXB9GFlkLl0wO1yCkvP9E6IAJzS7gVXorKH2s9+tMZYAXxIlMmXyRYfKtIdT92RTwQw90pfzMVIwRlQOr9JcfW+/R1hdEv1EpRgXJl1hTg595cFwLRyngJczsU4dgcgVAojm3IfSweL3hVaO6LKpVsy2sARQImGDsckyBkBXBJG2O9fliODRohsNbp/9UXZh/jHp91kdAW/pyFWFbrLZASjV9/Juft1AMKIh7bCN5mMm; bm_mi=068BCE439C8DDC698826CC3C0EEACCD6~YAAQHMIcuJuj4WeMAQAAIzbL7haWCOA7Vr7/1X8+VHgMS6OGmsmm45fop4hpi3vtLFSgEpmj1381ixaUg46ed1pmxUVlS88g6lPknTOJxFEW80yurTTDLwniGnzZGqOPJicK0jtmlTXWXabZVFrxCKxKF0MALt5jPH5vxCeCKnvw+86tQQIax/iFBuNNf7UpUTfY71AeDGfUGkhPYYlHCIeacq66HS60Y5wZ9oOMyRSHRCVpJiEcvRB4kawOfXv8SsBDMwpnu2lj/5skCdIni7lBF353stXHH/7T2RWT2Er0vt7zlNeZi0sAR8lhasojXSvmTCDFFzbzYNQk1u/umT2FKKPL+9FDPRU4z0D150tv~1; pdfcc=1; bm_sv=815483752A6830B02040956EDBF9B5D9~YAAQHMIcuKaj4WeMAQAAIjfL7haokwMZ6HotaGXIlVLm7r357sI4uQFVDMQBOmIkzXLjMmNxupllicGxtknf52BzmWmVheqRwPxp5nPnHDNuhBv8TtWrpYGyHnXKEYF/PbMHkTHQ1FABntnzx8Ddx8hOZe+WWKeJjTQ/sqKYwElcNQX1thg6yp9O9plGxEHSK/JJeQt94AWy+VxEdU82EjZQyl8CDCDn7Ig/VKy1xTtQecLuSfNtfItP9GvD~1',
        'Referer': 'https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm',
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
    
    response = requests.get('https://www.eia.gov/dnav/pet/xls/PET_PRI_FUT_S1_D.xls', cookies=cookies, headers=headers)
    return response

def save_xls_from_request(request, output_directory_path):
    # Check if the request was successful
    if request.status_code == 200:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)
        
        # Define the path for the output file
        output_file_path = os.path.join(output_directory_path, 'futures_data.xls')
        
        # Write the content to an Excel file
        with open(output_file_path, 'wb') as file:
            file.write(request.content)
        print(f"File saved successfully at {output_file_path}")
    else:
        print("Failed to download the data. Status code:", request.status_code)

def download_spot_data():
    cookies = {
        'ak_bmsc': '8B98D98F4383E3C03F63FBAA95471769~000000000000000000000000000000~YAAQHMIcuJij4WeMAQAAnzXL7haNoOJ3LhQrvQ+7UA7tBcUtgDPDyeeZ38hnSy7np5eCh7OnnWFnvNAqPpb8lHqKrkIr6KnCgG4UJusA7qAjZh5L3ZNcefV4dYFLnikOZ6ZsPm/qlJHprkHSZXB9GFlkLl0wO1yCkvP9E6IAJzS7gVXorKH2s9+tMZYAXxIlMmXyRYfKtIdT92RTwQw90pfzMVIwRlQOr9JcfW+/R1hdEv1EpRgXJl1hTg595cFwLRyngJczsU4dgcgVAojm3IfSweL3hVaO6LKpVsy2sARQImGDsckyBkBXBJG2O9fliODRohsNbp/9UXZh/jHp91kdAW/pyFWFbrLZASjV9/Juft1AMKIh7bCN5mMm',
        'bm_mi': '068BCE439C8DDC698826CC3C0EEACCD6~YAAQdWDcF1sLNF6MAQAAAIXT7hbbtjiMnSzUnMVOATmJ2WU482VZ2rDGVq/GbR1CDDRSaXaIQCBbZSXwJd55yAqaNNeKqjsMUpcYoGmny4msY6EcXA+zlZ64A596Qt3f1mVmtyLHx0hYyFGTG+YQoF1TLlCBEFfhs2wJEYTMxQbWgSo/K4vpE7MZrreKw+pKJ3cZtzJni85fqtzzO1ZUuwL8glsiwJWDuyLyomRzRRbsb0BBxOXQVlBhcMjxKl4L3VU/M+eesZMVBpOkqysSx7EQ6XfffM0Z7UKI9fHgpvdW6CIct3B1PWqYKiNy/E4ysJLASCNET0rVP+zgFMsU7gXZH8yZ1bbK~1',
        'pdfcc': '2',
        'bm_sv': '815483752A6830B02040956EDBF9B5D9~YAAQdWDcF2cLNF6MAQAAlobT7hb6iPaxRwyd7kYQ6S9z7yX6gC1ylBk/NAtv5uePNeZ4x3M4iWIZYKa9K7N070gRUMTB81hPq0tVztZKun+CzCkdcIdouV1cLUCwO27f4FK7TzQFqzLZw7D7DP+LCfacrCNE0csJwtwIKRYroRp0V6xP7fpXF0CrushncVjGux7V9HP3g3akw5T+0I2cdfTb9oVhsQArQWxvy+inrmYHmWDnmgpnfRtviUSmBQ==~1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'ak_bmsc=8B98D98F4383E3C03F63FBAA95471769~000000000000000000000000000000~YAAQHMIcuJij4WeMAQAAnzXL7haNoOJ3LhQrvQ+7UA7tBcUtgDPDyeeZ38hnSy7np5eCh7OnnWFnvNAqPpb8lHqKrkIr6KnCgG4UJusA7qAjZh5L3ZNcefV4dYFLnikOZ6ZsPm/qlJHprkHSZXB9GFlkLl0wO1yCkvP9E6IAJzS7gVXorKH2s9+tMZYAXxIlMmXyRYfKtIdT92RTwQw90pfzMVIwRlQOr9JcfW+/R1hdEv1EpRgXJl1hTg595cFwLRyngJczsU4dgcgVAojm3IfSweL3hVaO6LKpVsy2sARQImGDsckyBkBXBJG2O9fliODRohsNbp/9UXZh/jHp91kdAW/pyFWFbrLZASjV9/Juft1AMKIh7bCN5mMm; bm_mi=068BCE439C8DDC698826CC3C0EEACCD6~YAAQdWDcF1sLNF6MAQAAAIXT7hbbtjiMnSzUnMVOATmJ2WU482VZ2rDGVq/GbR1CDDRSaXaIQCBbZSXwJd55yAqaNNeKqjsMUpcYoGmny4msY6EcXA+zlZ64A596Qt3f1mVmtyLHx0hYyFGTG+YQoF1TLlCBEFfhs2wJEYTMxQbWgSo/K4vpE7MZrreKw+pKJ3cZtzJni85fqtzzO1ZUuwL8glsiwJWDuyLyomRzRRbsb0BBxOXQVlBhcMjxKl4L3VU/M+eesZMVBpOkqysSx7EQ6XfffM0Z7UKI9fHgpvdW6CIct3B1PWqYKiNy/E4ysJLASCNET0rVP+zgFMsU7gXZH8yZ1bbK~1; pdfcc=2; bm_sv=815483752A6830B02040956EDBF9B5D9~YAAQdWDcF2cLNF6MAQAAlobT7hb6iPaxRwyd7kYQ6S9z7yX6gC1ylBk/NAtv5uePNeZ4x3M4iWIZYKa9K7N070gRUMTB81hPq0tVztZKun+CzCkdcIdouV1cLUCwO27f4FK7TzQFqzLZw7D7DP+LCfacrCNE0csJwtwIKRYroRp0V6xP7fpXF0CrushncVjGux7V9HP3g3akw5T+0I2cdfTb9oVhsQArQWxvy+inrmYHmWDnmgpnfRtviUSmBQ==~1',
        'Referer': 'https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm',
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
    
    response = requests.get('https://www.eia.gov/dnav/pet/xls/PET_PRI_SPT_S1_D.xls', cookies=cookies, headers=headers)
    return response

# Usage example:
data_output_directory_path = "C:\_Data_Out"
# data_output_directory_path = filedialog.askdirectory()
# print(data_output_directory_path)
request = download_futures_data()
save_xls_from_request(request,data_output_directory_path)
