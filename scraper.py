import json
import urllib.request
import datetime
import pytz

# 設定時區與時間
bne_tz = pytz.timezone('Australia/Brisbane')
now = datetime.datetime.now(bne_tz)
update_time = now.strftime("%Y-%m-%d %H:%M:%S")

# 讀取 schools.json 資料庫
try:
    with open('schools.json', 'r', encoding='utf-8') as f:
        schools = json.load(f)
except Exception as e:
    print(f"讀取 JSON 失敗: {e}")
    schools = []

# HTML 模板頭部與視覺美化
html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>布里斯本名校情報站 4.0</title>
    <style>
        body {{ font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif; line-height: 1.6; padding: 20px; background: #f8f9fa; color: #2c3e50; }}
        .container {{ max-width: 900px; margin: auto; }}
        h1 {{ text-align: center; color: #2c3e50; margin-bottom: 5px; }}
        .time {{ text-align: center; color: #7f8c8d; font-size: 0.9em; margin-bottom: 30px; border-bottom: 2px solid #3498db; padding-bottom: 10px; display: inline-block; width: 100%; }}
        .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 20px; }}
        @media (max-width: 500px) {{ .card-grid {{ grid-template-columns: 1fr; }} }}
        .card {{ background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #3498db; }}
        h2 {{ margin: 0 0 15px 0; color: #2980b9; font-size: 1.3em; }}
        .info-row {{ margin-bottom: 8px; font-size: 0.95em; display: flex; align-items: baseline; }}
        .label {{ font-weight: bold; min-width: 90px; color: #34495e; }}
        .value {{ color: #16a085; font-weight: 500; }}
        .btn-group {{ display: flex; gap: 10px; margin-top: 20px; }}
        .btn {{ flex: 1; text-align: center; color: white; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 0.9em; transition: 0.3s; }}
        .btn-openday {{ background: #27ae60; }}
        .btn-openday:hover {{ background: #219150; }}
        .btn-exam {{ background: #2980b9; }}
        .btn-exam:hover {{ background: #21618c; }}
        .footer {{ text-align: center; margin-top: 40px; color: #bdc3c7; font-size: 0.8em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 布里斯本入學情報站 4.0</h1>
        <p class="time">最後自動巡邏時間：{update_time} (AEST)</p>
        <div class="card-grid">
"""

# 生成卡片邏輯
for s in schools:
    html += f"""
    <div class="card">
        <h2>{s.get('name', '未命名學校')}</h2>
        <div class="info-row"><span class="label">📅 開放日：</span><span class="value">{s.get('openDay', '待確認')}</span></div>
        <div class="info-row"><span class="label">📝 報名期：</span><span class="value">{s.get('regDate', '待確認')}</span></div>
        <div class="info-row"><span class="label">🔥 考試日：</span><span class="value">{s.get('examDate', '待確認')}</span></div>
        <div class="btn-group">
            <a href="{s.get('openDayUrl', '#')}" class="btn btn-openday" target="_blank">📅 開放日連結</a>
            <a href="{s.get('examUrl', '#')}" class="btn btn-exam" target="_blank">📝 報名與考試情報</a>
        </div>
    </div>
    """

html += """
        </div>
        <div class="footer">由 Jack 的自動化算力引擎代勞分憂，每日自動更新。</div>
    </div>
</body>
</html>
"""

# 寫入最終網頁檔
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 佈署完畢：情報站 4.0 已成功生成。")
