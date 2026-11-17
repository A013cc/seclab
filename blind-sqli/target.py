import sqlite3
from flask import Flask, request

app = Flask(__name__)
DB = "vuln.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'admin', 'S3cr3t_P@ssw0rd_2024')")
    conn.execute("INSERT INTO users VALUES (2, 'guest', 'guest123')")
    conn.commit()
    conn.close()
    print("[DB] 初始化完成")

@app.route("/")
def index():
    return ('<form action="/login">'
            '用户名 <input name="username"> '
            '密码 <input name="password"> '
            '<button>登录</button></form>')

@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    # ↓↓↓↓ 漏洞就在这里:用户输入被直接拼进了 SQL ↓↓↓↓
    sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print("[SQL]", sql)          # ★ 每来一次请求,终端就打印真实 SQL

    conn = sqlite3.connect(DB)
    row = conn.execute(sql).fetchone()
    conn.close()
    return "登录成功" if row else "登录失败"

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)