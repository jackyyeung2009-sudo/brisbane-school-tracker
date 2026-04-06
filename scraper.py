import json
import urllib.request
import datetime
import pytz
import re

# 設定時區
bne_tz = pytz.timezone('Australia/Brisbane')
now = datetime.datetime.now(bne_tz)
update_time = now.strftime("%Y-%m-%d %H:%M:%S")

# 讀取資料
try:
    with open('schools.json', 'r', encoding='utf-8') as f:
        schools = json.load(f)
except Exception as e:
    print(f"讀取失敗: {e}")
    schools = []

# --- 核心排序邏輯：提取開放日日期進行排序 ---
def get_sort_date(school):
    date_str = school.get('openDay', '')
    # 尋找月份與日期 (例如: 5月12日)
    match = re.search(r'(\d+)月(\d+)日', date_str)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        # 判定年份：沒寫 2027 即為 2026
        year = 2027 if '2027' in date_str else 2026
        return datetime.datetime(year, month, day)
    # 若無日期格式，排在最後面 (給予一個遙遠的未來日期)
    return datetime.datetime(2099, 12, 31)

# 執行排序 (由近到遠)
schools.sort(key=get_sort_date)

# --- HTML 生成 ---
html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>布里斯本名校情報站 5.0 - 智能排序版</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; line-height: 1.6; padding: 20px; background: #f4f7f9; color: #333; }}
        .container {{ max-width: 900px; margin: auto; }}
        h1 {{ text-align: center; color: #2c3e50; }}
        .time {{ text-align: center; color: #7f8c8d; font-size: 0.9em; margin-bottom: 20px; border-bottom: 2px solid #3498db; padding-bottom: 10px; width: 100%; display: block; }}
        .card {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 6px solid #3498db; }}
        .card:nth-child(2) {{ border-left-color: #e74c3c; }} /* 第一名顯示紅色提醒，代表最接近 */
        h2 {{ margin: 0 0 10px 0; color: #2980b9; }}
        .info {{ font-size: 0.95em; margin-bottom: 5px; }}
        .label {{ font-weight: bold; color: #555; width: 100px; display: inline-block; }}
        .val {{ color: #27ae60; font-weight: bold; }}
        .btn-group {{ display: flex; gap: 10px; margin-top: 15px; }}
        .btn {{ flex: 1; text-align: center; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.9em; }}
        .btn-blue {{ background: #3498db; }}
        .btn-green {{ background: #27ae60; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 布里斯本名校情報站 5.0</h1>
        <p class="time">🚀 智能排序模式已啟動 | 更新時間：{update_time}</p>
"""

for s in schools:
    html += f"""
    <div class="card">
        <h2>{s['name']}</h2>
        <div class="info"><span class="label">📅 開放日：</span><span class="val">{s.get('openDay', '待確認')}</span></div>
        <div class="info"><span class="label">📝 報名期：</span><span class="val">{s.get('regDate', '待確認')}</span></div>
        <div class="info"><span class="label">🔥 考試日：</span><span class="val">{s.get('examDate', '待確認')}</span></div>
        <div class="btn-group">
            <a href="{s.get('openDayUrl', '#')}" class="btn btn-green" target="_blank">📅 開放日連結</a>
            <a href="{s.get('examUrl', '#')}" class="btn btn-blue" target="_blank">📝 考試報名情報</a>
        </div>
    </div>
    """

html += "</div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
