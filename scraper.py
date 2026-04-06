import json
import urllib.request
import datetime
import pytz

def fetch_data():
    bne_tz = pytz.timezone('Australia/Brisbane')
    now = datetime.datetime.now(bne_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    with open('schools.json', 'r', encoding='utf-8') as f:
        schools = json.load(f)

    html_template = """
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>布里斯本名校入學情報站</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; padding: 20px; background-color: #f8f9fa; color: #333; }
            .container { max-width: 900px; margin: auto; }
            .header { text-align: center; padding: 20px; background: #003087; color: white; border-radius: 10px; margin-bottom: 20px; }
            .school-card { background: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #003087; }
            .school-name { font-size: 1.25rem; font-weight: bold; color: #003087; }
            .update-tag { font-size: 0.8rem; color: #666; text-align: right; }
            .btn { display: inline-block; padding: 8px 15px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin-top: 10px; }
            .btn:hover { background: #218838; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 布里斯本名校入學情報站</h1>
                <p>自動掃描 2026 年度 Open Day & 考試日期</p>
            </div>
            <p class="update-tag">資料更新日期：""" + now + """ AEST</p>
    """

    for school in schools:
        # 這裡執行連結探測，確保網址存活
        status = "🟢 連結正常，自動監控中"
        try:
            req = urllib.request.Request(school['url'], headers={'User-Agent': 'Mozilla/5.0'})
            urllib.request.urlopen(req, timeout=10)
        except:
            status = "🔴 網址可能變更或維護中，建議點擊手動確認"

        html_template += f"""
            <div class="school-card">
                <div class="school-name">{school['name']}</div>
                <p>狀態：{status}</p>
                <a href="{school['url']}" class="btn" target="_blank">點擊查看最新 Open Day/Exam 日期</a>
            </div>
        """

    html_template += """
        </div>
        <footer style="text-align: center; margin-top: 50px; color: #888;">
            <p>由 GitHub Actions 每日自動更新 | 最高算力代勞分憂</p>
        </footer>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    fetch_data()
