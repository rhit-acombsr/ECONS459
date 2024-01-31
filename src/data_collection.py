import os
import requests
# import tkinter as tk
# from tkinter import filedialog

def download_futures_data(output_directory_path):
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
    # return response
    save_xls_from_request(response, 'PET_PRI_FUT_S1_D.xls', output_directory_path)

def download_spot_data(output_directory_path):
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
    # return response
    save_xls_from_request(response, 'PET_PRI_SPT_S1_D.xls', output_directory_path)

def download_futures_calendar(output_directory_path):
    cookies = {
        'kppid': '4wqBdMFztYs',
        '__Secure-Fgp': 'BD9FFA09797CF1C42B2B05914FB324DE0B903FDBC1A5CA45BF0A64217E1B1ED6459BEE60C24C6D2FF41D22D46222C5EF8823',
        'userId': '281718',
        'cmeToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYXN0TmFtZSI6IkFjb21iIiwiY3JlYXRlZERhdGUiOjE3MDMyNjQyNjgsImZpc3ROYW1lIjoiU3RlcGhlbiIsInVub0lkIjoiVVIwMDA0MDI3MTUiLCJ1c2VyRmluZ2VycHJpbnQiOiJCQ0FFQjE2Q0UxRDU3NzFFODM0RTExQ0FFQzYzMkNDNTk3MEY4MTk5NEVDNEUyNjUxNjhFOTA3MjI5NUM0QkNFIiwiaXNzIjoiYXV0aDAiLCJ1c2VyVHlwZSI6IkIiLCJleHAiOjE3MzQ4ODY2NjgsInVzZXJJZCI6IjI4MTcxOCIsImVtYWlsIjoiYWNvbWJzckByb3NlLWh1bG1hbi5lZHUifQ.68oTeynDfyKcAQn7B_wJx28UVmCznwm55UjSC7yTc24',
        'userinfo': '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYXN0TmFtZSI6IkFjb21iIiwiY3JlYXRlZERhdGUiOjE3MDMyNjQyNjgsImZpc3ROYW1lIjoiU3RlcGhlbiIsInVub0lkIjoiVVIwMDA0MDI3MTUiLCJ1c2VyRmluZ2VycHJpbnQiOiJCQ0FFQjE2Q0UxRDU3NzFFODM0RTExQ0FFQzYzMkNDNTk3MEY4MTk5NEVDNEUyNjUxNjhFOTA3MjI5NUM0QkNFIiwiaXNzIjoiYXV0aDAiLCJ1c2VyVHlwZSI6IkIiLCJleHAiOjE3MzQ4ODY2NjgsInVzZXJJZCI6IjI4MTcxOCIsImVtYWlsIjoiYWNvbWJzckByb3NlLWh1bG1hbi5lZHUifQ.68oTeynDfyKcAQn7B_wJx28UVmCznwm55UjSC7yTc24","userId":"281718","userName":"Stephen+Acomb","onePass":"UR000402715","email":"acombsr@rose-hulman.edu","firstName":"Stephen","lastName":"Acomb","firstLogIn":false,"jobRole":"Student","company":"Rose-Hulman+Institute+of+Technology","companyType":"University%2FEducation","country":"US","isLite":false,"loginFrom":"/markets/energy/crude-oil/light-sweet-crude.calendar.html","hashedEmail":"0f81ee7f9836b7dc8b42059f1e2cfc44457d84ea7d5c41a7044a613df9dfcbd6"}',
        'AKA_A2': 'A',
        'ak_bmsc': 'DF663FA6782A736639DF9FB10FC7AEC2~000000000000000000000000000000~YAAQCKTAF7/YlvWMAQAAtGN5EhYsI6E7O3oOLW6QAh4a2hZnnaE0P/lWOD6b/n6JWwo61P9xWqFfBw6ezlLoMu9vtYzaIkctyTgsMZurxkWacedo/EoZqKo7WD+7XFl3EhJwQT97jz5uKXgfA/kxltIckYZrihZk3FcXQqGQ7XSMTLkOHSzlRlTtpiU586Pzh4lqw1glFzGQEEiJF5MKW0UQ77+d6U0Q6thT0xv0R16HBLC+y5bBqs/L4nyU6jN3FeB2BJB+hzDD41+clOlf0GwBtzoBDQu1wqa5DG/X9ZcX7OTfMeSimZmF73+3PdA/pdeNOSWLJjwgFEGCtft3wnReyhw+dnmOgrldJKTG9otgOjqKNxrn3sSUyugj6IhxHy+DUlmonJOAybiq',
        'pdfcc': '1',
        'OptanonAlertBoxClosed': '2024-01-16T13:32:43.959Z',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Jan+16+2024+08%3A32%3A43+GMT-0500+(Eastern+Standard+Time)&version=202401.1.0&isIABGlobal=false&hosts=&consentId=3a1b10dd-6c97-4186-bead-11122994ec60&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=US%3BIN&AwaitingReconsent=true&browserGpcFlag=0',
        'bm_mi': '6B4249456C9DFE099BD21A3845123738~YAAQCKTAFzDblvWMAQAAfpt5EhbI+KTmev5GgxMeNmAY3SWN79NKH1ytLDyVD1robn37XiYrf7GcGLwAkG/GD1QohmkepD5EO8zOZnj7+qQriQ2qu7k7rxBaResSNOTc+sYEemqwazeSChvgRr6jQPsp2fdhVrYUG7S9QHtKM8J5dMC/C9BisokjuRtV7/s5L2LyKzvuVU1bfc002xdETz/ECTBgQ9mlhpUBcwKphJO9sPBbmQdtQec7nc6mzT99EXQLi9m32TShUqzLqGxrf8/MsWIxpp+yFB/XFtS1lz9+PF9PSO2cH7O8GgDba67ww7jsrgYZnMQEn2boZT8qnC9wH+LRbx96FFHcJp9ruuORl1FEqPeyHUlqxE9026yauwMLUzELsYpJXjfj6mNXG3UnJQ==~1',
        'bm_sv': 'BB391026E3C5930E673E1622B0E426C8~YAAQCKTAFzHblvWMAQAAfpt5EhbnvjnOWvtuqDxaRm+FtD3v+2CEBW7WwSfis2ryzGl4FvfDpv/rrBoiMgrMbTAytRid0ybBZDC1a/a/sBZ+LhIBSqMpJ68RaV8R81QJU3ZHh5CBkm8pZFVUCAzVXwoohB3/SKwImJcKFXToTR/9AC59Fe5UsqwJZl3311FezNnrNuSgRgspVzD7p0jC6hgNDbUV15FmlGnldl608nhD3X1A5lsgOetaRCB+WijMK04=~1',
    }

    headers = {
        'authority': 'www.cmegroup.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'kppid=4wqBdMFztYs; __Secure-Fgp=BD9FFA09797CF1C42B2B05914FB324DE0B903FDBC1A5CA45BF0A64217E1B1ED6459BEE60C24C6D2FF41D22D46222C5EF8823; userId=281718; cmeToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYXN0TmFtZSI6IkFjb21iIiwiY3JlYXRlZERhdGUiOjE3MDMyNjQyNjgsImZpc3ROYW1lIjoiU3RlcGhlbiIsInVub0lkIjoiVVIwMDA0MDI3MTUiLCJ1c2VyRmluZ2VycHJpbnQiOiJCQ0FFQjE2Q0UxRDU3NzFFODM0RTExQ0FFQzYzMkNDNTk3MEY4MTk5NEVDNEUyNjUxNjhFOTA3MjI5NUM0QkNFIiwiaXNzIjoiYXV0aDAiLCJ1c2VyVHlwZSI6IkIiLCJleHAiOjE3MzQ4ODY2NjgsInVzZXJJZCI6IjI4MTcxOCIsImVtYWlsIjoiYWNvbWJzckByb3NlLWh1bG1hbi5lZHUifQ.68oTeynDfyKcAQn7B_wJx28UVmCznwm55UjSC7yTc24; userinfo={"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYXN0TmFtZSI6IkFjb21iIiwiY3JlYXRlZERhdGUiOjE3MDMyNjQyNjgsImZpc3ROYW1lIjoiU3RlcGhlbiIsInVub0lkIjoiVVIwMDA0MDI3MTUiLCJ1c2VyRmluZ2VycHJpbnQiOiJCQ0FFQjE2Q0UxRDU3NzFFODM0RTExQ0FFQzYzMkNDNTk3MEY4MTk5NEVDNEUyNjUxNjhFOTA3MjI5NUM0QkNFIiwiaXNzIjoiYXV0aDAiLCJ1c2VyVHlwZSI6IkIiLCJleHAiOjE3MzQ4ODY2NjgsInVzZXJJZCI6IjI4MTcxOCIsImVtYWlsIjoiYWNvbWJzckByb3NlLWh1bG1hbi5lZHUifQ.68oTeynDfyKcAQn7B_wJx28UVmCznwm55UjSC7yTc24","userId":"281718","userName":"Stephen+Acomb","onePass":"UR000402715","email":"acombsr@rose-hulman.edu","firstName":"Stephen","lastName":"Acomb","firstLogIn":false,"jobRole":"Student","company":"Rose-Hulman+Institute+of+Technology","companyType":"University%2FEducation","country":"US","isLite":false,"loginFrom":"/markets/energy/crude-oil/light-sweet-crude.calendar.html","hashedEmail":"0f81ee7f9836b7dc8b42059f1e2cfc44457d84ea7d5c41a7044a613df9dfcbd6"}; AKA_A2=A; ak_bmsc=DF663FA6782A736639DF9FB10FC7AEC2~000000000000000000000000000000~YAAQCKTAF7/YlvWMAQAAtGN5EhYsI6E7O3oOLW6QAh4a2hZnnaE0P/lWOD6b/n6JWwo61P9xWqFfBw6ezlLoMu9vtYzaIkctyTgsMZurxkWacedo/EoZqKo7WD+7XFl3EhJwQT97jz5uKXgfA/kxltIckYZrihZk3FcXQqGQ7XSMTLkOHSzlRlTtpiU586Pzh4lqw1glFzGQEEiJF5MKW0UQ77+d6U0Q6thT0xv0R16HBLC+y5bBqs/L4nyU6jN3FeB2BJB+hzDD41+clOlf0GwBtzoBDQu1wqa5DG/X9ZcX7OTfMeSimZmF73+3PdA/pdeNOSWLJjwgFEGCtft3wnReyhw+dnmOgrldJKTG9otgOjqKNxrn3sSUyugj6IhxHy+DUlmonJOAybiq; pdfcc=1; OptanonAlertBoxClosed=2024-01-16T13:32:43.959Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+16+2024+08%3A32%3A43+GMT-0500+(Eastern+Standard+Time)&version=202401.1.0&isIABGlobal=false&hosts=&consentId=3a1b10dd-6c97-4186-bead-11122994ec60&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=US%3BIN&AwaitingReconsent=true&browserGpcFlag=0; bm_mi=6B4249456C9DFE099BD21A3845123738~YAAQCKTAFzDblvWMAQAAfpt5EhbI+KTmev5GgxMeNmAY3SWN79NKH1ytLDyVD1robn37XiYrf7GcGLwAkG/GD1QohmkepD5EO8zOZnj7+qQriQ2qu7k7rxBaResSNOTc+sYEemqwazeSChvgRr6jQPsp2fdhVrYUG7S9QHtKM8J5dMC/C9BisokjuRtV7/s5L2LyKzvuVU1bfc002xdETz/ECTBgQ9mlhpUBcwKphJO9sPBbmQdtQec7nc6mzT99EXQLi9m32TShUqzLqGxrf8/MsWIxpp+yFB/XFtS1lz9+PF9PSO2cH7O8GgDba67ww7jsrgYZnMQEn2boZT8qnC9wH+LRbx96FFHcJp9ruuORl1FEqPeyHUlqxE9026yauwMLUzELsYpJXjfj6mNXG3UnJQ==~1; bm_sv=BB391026E3C5930E673E1622B0E426C8~YAAQCKTAFzHblvWMAQAAfpt5EhbnvjnOWvtuqDxaRm+FtD3v+2CEBW7WwSfis2ryzGl4FvfDpv/rrBoiMgrMbTAytRid0ybBZDC1a/a/sBZ+LhIBSqMpJ68RaV8R81QJU3ZHh5CBkm8pZFVUCAzVXwoohB3/SKwImJcKFXToTR/9AC59Fe5UsqwJZl3311FezNnrNuSgRgspVzD7p0jC6hgNDbUV15FmlGnldl608nhD3X1A5lsgOetaRCB+WijMK04=~1',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'productId': '425',
    }

    response = requests.get(
        'https://www.cmegroup.com/CmeWS/mvc/ProductCalendar/Download.xls',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    # return response
    save_xls_from_request(response, 'ProductCalendar.xls', output_directory_path)

def save_xls_from_request(request, filename, output_directory_path):
    # Check if the request was successful
    if request.status_code == 200:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)
        
        # Define the path for the output file
        output_file_path = os.path.join(output_directory_path, filename)
        
        # Write the content to an Excel file
        with open(output_file_path, 'wb') as file:
            file.write(request.content)
        print(f"File saved successfully at {output_file_path}")
    else:
        print("Failed to download the data. Status code:", request.status_code)

# Usage example:
data_output_directory_path = "C:\_Data_Out"
# data_output_directory_path = filedialog.askdirectory()
download_futures_data(data_output_directory_path)
download_spot_data(data_output_directory_path)
request = download_futures_calendar(data_output_directory_path)
print("All done!")
