import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

userAgent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
#取得User-Agent資格
headers = {
    #User-Agent固定寫法
    'User-Agent': userAgent,
    'Referer': f'https://www.104.com.tw/job/7g8jb'
}

jobOpeningList = []
jobCompanyList = []
jobDescriptionList = []
jobName_Url_List = []

jobURLList = []

for page in range(1, 10):

    url = 'https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001000&kwop=7&keyword=%E6%95%B8%E6%93%9A%E5%88%86%E6%9E%90&scmin=50000&scstrict=1&page={}'.format(page)

    ss = requests.session()
    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    jobSoupList = soup.select('a[class="js-job-link"]')


    for i in jobSoupList:
        # 職稱
        #print(i.text)
        jobOpeningList.append(i.text)
        #網址
        jobUrl = "https:" + i['href']
        #print(jobUrl)
        jobURLList.append(jobUrl)
        #jobName_Url_Dic.setdefault(i.text, "https://www.104.com.tw/job/ajax/content/" + i['href'][21:26])
        jobName_Url_List.append("https://www.104.com.tw/job/ajax/content/" + i['href'][21:26])
        #print("https://www.104.com.tw/job/ajax/content/" + i['href'][21:26])
    print('Page {} ========================================================'.format(page))

    # Job Detail / content

for singleJobDetail in jobName_Url_List:

    # url2 = 'https://www.104.com.tw/job/ajax/content/7g8jb'
    url2 = singleJobDetail
    res2 = ss.get(url2, headers=headers)
    jsonData = res2.json() # list of article object
    jonContent = jsonData['data']['jobDetail']['jobDescription']
    jobDescriptionList.append(jonContent.replace('\n', ''))
    #print(jonContent)
    companyName = jsonData['data']['header']['custName']
    jobCompanyList.append(companyName)
    # print(companyName) #公司名
    #
    #print('========================================================')
# print(jsonData['data']['jobDetail'])
# for i in jsonData['data']['jobDetail']['salary']:
#     print(i)

# write to csv
# print(len(jobCompanyList))
# print(len(jobOpeningList))
# print(len(jobDescriptionList))
# print(len(jobName_Url_List))
df = pd.DataFrame({
    'Company': jobCompanyList,
    'Job Opening': jobOpeningList,
    'Job Content': jobDescriptionList,
    'Job URL': jobURLList
})

df.to_csv('C:\\Users\\TibeMe_user\\Desktop\\CLASS\\pyETL\\homework.csv', encoding='utf_8_sig')