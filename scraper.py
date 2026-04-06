import json
import urllib.request
import datetime
import pytz
import re

bne_tz = pytz.timezone('Australia/Brisbane')
now = datetime.datetime.now(bne_tz)
update_time = now.strftime("%Y-%m-%d %H:%M:%S")

with open('schools.json', 'r', encoding='utf-8') as f:
    schools = json.load(f)

def get_sort_date(school):
    date_str = school.get('openDay', '')
    # 正則表達式抓取: 年、月、日
    match = re.search(r'(\d+)年(\d+)月(\d+)日', date_str)
    if match:
        return datetime.datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    
    # 若只有年份+TERM (例如 2026年TERM 3)，給予該年 7 月中旬排序
    year_match = re.search(r'(\d+)年', date_str)
    if year_match:
        return datetime.datetime(int(year_match.group(1)), 7, 15)
    
    return datetime.datetime(2099, 12, 31)

# 由近到遠排序
schools.sort(key=get_sort_date)

html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>布里斯本名校情報站 終極排序版</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; padding: 20px; background: #f0f4f8; color: #333; }}
        .container {{ max-width: 800px; margin: auto; }}
        .time {{ text-align: center; color: #666; font-size: 0.8em; margin-bottom: 20px; }}
        .card {{ background: white; border-radius: 10px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-left: 5px solid #3498db; }}
        h2 {{ margin: 0; font-size: 1.2em; color: #2c3e50; }}
        .row {{ font-size: 0.9em; margin: 5px 0; }}
        .label {{ font-weight: bold; color: #555; }}
        .val {{ color: #27ae60; }}
        .btn-group {{ display: flex; gap: 8px; margin-top: 10px; }}
        .btn {{ flex: 1; text-align: center; color: white; padding: 8px; border-radius: 5px; text-decoration: none; font-size: 0.85em; font-weight: bold; }}
        .bg-green {{ background: #2ecc71; }}
        .bg-blue {{ background: #3498db; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align:center;">🎓 布里斯本入學情報站</h1>
        <p class="time">精準排序更新：{update_time}</p>
"""

for s in schools:
    html += f"""
    <div class="card">
        <h2>{s['name']}</h2>
        <div class="row"><span class="label">📅 開放日：</span><span class="val">{s['openDay']}</span></div>
        <div class="row"><span class="label">📝 報名期：</span><span class="val">{s['regDate']}</span></div>
        <div class="row"><span class="label">🔥 考試日：</span><span class="val">{s['examDate']}</span></div>
        <div class="btn-group">
            <a href="{s['openDayUrl']}" class="btn bg-green" target="_blank">📅 開放日連結</a>
            <a href="{s['examUrl']}" class="btn bg-blue" target="_blank">📝 報名與考試</a>
        </div>
    </div>
    """

html += "</div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
