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
    match = re.search(r'(\d+)年(\d+)月(\d+)日', reg_str)
    if match:
        return datetime.datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return datetime.datetime(2099, 12, 31)

# 按報名日期排序
schools.sort(key=get_deadline_date)

html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>布里斯本名校入學指南</title>
    <style>
        body {{ font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif; padding: 20px; background: #eef7f9; color: #444; }}
        .container {{ max-width: 800px; margin: auto; }}
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ color: #2c7da0; font-size: 1.8em; margin-bottom: 5px; }}
        .update-tag {{ font-size: 0.85em; color: #88b0bd; }}
        .card {{ background: white; border-radius: 16px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); border-top: 6px solid #89cff0; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-3px); }}
        h2 {{ margin: 0 0 15px 0; font-size: 1.3em; color: #4682b4; }}
        .info-grid {{ display: grid; gap: 10px; margin-bottom: 20px; }}
        .item {{ display: flex; align-items: center; font-size: 0.95em; }}
        .label {{ font-weight: bold; color: #5a9fb3; width: 100px; }}
        .content {{ color: #555; }}
        .btn-group {{ display: flex; gap: 10px; }}
        .btn {{ flex: 1; text-align: center; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 0.9em; transition: 0.3s; }}
        .btn-open {{ background: #b0e0e6; color: #2c7da0; }}
        .btn-open:hover {{ background: #a0d0d6; }}
        .btn-reg {{ background: #6495ed; color: white; }}
        .btn-reg:hover {{ background: #4169e1; }}
        .footer {{ text-align: center; color: #bdc3c7; font-size: 0.8em; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>☀️ 布里斯本名校情報站</h1>
            <div class="update-tag">專屬情報即時更新：{update_time}</div>
        </header>
"""

for s in schools:
    html += f"""
    <div class="card">
        <h2>{s['name']}</h2>
        <div class="info-grid">
            <div class="item"><span class="label">✍️ 報名日期</span><span class="content">{s['regDate']}</span></div>
            <div class="item"><span class="label">📅 開放日期</span><span class="content">{s['openDay']}</span></div>
            <div class="item"><span class="label">📝 考試日期</span><span class="content">{s['examDate']}</span></div>
        </div>
        <div class="btn-group">
            <a href="{s['openDayUrl']}" class="btn btn-open" target="_blank">預約開放日</a>
            <a href="{s['examUrl']}" class="btn btn-reg" target="_blank">前往報名</a>
        </div>
    </div>
    """

html += """
        <div class="footer">最高算力代勞分憂 · 祝願入讀心儀名校</div>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
