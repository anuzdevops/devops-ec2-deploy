from flask import Flask, jsonify
import socket
import os
from datetime import datetime

app = Flask(__name__)

START_TIME = datetime.now()

@app.route('/')
def home():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = "Unknown"

    uptime = datetime.now() - START_TIME

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevOps Pipeline | Anuj Yadav</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
           .container {{
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 20px;
                padding: 50px;
                max-width: 700px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                animation: float 6s ease-in-out infinite;
            }}
            @keyframes float {{
                0% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-10px); }}
                100% {{ transform: translateY(0px); }}
            }}
            h1 {{
                font-size: 2.5em;
                background: linear-gradient(to right, #00f2fe, #4facfe);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}
           .badge {{
                display: inline-block;
                background: #00f2fe;
                color: #0f0c29;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.9em;
                margin-bottom: 20px;
            }}
           .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-top: 30px;
                text-align: left;
            }}
           .info-box {{
                background: rgba(255,255,255,0.07);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #4facfe;
            }}
           .info-box b {{ color: #00f2fe; display: block; font-size: 0.8em; margin-bottom: 5px; }}
           .footer {{ margin-top: 30px; opacity: 0.6; font-size: 0.85em; }}
           .pulse {{
                display: inline-block;
                width: 10px; height: 10px;
                background: #00ff88;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 rgba(0,255,136,0.7); }}
                70% {{ box-shadow: 0 0 0 10px rgba(0,255,136,0); }}
                100% {{ box-shadow: 0 0 0 0 rgba(0,255,136,0); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">LEVEL 4 - REMOTE STATE ACTIVE</span>
            <h1>🚀 Deployed via DevOps Pipeline</h1>
            <p style="opacity:0.8; font-size:1.2em; margin-top:10px;">Terraform + AWS + S3 Backend + Flask</p>

            <div class="info-grid">
                <div class="info-box"><b>HOSTNAME</b>{hostname}</div>
                <div class="info-box"><b>PRIVATE IP</b>{ip}</div>
                <div class="info-box"><b>STATUS</b><span class="pulse"></span>Live & Healthy</div>
                <div class="info-box"><b>UPTIME</b>{str(uptime).split('.')[0]}</div>
                <div class="info-box"><b>REGION</b>eu-north-1</div>
                <div class="info-box"><b>DEPLOYED BY</b>Anuj Yadav</div>
            </div>

            <div class="footer">
                Infrastructure as Code • Remote State in S3 • Zero Downtime<br>
                Last deployed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname(),
        "version": "v4.0-remote-state",
        "uptime_seconds": int((datetime.now() - START_TIME).total_seconds())
    }), 200

@app.route('/api/info')
def info():
    return jsonify({
        "project": "devops-ec2-deploy",
        "level": "Level 4 - Remote State",
        "stack": ["Terraform", "AWS EC2", "S3 Backend", "Flask"],
        "author": "Anuj Yadav"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
