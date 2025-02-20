def fetch_song():
    '抓取歌单信息'
    import requests, json

    url = 'https://api.starlwr.com/songlist/getView'
    headers = {
        'content-type': 'application/json', 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        }

    payload = {
        'url': "wasesong.songlist.cc",
        'uid': 0
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    #response = requests.post(url, data=json.dumps(payload), headers=headers)
    res_json = response.json()
    #print(json.dumps(res_json))
    return res_json

def convert_song(res_json):
    '转换格式'
    import pandas as pd
    data = pd.DataFrame(res_json['data']['songs'])

    # 标签列
    import numpy
    remarks = []
    for idx, i in enumerate(data['guard']):
        remark = ''
        # SC等级
        price = data['pay'][idx]
        if not numpy.isnan(price):
            remark += f"SC={int(price)}；"

        # 航海等级
        if i == 1:
            remark += "舰长；"
        elif i == 2:
            remark += "提督；"
        elif i == 3:
            remark += "总督；"

        # 语言
        remark += data['language'][idx]

        # 完工
        remarks.append(remark)
    tags_column = pd.Series(remarks, name = "remarks")

    # 导出数据
    empty_column = pd.Series([' '] * len(data), name = "")
    zero_column = pd.Series([0] * len(data), name = "")
    export_data = pd.concat([data['name'], data['singer'], data['remark'], tags_column, zero_column, empty_column], axis=1, keys=[
        '歌曲名','艺术家','备注','标签','演唱次数','最近演唱时间'])
    return export_data

def export_xlsx(export_data):
    # 导出pd data到xlsx
    import datetime
    # 获取时间
    date_now = datetime.datetime.now().strftime(r"%y%m%d_%H%M%S")
    filename = f'歌单{date_now}.xlsx'
    export_data.to_excel(filename, index=False)
    return filename

def main():
    import json
    with open("config.json", encoding='utf-8') as f:
        config = json.load(f)
    url = config['url']

    # 处理
    print(f"正在抓取最新歌单: {url}")
    song_json = fetch_song(url)
    with open("songs.json", 'w') as f:
        json.dump(song_json, f)
    print("格式转换中...")
    export_data = convert_song(song_json)

    # 导出
    filename = export_xlsx(export_data)
    print(f"歌单'{filename}'导出完成,请从reito点歌姬导入使用")

if __name__ == "__main__":
    print("Author: 卤鹅菌\nRepo: https://github.com/lue-trim/songlist-reito.git")
    main()
