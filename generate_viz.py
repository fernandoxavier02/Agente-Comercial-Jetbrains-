import sqlite3
import json

def generate_html_report():
    conn = sqlite3.connect('sql_app.db')
    cursor = conn.cursor()
    
    # Buscar leads e itens de origem
    cursor.execute("""
        SELECT l.id, l.scores, l.labels, s.author_handle, s.text, s.raw_metadata
        FROM leads l
        JOIN source_items s ON l.source_item_id = s.id
        ORDER BY json_extract(l.scores, '$.lead_score') DESC
    """)
    rows = cursor.fetchall()
    
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Elite Leads Hub - Clínica Médica Mais</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0e1117; color: #e0e0e0; margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: auto; }
            .header { text-align: center; padding: 40px 0; border-bottom: 1px solid #333; }
            .header h1 { color: #ffd700; margin: 0; font-size: 2.5em; }
            .lead-card { background-color: #161b22; border: 1px solid #333; border-radius: 12px; padding: 25px; margin-bottom: 30px; display: flex; align-items: flex-start; transition: transform 0.2s; }
            .lead-card:hover { transform: scale(1.01); border-color: #ffd700; }
            .avatar { width: 120px; height: 120px; border-radius: 10px; object-fit: cover; margin-right: 25px; border: 2px solid #333; }
            .no-avatar { width: 120px; height: 120px; background: #333; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 25px; color: #888; }
            .content { flex-grow: 1; }
            .author { font-size: 1.4em; color: #fff; margin: 0; }
            .badge { background-color: #ffd700; color: #000; padding: 3px 10px; border-radius: 5px; font-size: 0.7em; font-weight: bold; margin-left: 10px; vertical-align: middle; }
            .text { font-style: italic; color: #aaa; margin: 15px 0; line-height: 1.5; }
            .tags { margin-top: 10px; }
            .tag { background-color: #0068c9; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.8em; margin-right: 8px; }
            .score-box { text-align: center; min-width: 100px; padding-left: 20px; border-left: 1px solid #333; }
            .score-value { font-size: 2.2em; font-weight: bold; color: #ffd700; }
            .score-label { font-size: 0.8em; color: #888; }
            .pericia { margin-top: 20px; background: #0d1117; padding: 15px; border-radius: 8px; font-size: 0.9em; }
            .pericia-title { font-weight: bold; color: #ffd700; margin-bottom: 5px; }
            .whatsapp-btn { display: inline-block; margin-top: 20px; background-color: #25d366; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💎 Elite Leads Hub</h1>
                <p>Painel de Inteligência de Captação - Clínica Médica Mais</p>
            </div>
    """
    
    for row in rows:
        lead_id, scores_json, labels_json, author, text, metadata_json = row
        scores = json.loads(scores_json)
        labels = json.loads(labels_json)
        metadata = json.loads(metadata_json) if metadata_json else {}
        
        score_val = scores.get('lead_score', 0)
        is_vip = score_val > 30
        status_label = "VIP ELITE" if is_vip else "QUALIFICADO"
        img_url = metadata.get('author_image')
        
        avatar_html = f'<img src="{img_url}" class="avatar">' if img_url else '<div class="no-avatar">👤 No Image</div>'
        
        tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in labels.get('visual_profile', [])])
        
        html_content += f"""
            <div class="lead-card">
                {avatar_html}
                <div class="content">
                    <p class="author">{author} <span class="badge">{status_label}</span></p>
                    <p class="text">"{text}"</p>
                    <div class="tags">
                        {tags_html}
                    </div>
                    <div class="pericia">
                        <div class="pericia-title">🔍 Relatório de Perícia Visual:</div>
                        {scores.get('visual_justification', 'N/A')}
                    </div>
                    <a href="#" class="whatsapp-btn">📱 Abordar no WhatsApp</a>
                </div>
                <div class="score-box">
                    <div class="score-value">{score_val:.1f}</div>
                    <div class="score-label">LEAD SCORE</div>
                </div>
            </div>
        """
        
    html_content += """
        </div>
    </body>
    </html>
    """
    
    with open('elite_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    conn.close()
    print("Dashboard HTML gerado com sucesso: elite_dashboard.html")

if __name__ == "__main__":
    generate_html_report()
