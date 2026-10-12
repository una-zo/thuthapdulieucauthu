from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.json.sort_keys = False
DB_PATH = "football_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

def get_real_columns(conn):
    "Tự động tìm tên cột thực tế trong DB có chứa từ khóa"
    cursor = conn.cursor()
    # Lệnh lấy toàn bộ cấu trúc bảng
    cursor.execute("PRAGMA table_info(fbref_player_stats)")
    cols = [row[1] for row in cursor.fetchall()]
    
    # Lọc ra tên cột có chứa chữ Player và Squad
    player_col = [c for c in cols if 'Player' in c][0]
    squad_col = [c for c in cols if 'Squad' in c][0]
    
    return player_col, squad_col

# API 1: Tra cứu theo Tên cầu thủ

@app.route('/api/player', methods=['GET'])
def get_player():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Vui lòng nhập tên cầu thủ. Ví dụ: ?name=Haaland"}), 400
    
    conn = get_db_connection()
    player_col, _ = get_real_columns(conn) # Gọi hàm dò tìm
    
    # Dùng f-string nhét tên cột thực tế vào câu SQL
    query = f"""
        SELECT a.*, b.Transfer_Value 
        FROM fbref_player_stats a
        RIGHT JOIN player_transfer_values b ON a."{player_col}" = b.Player
        WHERE a."{player_col}" LIKE ?
    """
    player_data = conn.execute(query, ('%' + name + '%',)).fetchall()
    conn.close()

    if player_data:
        return jsonify([dict(row) for row in player_data])
    return jsonify({"message": "Không tìm thấy cầu thủ này trong Database"}), 404

# API 2: Tra cứu theo Câu lạc bộ (Club)

@app.route('/api/club', methods=['GET'])
def get_club():
    club = request.args.get('name')
    if not club:
        return jsonify({"error": "Vui lòng nhập tên CLB. Ví dụ: ?name=Arsenal"}), 400
    
    conn = get_db_connection()
    player_col, squad_col = get_real_columns(conn)

    query = f"""
        SELECT a.*, b.Transfer_Value 
        FROM fbref_player_stats a
        RIGHT JOIN player_transfer_values b ON a."{player_col}" = b.Player
        WHERE a."{squad_col}" LIKE ?
    """
    club_data = conn.execute(query, ('%' + club + '%',)).fetchall()
    conn.close()

    if club_data:
        return jsonify([dict(row) for row in club_data])
    return jsonify({"message": "Không tìm thấy câu lạc bộ này"}), 404

# --- CHẠY SERVER ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
