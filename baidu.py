import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
import os

def get_baidu_search_results(keyword, num_pages=1):
    links = []
    titles = []
    jianjies = []

    base_url = f'http://www.baidu.com/s?wd={urllib.parse.quote(keyword)}&pn='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    cookies = {
        'Cookie':
        'BIDUPSID=C7E32AC5A1CF89E0FFDAEE456B7AAAA2; PSTM=1682917601; BAIDUID=C7E32AC5A1CF89E0CBE4BBF0761F55EF:FG=1; BDUSS=HhLZnNkNHU5bjdudnZQMlhZby1Mbi1MRVJiMEFyRlN0UFpDUWVXN1JBU0Jtb0psSVFBQUFBJCQAAAAAAAAAAAEAAADXmaWvyOXRxbXEy8TW-QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIENW2WBDVtlS; BDUSS_BFESS=HhLZnNkNHU5bjdudnZQMlhZby1Mbi1MRVJiMEFyRlN0UFpDUWVXN1JBU0Jtb0psSVFBQUFBJCQAAAAAAAAAAAEAAADXmaWvyOXRxbXEy8TW-QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIENW2WBDVtlS; BD_UPN=12314753; H_WISE_SIDS_BFESS=282631_110085_287168_284553_287977_292509_292345_292709_292822_287703_292893_293589_293755_293961_293960_292168_275098_294063_288664_294230_287932_294107_294346_294307_292641_294435_292119_292246_294545_294706_294756_294796_294394_295018_279490_295129_294625_292241_290425_290401_289026_295341_294861_295463_295302_295502_295498_295509_295607_295772_291191_290400_277936_295908_296143_282466_295794_291026_281879_296149_293380_295845_283867_296434_294385_296466_294566_291844_296741; H_WISE_SIDS=40210_40207_40216_40222_40273_40295_40291_40288_40286_40317_40079_40364_40351_40369_40379_40407_40415; BAIDUID_BFESS=C7E32AC5A1CF89E0CBE4BBF0761F55EF:FG=1; B64_BOT=1; BA_HECTOR=alak2l8l258h84aha5240l8lr7j6sq1ivighm1s; H_PS_PSSID=40210_40207_40216_40079_40364_40351_40369_40379_40407_40415_40460_40479; ab_sr=1.0.1_N2NkYzFmYjIwMzA0ZGQyNTlhODgxOWUyMzdmYzI4ZDgzYjFhZDIxNjg2ZmRiYTQyMzQ5Y2YwMmU3ZTE4ZjA1NjdkZGRiMjMyODJhZGUzNWRiYTczY2FiNmFkMjdjYTM4ZmYwMWQ2YmJmMGEyN2FhNWE0ZTM0OTI3ZmQzOWEzYWFjZDE5NWY4NTZlNWFjZGFiNjUwZDRlOWI4ZjAxM2NiMA==; BDRCVFR[V3EOV_cRy1C]=mk3SLVN4HKm; BD_CK_SAM=1; PSINO=7; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; channel=baidusearch; baikeVisitId=3cb5d36b-d825-4c5a-bd9d-31ae3ed347b2; delPer=0; H_PS_645EC=b68bxRIKfLu%2Bi%2BxB6YWP%2B0vMVTYgE7WSDiBjQD6i7n3XmZLhYkSt%2B7RNpnSoG2QEwUYaOho; COOKIE_SESSION=162801_0_9_9_9_23_1_1_7_8_605_6_162106_0_615_0_1710904201_0_1710903586%7C9%234885250_31_1708007154%7C8; ZFY=g:B9zzSp8u2mr7zQBg39Hc:At5nNe6RKz2PxV8zMpC1YE:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598'
        }

    for i in range(num_pages * 10):  # 假设每页10个结果，根据实际情况调整
        params = {'wd': keyword, 'pn': str(i)}
        response = requests.get(base_url + str(i * 10), headers=headers,cookies=cookies)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')  # 移除from_encoding参数避免警告
            
            search_results = soup.select('.c-container')  # 示例选择器，可能需要根据实际结构更改
            for result in search_results:
                link = result.find('a', href=True)
                title = result.find('h3')
                jianjie= result.find('span', class_='content-right_8Zs40')
            

                if link and title:
                    links.append(link['href'])
                    titles.append(title.get_text().strip() if title else '')
                    jianjies.append(jianjie.get_text().strip() if jianjie else '')

        else:
            print(f"请求失败，状态码：{response.status_code}")
            break

    return links, titles,jianjies


def save_to_csv(links, titles, jianjies,filename="baidu_search_results.csv"):
    # 确保有写入权限，将文件保存在当前用户的temp目录下
    user_dir = os.path.expanduser("~")
    temp_dir = os.path.join(user_dir, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    csv_path = os.path.join(temp_dir, filename)

    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        # 添加表头
        writer.writerow(["序号", "链接", "标题","简介"])

        for index, (link, title,jianjie) in enumerate(zip(links, titles,jianjies)):
            writer.writerow([index + 1, link, title,jianjie])

    return csv_path


if __name__ == "__main__":
    keyword = "雪允"
    num_pages_to_scrape = 2  # 指定要抓取的页面数，默认为2页

    results = get_baidu_search_results(keyword, num_pages_to_scrape)
    links, titles,jianjies = results

    csv_file_path = save_to_csv(links, titles,jianjies)

    print(f"已将搜索结果保存到'{csv_file_path}'文件中。")
