import requests
import urllib.request
import re
import os
import ssl
# ssh 憑證設定
ssl._create_default_https_context = ssl._create_unverified_context
# 抓取關鍵字
keyword = input("Please input search keyword: ")
search_keyword = {'tbm': 'isch', 'q': str(keyword)}
print("search_keyword: ",end="")
print(search_keyword)
# 建立爬蟲搜尋資料
url = f"https://www.google.com/search?{urllib.parse.urlencode(search_keyword)}/"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}  
#print("url: " + url)

# 建立連線
req = urllib.request.Request(url, headers = headers)
conn = urllib.request.urlopen(req)
# 取回爬蟲資料
data = conn.read()
# 一些參數初始化設定
pattern = 'img data-src="\S*"'
img_url_list = []
folderName = str(keyword) + "_images"
dataCount = 0
downloadFlag = "n"

# 透過pattern來篩選取回的資料，
for match in re.finditer(pattern, str(data)):
    img_url_list.append(match.group())

dataCount = len(img_url_list)
if(dataCount >= 1):
    print("find "+ str(len(img_url_list)) + " data.")
    downloadFlag = input("Download the data and create folder to the current directory. (y/n): ")
    if(downloadFlag == "y"):
        if not os.path.exists(str(keyword) + "_images"): # 偵測資料夾
            os.mkdir(str(keyword) + "_images") # 建立資料夾
            print(f"New folder '{folderName}' create.")
        else:
            print(f"find folder '{folderName}'")

        for index,data in enumerate(img_url_list):
            data = data.replace("img data-src=","") #將多餘的字串去除
            data = data.replace("\"","") #將多餘的字串去除

            img_url_list[index] = data #將處理後的字串放回
            img = requests.get(img_url_list[index]) #透過URL載圖片
            with open(str(keyword) + "_images/" + str(keyword) +str(index+1) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
                file.write(img.content)  # 寫入圖片的二進位碼
        print("done.")
    elif(downloadFlag == "n"):
        print("Bye.")
    
else:
    print("[Data error] Can't find any data.")









