import pandas as pd
import sqlite3
from seleniumbase import Driver
class FootballDataScraper:
    def __init__(self, db_name="football_data.db"):
        self.db_name = db_name
        
        print("Đang khởi động trình duyệt ảo Chrome...")
        self.driver = Driver(uc=True, headless=False)
    def scrape_fbref_stats(self, url):
        print(f"Đang truy cập: {url}")
        self.driver.uc_open_with_reconnect(url, 4)
        try:
            print("Đang chờ bảng dữ liệu 'stats_standard' xuất hiện...")
            self.driver.wait_for_element("#stats_standard", timeout=15)

            html_content = self.driver.get_page_source()
            html_content = html_content.replace('<!--', '').replace('-->', '')

            from io import StringIO

            # Dùng attrs={"id": "stats_standard"} để bảo Pandas chỉ lấy đúng bảng này
            tables = pd.read_html(StringIO(html_content), attrs={"id": "stats_standard"})

            if not tables:
                print("Không tìm thấy bảng stats_standard trong HTML.")
                return None

            # Vì đã lọc chính xác theo ID, danh sách tables giờ chỉ có 1 phần tử duy nhất
            df = tables[0]

            return self._clean_data(df)

        except Exception as e:
            print(f"Không thể vượt qua Cloudflare hoặc web lỗi: {e}")
            return None
    def _clean_data(self, df):
        print("Đang làm sạch dữ liệu...")

        # 1. Xử lý tên cột: Đảm bảo TẤT CẢ đều là chuỗi (string)
        if isinstance(df.columns, pd.MultiIndex):
            # Ép kiểu từng phần tử (i) thành chuỗi str(i) trước khi join
            df.columns = ['_'.join(str(i) for i in col).strip().replace(' ', '_') for col in df.columns.values]
        else:
            # Nếu không phải MultiIndex, ép kiểu toàn bộ cột thành chuỗi
            df.columns = df.columns.astype(str)

        rename_map = {
            'Unnamed:_0_level_0_Rk': 'Rk',
            'Unnamed:_1_level_0_Player': 'Player',
            'Unnamed:_2_level_0_Nation': 'Nation',
            'Unnamed:_3_level_0_Pos': 'Pos',
            'Unnamed:_4_level_0_Squad': 'Squad',
            'Unnamed:_5_level_0_Age': 'Age',
            'Unnamed:_6_level_0_Born': 'Born',
            'Playing_Time_MP': 'MP',
            'Playing_Time_Starts': 'Starts',
            'Playing_Time_Min': 'Min',
            'Playing_Time_90s': '90s',
            'Performance_Gls': 'Gls',
            'Performance_Ast': 'Ast',
            'Performance_G+A': 'G+A',
            'Performance_G-PK': 'G-PK',
            'Performance_PK': 'PK',
            'Performance_PKatt': 'PKatt',
            'Performance_CrdY': 'CrdY',
            'Performance_CrdR': 'CrdR',
            'Per_90_Minutes_Gls': 'Gls/90',
            'Per_90_Minutes_Ast': 'Ast/90',
            'Per_90_Minutes_G+A': 'G+A/90',
            'Per_90_Minutes_G-PK': 'G-PK/90',
            'Per_90_Minutes_G+A-PK': 'G+A-PK/90',
            'Unnamed:_24_level_0_Matches': 'Matches'
        }

        df.rename(columns=rename_map, inplace=True)

        # 2. Tìm cột an toàn bằng cách bọc str(c)
        try:
            player_col = [c for c in df.columns if 'Player' in str(c)][0]
            df = df[df[player_col] != 'Player']

            min_col = [c for c in df.columns if 'Min' in str(c)][0]
            df[min_col] = pd.to_numeric(df[min_col], errors='coerce')

            # Chỉ lấy cầu thủ đá trên 90 phút
            df = df[df[min_col] > 90]

        except IndexError:
            # Nếu web đổi cấu trúc và Pandas không tìm thấy chữ Player/Min, in ra lỗi
            print("Lỗi Pandas: Không tìm thấy cột 'Player' hoặc 'Min' trong dữ liệu tải về.")
            print("Danh sách các cột hiện tại để kiểm tra:", df.columns.tolist())
            return None

        df = df.fillna('N/a')
        return df
    def save_to_sqlite(self, df, table_name):
        if df is not None and not df.empty:
            print(f"Đang lưu {len(df)} cầu thủ vào DB...")
            with sqlite3.connect(self.db_name) as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
            print("Lưu thành công!\n")
        else:
            print("Không có dữ liệu để lưu.")
    def close_browser(self):
        self.driver.quit()

# --- KHỐI LỆNH CHẠY THỬ ---
if __name__ == "__main__":
    url_epl = "https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats"
    scraper = FootballDataScraper()
    try:
        df_players = scraper.scrape_fbref_stats(url_epl)
        scraper.save_to_sqlite(df_players, table_name="fbref_player_stats")

        if df_players is not None:
            print("Dữ liệu xem trước:")
            print(df_players.head())
    finally:
        # Luôn đảm bảo trình duyệt được đóng dù có lỗi xảy ra
        scraper.close_browser()
