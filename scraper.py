import json
import urllib.request
import datetime
import pytz

# 設定時區與時間
bne_tz = pytz.timezone('Australia/Brisbane')
now = datetime.datetime.now(bne_tz)
update_time = now.strftime("%Y-%m-%d %H:%M:%S")

# 讀取剛升級的 JSON 資料庫
with open('schools.json', 'r', encoding='utf-8') as f:
    schools = json.load(f)

# HTML 模板頭部與 CSS 視覺優化 (支援雙按鈕並排)
html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>布里斯本名校情報站 2.0</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; line-height: 1.6; padding: 20px; background: #f0f2f5; color: #1c1e21; }}
        .container {{ max-width: 800px; margin: auto; }}
        h1 {{ text-align: center; color: #1a73e8; }}
        .time {{ text-align: center; color: #666; font-size: 0.9em; margin-bottom: 30px; }}
        .card {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.3s; }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }}
        h2 {{ margin-top: 0; color: #202124; font-size: 1.2em; border-bottom: 2px solid #e8eaed; padding-bottom: 10px; }}
        .btn-group {{ display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap; }}
        .btn {{ flex: 1; text-align: center; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; min-width: 140px; box-sizing: border-box; }}
        .btn-openday {{ background: #34a853; }}
        .btn-openday:hover {{ background: #2b8c46; }}
        .btn-exam {{ background: #1a73e8; }}
        .btn-exam:hover {{ background: #1557b0; }}
        .btn-disabled {{ background: #cccccc; cursor: not-allowed; color: #666; }}
        .status {{ font-size: 0.85em; color: #5f6368; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 布里斯本入學情報站 2.0</h1>
        <p class="time">資料更新日期 (AEST)：{update_time}</p>
"""

# 遍歷資料庫，生成雙通道按鈕卡片
for s in schools:
    open_day_url = s.get('openDayUrl', '#')
    exam_url = s.get('examUrl', '#')
    
    html += f"""
    <div class="card">
        <h2>{s['name']}</h2>
        <p class="status">⚡ 雙引擎掛載完畢，請點擊下方專屬通道直達官方陣地。</p>
        <div class="btn-group">
    """
    
    # 開放日通道邏輯
    if open_day_url != '#' and open_day_url != '':
        html += f'<a href="{open_day_url}" class="btn btn-openday" target="_blank">📅 開放日情報</a>'
    else:
        html += f'<span class="btn btn-disabled">📅 暫無開放日連結</span>'

    # 考試/獎學金通道邏輯
    if exam_url != '#' and exam_url != '':
        html += f'<a href="{exam_url}" class="btn btn-exam" target="_blank">📝 考試與入學情報</a>'
    else:
         html += f'<span class="btn btn-disabled">📝 暫無考試連結</span>'

    html += """
        </div>
    </div>
    """

html += "</div></body></html>"

# 寫入靜態網頁檔案
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
    
print("情報站 2.0 HTML 檔案生成完畢！")
