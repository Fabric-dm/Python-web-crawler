import requests
import json
import csv
import os
import pandas as pd

# 检查路径是否存在，如果不存在就创建
if not os.path.exists('./luoyang/'):
    os.makedirs('./luoyang/')

    
postUrl = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"

# 将景点poiId和名称添加到此处
urls = [
    ['77498', '龙门石窟（人文古迹）'],
    ['77567', '白马寺（人文古迹）'],
    ['77806', '老君山（山水景点）'],
    ['61114449','隋唐洛阳城应天门遗址(人文古迹)'],
    ['10542669','隋唐洛阳城国家遗址公园天堂明堂景区(人文古迹)'],
    ['89920','洛阳博物馆(人文古迹)'],
    ['82475','中国国花园(山水景点)'],
    ['36428655','洛邑古城'],
    ['77805','鸡冠洞'],
    ['77784','白云山'],
    ['97248','龙潭大峡谷'],
    ['101970','关林庙'],
    ['71496012','隋唐洛阳城九洲池'],
    ['86233','重渡沟风景区'],
    ['82371','国家牡丹园'],
    ['77813','王城公园'],
]

for id in urls:
    print("正在爬取景点：", id[1])
    # 通过返回值判断总评论数，每页9条，计算出总页数，对大于2000条的数据只爬取两千条
    data_pre = {
        "arg": {
            "channelType": 2,
            "collapseType": 0,
            "commentTagId": 0,
            "pageIndex": 1,
            "pageSize": 10,
            "poiId": id[0],
            "sourceType": 1,
            "sortType": 3,
            "starType": 0
        },
        "head": {
            "cid": "09031049217606079171",
            "ctok": "",
            "cver": "1.0",
            "lang": "01",
            "sid": "8888",
            "syscode": "09",
            "auth": "",
            "xsid": "",
            "extension": []
        }
    }

    html = requests.post(postUrl, data=json.dumps(data_pre)).text
    html = json.loads(html)

    # 确定总页数总页数
    total_page = int(html['result']['totalCount'] / 10)
    if total_page > 200:
        total_page = 200
    # 遍历查询评论
    print("总页数:", total_page, "爬取中")

    # 创建写入csv文件
    path = './luoyang/' + str(id[1]) + '.csv'
    xuhao = 0
    with open(path, 'w', newline='', encoding='utf-8') as f:
        file = csv.writer(f)
        file.writerow(['序号', '景区ID', '景区名称', '评论','游客评分','评论时间'])

        # 存储已抓取的评论
        comments = set()
        
        for page in range(1, int(total_page) + 1):
            data = {
                "arg": {
                    "channelType": 2,
                    "collapseType": 0,
                    "commentTagId": 0,
                    "pageIndex": page,
                    "pageSize": 10,
                    "poiId": id[0],
                    "sourceType": 1,
                    "sortType": 3,
                    "starType": 0
                },
                "head": {
                    "cid": "09031069112760102754",
                    "ctok": "",
                    "cver": "1.0",
                    "lang": "01",
                    "sid": "8888",
                    "syscode": "09",
                    "auth": "",
                    "xsid": "",
                    "extension": []
                }
            }
            html = requests.post(postUrl, data=json.dumps(data)).text
            html = json.loads(html)
            
            # 获取评论
            for j in range(10):
                result1 = html['result']['items'][j]['content']
                 # 删除重复评论
                if result1 in comments:
                    continue
                comments.add(result1)

                result2 = html['result']['items'][j]['publishTypeTag']
                result3 = html['result']['items'][j]['score']
                 # 删除有缺失项的数据
                if result1 == "" or result2 == ""or result3 == "":
                    continue
                
                file.writerow([xuhao, id[0], id[1], result1,result3,result2])
                print([xuhao, id[0], id[1], result1,result3,result2])
                xuhao += 1
    print(id[1], "爬取完成")
