import json
import datetime
import pytz
import re

bne_tz = pytz.timezone('Australia/Brisbane')
now = datetime.datetime.now(bne_tz)
update_time = now.strftime("%Y-%m-%d %H:%M:%S")

with open('schools.json', 'r', encoding='utf-8') as f:
    schools = json.load(f)

def get_deadline_date(school):
    reg_str = school.get('regDate', '')
    # 優先抓取報名期內的日期 (例如 5月11日 或 8月21日)
    match = re.search(r'(\d+)年(\d+)月(\d+)日', reg_str)
    if match:
        return datetime.datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return datetime.datetime(2099, 12, 31)

# 核心排序：按報名日期由近到遠
schools.sort(key=get_deadline_date)

html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>布里斯本入學生死線 6.0</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; padding: 20px; background: #fdf2f2; color: #333; }}
        .container {{ max-width: 800px; margin: auto; }}
        .card {{ background: white; border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 8px solid #e74c3c; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .deadline-box {{ background: #e74c3c; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin-bottom: 10px; }}
        h2 {{ margin: 0; font-size: 1.3em; color: #c0392b; }}
        .row {{ font-size: 1em; margin: 8px 0; }}
        .label {{ font-weight: bold; color: #7f8c8d; min-width: 100px; display: inline-block; }}
        .highlight {{ color: #e74c3c; font-weight: 900; font-size: 1.1em; }}
        .btn {{ display: block; text-align: center; color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; background: #2c3e50; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align:center;">🔥 布里斯本名校：報名生死線排序</h1>
        <p style="text-align:center; color:#666;">忘了報名便沒戲了！系統已按報名截止日自動排序</p>
"""

for s in schools:
    html += f"""
    <div class="card">
        <div class="deadline-box">🚨 報名優先級</div>
        <h2>{s['name']}</h2>
        <div class="row"><span class="label">✍️ 報名日期：</span><span class="highlight">{s['regDate']}</span></div>
        <div class="row"><span class="label">📅 開放日：</span><span>{s['openDay']}</span></div>
        <div class="row"><span class="label">🔥 考試日期：</span><span>{s['examDate']}</span></div>
        <a href="{s['examUrl']}" class="btn" target="_blank">立即前往報名官網</a>
    </div>
    """

html += "</div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
