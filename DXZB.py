import time
import os
import re
import base64
import datetime
import requests
import threading
from queue import Queue
from datetime import datetime


# 线程安全的队列，用于存储下载任务
task_queue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

urls = ["Guangzhou", "Shenzhen", "Foshan", "Qingyuan", "Shaoguan", "Jiangmen", "Yangjiang", "Maoming", "Zhanjiang","Huizhou", "Dongguan", "Zhuhai", "Shantou","Jieyang", "Chaozhou", "Meizhou", "Heyuan", "Shanwei", "Zhongshan", "Yunfu"]
channelsx = [
"广东卫视超清,http://8.8.8.8:8/udp/239.77.0.166:5146",
"广东珠江超清,http://8.8.8.8:8/udp/239.77.0.114:5146",
"广东新闻高清,http://8.8.8.8:8/udp/239.77.0.173:5146",
"广东民生高清,http://8.8.8.8:8/udp/239.77.0.225:5146",
"广东体育超清,http://8.8.8.8:8/udp/239.77.0.168:5146",
"经济科教超清,http://8.8.8.8:8/udp/239.77.0.167:5146",
"大湾区卫视高清,http://8.8.8.8:8/udp/239.77.0.215:5146",
"广东综艺 4K,http://8.8.8.8:8/udp/239.77.1.237:5146",
"广东影视高清,http://8.8.8.8:8/udp/239.77.0.217:5146",
"广东少儿高清,http://8.8.8.8:8/udp/239.77.0.250:5146",
"嘉佳卡通高清,http://8.8.8.8:8/udp/239.77.0.179:5146",
"南方购物-精选,http://8.8.8.8:8/udp/239.77.0.19:5146",
"南方购物,http://8.8.8.8:8/udp/239.77.0.22:5146",
"岭南戏曲高清,http://8.8.8.8:8/udp/239.77.0.122:5146",
"现代教育高清,http://8.8.8.8:8/udp/239.77.0.213:5146",
"广州综合高清,http://8.8.8.8:8/udp/239.253.43.71:5146",
"广州新闻高清,http://8.8.8.8:8/udp/239.253.43.72:5146",
"广州影视高清,http://8.8.8.8:8/udp/239.253.43.73:5146",
"广州法治高清,http://8.8.8.8:8/udp/239.253.43.74:5146",
"南国都市 4K,http://8.8.8.8:8/udp/239.253.43.99:5146",
"深圳卫视超清,http://8.8.8.8:8/udp/239.77.0.130:5146",
"深圳都市频道高清,http://8.8.8.8:8/udp/239.77.1.176:5146",
"深圳电视剧频道高清,http://8.8.8.8:8/udp/239.77.1.177:5146",
"深圳财经生活高清,http://8.8.8.8:8/udp/239.77.1.242:5146",
"深圳娱乐频道高清,http://8.8.8.8:8/udp/239.77.1.243:5146",
"深圳体育健康高清,http://8.8.8.8:8/udp/239.77.1.128:5146",
"深圳少儿频道高清,http://8.8.8.8:8/udp/239.77.1.244:5146",
"深圳公共频道高清,http://8.8.8.8:8/udp/239.77.1.178:5146",
"深圳宝安频道高清,http://8.8.8.8:8/udp/239.77.1.67:5146",
"深圳龙岗频道高清,http://8.8.8.8:8/udp/239.77.1.223:5146",
"深圳众创TV高清,http://8.8.8.8:8/udp/239.77.1.247:5146",
"深圳宜和购物高清,http://8.8.8.8:8/udp/239.77.1.87:5146",
"韶关新闻综合高清,http://8.8.8.8:8/udp/239.77.0.117:5146",
"湛江新闻综合高清,http://8.8.8.8:8/udp/239.77.0.141:5146",
"湛江公共高清,http://8.8.8.8:8/udp/239.77.0.140:5146",
"揭阳综合高清,http://8.8.8.8:8/udp/239.77.0.229:5146",
"揭阳生活高清,http://8.8.8.8:8/udp/239.77.0.251:5146",
"汕尾新闻综合高清,http://8.8.8.8:8/udp/239.77.0.25:5146",
"汕尾文化生活高清,http://8.8.8.8:8/udp/239.77.0.187:5146",
"江门综合高清,http://8.8.8.8:8/udp/239.77.0.201:5146",
"江门侨乡生活高清,http://8.8.8.8:8/udp/239.77.0.202:5146",
"HZTV-1高清,http://8.8.8.8:8/udp/239.77.1.232:5146",
"HZTV-2高清,http://8.8.8.8:8/udp/239.77.1.233:5146",
"珠海-1高清,http://8.8.8.8:8/udp/239.77.0.155:5146",
"珠海-2高清,http://8.8.8.8:8/udp/239.77.0.154:5146",
"肇庆综合高清,http://8.8.8.8:8/udp/239.253.43.1:5146",
"肇庆生活服务高清,http://8.8.8.8:8/udp/239.253.43.2:5146",
"河源综合高清,http://8.8.8.8:8/udp/239.253.43.213:5146",
"河源公共高清,http://8.8.8.8:8/udp/239.253.43.214:5146",
"清远新闻综合高清,http://8.8.8.8:8/udp/239.253.43.33:5146",
"清远文旅生活高清,http://8.8.8.8:8/udp/239.253.43.34:5146",
"云浮综合高清,http://8.8.8.8:8/udp/239.77.0.253:5146",
"云浮文旅高清,http://8.8.8.8:8/udp/239.77.0.254:5146",
"茂名综合高清,http://8.8.8.8:8/udp/239.77.0.206:5146",
"茂名公共高清,http://8.8.8.8:8/udp/239.77.0.207:5146",
"汕头综合高清,http://8.8.8.8:8/udp/239.77.1.130:5146",
"汕头综合高清,http://8.8.8.8:8/udp/239.253.43.45:5146",
"汕头经济生活高清,http://8.8.8.8:8/udp/239.77.1.131:5146",
"汕头经济生活高清,http://8.8.8.8:8/udp/239.253.43.46:5146",
"汕头文旅体育高清,http://8.8.8.8:8/udp/239.77.1.132:5146",
"汕头文旅体育高清,http://8.8.8.8:8/udp/239.253.43.47:5146",
"佛山公共高清,http://8.8.8.8:8/udp/239.253.43.53:5146",
"佛山南海高清,http://8.8.8.8:8/udp/239.253.43.54:5146",
"佛山顺德高清,http://8.8.8.8:8/udp/239.253.43.55:5146",
"佛山影视高清,http://8.8.8.8:8/udp/239.253.43.56:5146",
"佛山综合高清,http://8.8.8.8:8/udp/239.253.43.57:5146",
"东莞新闻综合高清,http://8.8.8.8:8/udp/239.253.43.104:5146",
"东莞生活资讯高清,http://8.8.8.8:8/udp/239.253.43.105:5146",
"中山综合高清,http://8.8.8.8:8/udp/239.253.43.62:5146",
"香山文化高清,http://8.8.8.8:8/udp/239.253.43.63:5146",
"潮州综合高清,http://8.8.8.8:8/udp/239.253.43.70:5146",
"潮州民生高清,http://8.8.8.8:8/udp/239.253.43.75:5146",
"徐闻综合高清,http://8.8.8.8:8/udp/239.253.43.112:5146",
"梅州-1高清,http://8.8.8.8:8/udp/239.253.43.123:5146",
"客家生活高清,http://8.8.8.8:8/udp/239.253.43.124:5146",
"CCTV-1超清,http://8.8.8.8:8/udp/239.77.0.129:5146",
"CCTV-2高清,http://8.8.8.8:8/udp/239.77.1.158:5146",
"CCTV-3高清,http://8.8.8.8:8/udp/239.77.0.169:5146",
"CCTV-4高清,http://8.8.8.8:8/udp/239.77.1.163:5146",
"CCTV-4美洲高清,http://8.8.8.8:8/udp/239.253.43.121:5146",
"CCTV-4欧洲高清,http://8.8.8.8:8/udp/239.253.43.120:5146",
"CCTV-5高清,http://8.8.8.8:8/udp/239.77.0.170:5146",
"CCTV-5+高清,http://8.8.8.8:8/udp/239.77.0.87:5146",
"CCTV-6高清,http://8.8.8.8:8/udp/239.77.0.171:5146",
"CCTV-7高清,http://8.8.8.8:8/udp/239.77.1.159:5146",
"CCTV-8高清,http://8.8.8.8:8/udp/239.77.0.172:5146",
"CCTV-9高清,http://8.8.8.8:8/udp/239.77.1.160:5146",
"CCTV-10高清,http://8.8.8.8:8/udp/239.77.1.113:5146",
"CCTV-11高清,http://8.8.8.8:8/udp/239.77.1.238:5146",
"CCTV-12高清,http://8.8.8.8:8/udp/239.77.1.109:5146",
"CCTV-13高清,http://8.8.8.8:8/udp/239.77.0.188:5146",
"CCTV-14高清,http://8.8.8.8:8/udp/239.77.1.161:5146",
"CCTV-15高清,http://8.8.8.8:8/udp/239.77.1.239:5146",
"CCTV-16高清,http://8.8.8.8:8/udp/239.77.0.165:5146",
"CCTV-17高清,http://8.8.8.8:8/udp/239.77.1.121:5146",
"CCTV-4K 4K,http://8.8.8.8:8/udp/239.77.0.194:5146",
"CCTV-4K 4K50p,http://8.8.8.8:8/udp/239.77.0.174:5146",
"CGTN英语高清,http://8.8.8.8:8/udp/239.77.0.199:5146",
"CGTN Documentary高清,http://8.8.8.8:8/udp/239.253.43.122:5146",
"CGTN西班牙语高清,http://8.8.8.8:8/udp/239.77.0.221:5146",
"CGTN法语高清,http://8.8.8.8:8/udp/239.77.0.228:5146",
"CGTN阿拉伯语高清,http://8.8.8.8:8/udp/239.253.43.200:5146",
"CGTN俄语高清,http://8.8.8.8:8/udp/239.253.43.201:5146",
"湖南卫视超清,http://8.8.8.8:8/udp/239.77.0.127:5146",
"浙江卫视高清,http://8.8.8.8:8/udp/239.77.1.33:5146",
"江苏卫视高清,http://8.8.8.8:8/udp/239.77.1.18:5146",
"东方卫视高清,http://8.8.8.8:8/udp/239.77.1.218:5146",
"安徽卫视高清,http://8.8.8.8:8/udp/239.77.1.92:5146",
"北京卫视高清,http://8.8.8.8:8/udp/239.77.1.4:5146",
"天津卫视高清,http://8.8.8.8:8/udp/239.77.1.141:5146",
"山东卫视高清,http://8.8.8.8:8/udp/239.77.1.142:5146",
"江西卫视高清,http://8.8.8.8:8/udp/239.77.1.219:5146",
"湖北卫视超清,http://8.8.8.8:8/udp/239.77.0.128:5146",
"辽宁卫视高清,http://8.8.8.8:8/udp/239.77.1.103:5146",
"黑龙江卫视超清,http://8.8.8.8:8/udp/239.77.0.124:5146",
"贵州卫视高清,http://8.8.8.8:8/udp/239.77.1.221:5146",
"四川卫视高清,http://8.8.8.8:8/udp/239.77.1.215:5146",
"河南卫视高清,http://8.8.8.8:8/udp/239.77.1.229:5146",
"云南卫视高清,http://8.8.8.8:8/udp/239.253.43.37:5146",
"重庆卫视高清,http://8.8.8.8:8/udp/239.77.1.162:5146",
"河北卫视高清,http://8.8.8.8:8/udp/239.77.1.214:5146",
"东南卫视高清,http://8.8.8.8:8/udp/239.77.1.104:5146",
"广西卫视高清,http://8.8.8.8:8/udp/239.253.43.36:5146",
"吉林卫视高清,http://8.8.8.8:8/udp/239.77.1.111:5146",
"青海卫视高清,http://8.8.8.8:8/udp/239.253.43.125:5146",
"海南卫视高清,http://8.8.8.8:8/udp/239.253.43.35:5146",
"甘肃卫视高清,http://8.8.8.8:8/udp/239.77.0.189:5146",
"三沙卫视高清,http://8.8.8.8:8/udp/239.253.43.113:5146",
"兵器科技高清,http://8.8.8.8:8/udp/239.253.43.18:5146",
"电视指南高清,http://8.8.8.8:8/udp/239.253.43.19:5146",
"风云足球高清,http://8.8.8.8:8/udp/239.253.43.20:5146",
"央视台球高清,http://8.8.8.8:8/udp/239.253.43.21:5146",
"高尔夫网球高清,http://8.8.8.8:8/udp/239.253.43.22:5146",
"女性时尚高清,http://8.8.8.8:8/udp/239.253.43.23:5146",
"世界地理高清,http://8.8.8.8:8/udp/239.253.43.24:5146",
"怀旧剧场高清,http://8.8.8.8:8/udp/239.253.43.25:5146",
"风云剧场高清,http://8.8.8.8:8/udp/239.253.43.26:5146",
"央视文化精品高清,http://8.8.8.8:8/udp/239.253.43.27:5146",
"第一剧场高清,http://8.8.8.8:8/udp/239.253.43.28:5146",
"风云音乐高清,http://8.8.8.8:8/udp/239.253.43.29:5146",
"CHC高清电影,http://8.8.8.8:8/udp/239.77.0.27:5146",
"金鹰卡通高清,http://8.8.8.8:8/udp/239.77.0.164:5146",
"CETV-1高清,http://8.8.8.8:8/udp/239.77.1.222:5146",
"CETV-4高清,http://8.8.8.8:8/udp/239.77.1.200:5146",
"早期教育高清,http://8.8.8.8:8/udp/239.77.0.180:5146",
"中国交通,http://8.8.8.8:8/udp/239.77.1.249:5146",
"茶频道高清,http://8.8.8.8:8/udp/239.77.1.207:5146",
"快乐垂钓高清,http://8.8.8.8:8/udp/239.77.1.119:5146",
"金鹰纪实高清,http://8.8.8.8:8/udp/239.77.1.217:5146",
"上海纪实高清,http://8.8.8.8:8/udp/239.77.1.216:5146",
"生态环境,http://8.8.8.8:8/udp/239.77.1.201:5146",
"车迷频道,http://8.8.8.8:8/udp/239.77.1.203:5146",
"求索纪录高清,http://8.8.8.8:8/udp/239.77.0.21:5146",
"求索生活高清,http://8.8.8.8:8/udp/239.77.0.153:5146",
"武术世界高清,http://8.8.8.8:8/udp/239.77.1.108:5146",
"文物宝库高清,http://8.8.8.8:8/udp/239.77.1.120:5146",
"先锋乒羽,http://8.8.8.8:8/udp/239.77.1.208:5146",
"天元围棋,http://8.8.8.8:8/udp/239.253.43.98:5146",
"爱体育高清,http://8.8.8.8:8/udp/239.77.0.176:5146",
]


results = []
channel = []
urls_all = []
resultsx = []
resultxs = []
error_channels = []

for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && org="Chinanet"').encode("utf-8")), "utf-8")
    url_64 = f'https://fofa.info/result?qbase64={url_0}'
    print(url_64)
    try:
        response = requests.get(url_64, headers=headers, timeout=15)
        page_content = response.text
        print(f" {url}  访问成功")
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)
        for urlx in page_urls:
            try:
                response = requests.get(url=urlx + '/status', timeout=1)
                response.raise_for_status()  # 返回状态码不是200异常
                page_content = response.text
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f"{urlx} 可以访问")

            except requests.RequestException as e:
                pass
    except:
        print(f"{url_64} 访问失败")
        pass

urls_all = set(urls_all)  # 去重得到唯一的URL列表
for urlx in urls_all:
    channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
               [line.strip().split(',') for line in channelsx]]
    results.extend(channel)
            
results = sorted(results)
# with open("itv.txt", 'w', encoding='utf-8') as file:
#     for result in results:
#         file.write(result + "\n")
#         print(result)

# 定义工作线程函数
def worker():
    while True:
        result = task_queue.get()
        channel_name, channel_url = result.split(',', 1)
        try:
            response = requests.get(channel_url, stream=True, timeout=3)
            if response.status_code == 200:
                result = channel_name, channel_url
                resultsx.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channels.append(result)
                numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
                print(
                    f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channels.append(result)
            numberx = (len(resultsx) + len(error_channels)) / len(results) * 100
            print(
                f"可用频道：{len(resultsx)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(results)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 5
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# 添加下载任务到队列
for result in results:
    task_queue.put(result)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


for resulta in resultsx:
    channel_name, channel_url = resulta
    resultx = channel_name, channel_url
    resultxs.append(resultx)

# 对频道进行排序
resultxs.sort(key=lambda x: channel_key(x[0]))
# now_today = datetime.date.today()

result_counter = 5  # 每个频道需要的个数

with open("iptv.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if 'CCTV' in channel_name or '央视' in channel_name or 'CGTN' in channel_name or '风云足球' in channel_name or '高尔夫' \
		in channel_name or '女性时尚' in channel_name or '世界地理' in channel_name or '怀旧剧场' in channel_name  or '风云剧场' in channel_name or '央视文化' \in channel_name or '第一剧场' in channel_name or '风云音乐' in channel_name or '兵器科技' in channel_name  or '电视指南' in channel_name or 'CETV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n卫视频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '卫视' in channel_name or '纪实' in channel_name or '求索' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('\n广东频道,#genre#\n')
    for result in resultxs:
        channel_name, channel_url = result
        if '广东' in channel_name or '经济科教' in channel_name or '大湾区' in channel_name or '汕头' in channel_name or '潮州' in channel_name or '揭阳' in channel_name or '广州' in channel_name or '深圳' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

# 合并所有的txt文件
file_contents = []
file_paths = ["iptv.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

    # 写入合并后的txt文件
with open("iptv_list.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

    # 写入更新日期时间
    # file.write(f"{now_today}更新,#genre#\n")
    now = datetime.now()
    output.write(f"\n更新时间,#genre#\n")
    output.write(f"{now.strftime("%Y-%m-%d")},url\n")
    output.write(f"{now.strftime("%H:%M:%S")},url\n")

os.remove("iptv.txt")

def txt_to_m3u(input_file, output_file):
    # 读取txt文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 打开m3u文件并写入内容
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')

        # 初始化genre变量
        genre = ''

        # 遍历txt文件内容
        for line in lines:
            line = line.strip()
            if "," in line:  # 防止文件里面缺失“,”号报错
                # if line:
                # 检查是否是genre行
                channel_name, channel_url = line.split(',', 1)
                if channel_url == '#genre#':
                    genre = channel_name
                    print(genre)
                else:
                    # 将频道信息写入m3u文件
                    f.write(f'#EXTINF:-1 group-title="{genre}",{channel_name}\n')
                    f.write(f'{channel_url}\n')


# 将txt文件转换为m3u文件
txt_to_m3u('iptv_list.txt', 'iptv_list.m3u')

print(f"电视频道成功写入iptv_dx.txt和iptv_list.m3u")
