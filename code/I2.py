import pandas as pd
import sqlite3
import time
from seleniumbase import Driver
class TransferScraper:
    def __init__(self, db_name="football_data.db"):
        self.db_name = db_name

        print("Đang khởi động trình duyệt ảo Chrome...")

        # Tự động tải và cài đặt ChromeDriver cho đúng phiên bản Chrome trên máy
        self.driver = Driver(uc=True, headless=False)

    def save_to_sqlite(self, df, table_name, mode='replace'):
        if df is not None and not df.empty:
            with sqlite3.connect(self.db_name) as conn:
                # Dùng tham số if_exists tùy biến để hỗ trợ lưu nối tiếp (append)
                df.to_sql(table_name, conn, if_exists=mode, index=False)
        else:
            print("Không có dữ liệu để lưu.")

    def scrape_transfer_values(self):
        with sqlite3.connect(self.db_name) as conn:
            df_temp = pd.read_sql("SELECT * FROM fbref_player_stats LIMIT 1", conn)
            player_col = [c for c in df_temp.columns if 'Player' in c][0]
            query = f'SELECT "{player_col}" FROM fbref_player_stats'
            players = pd.read_sql(query, conn)[player_col].tolist()

        transfer_data = []
        count = 0  # Biến đếm để lưu tiến độ
        # THÊM KHỐI TRY TỔNG Ở ĐÂY ĐỂ BẮT LỆNH CTRL+C
        try:
            for player in players:
                print(f"Đang tìm giá: {player}...", end=" ")
                try:
                    self.driver.uc_open_with_reconnect("https://www.footballtransfers.com/en/search", 3)

                    search_xpath = "//*[@id='search-form']/input[2]"
                    self.driver.type(search_xpath, player + "\n", timeout=10)

                    try:
                        value_xpath = "//*[@id='search-results']/div[1]/a[1]/div[3]/span"
                        price = self.driver.get_text(value_xpath, timeout=10)
                        print(f"-> TÌM THẤY: {price}")
                    except:
                        print(f"-> KHÔNG CÓ GIÁ.")
                        price = "N/a"

                    transfer_data.append({"Player": player, "Transfer_Value": price})
                    count += 1

                    if count % 20 == 0:
                        df_batch = pd.DataFrame(transfer_data)
                        mode = 'replace' if count == 20 else 'append'
                        self.save_to_sqlite(df_batch, table_name="player_transfer_values", mode=mode)
                        transfer_data = []
                        print(f"--- Đã lưu tạm {count} cầu thủ vào DB ---")

                    time.sleep(2)

                except Exception as e:
                    print(f"Lỗi web: {e}")
                    transfer_data.append({"Player": player, "Transfer_Value": "N/a"})
                    count += 1

        # BẮT SỰ KIỆN BẤM DỪNG (CTRL + C)
        except KeyboardInterrupt:
            print("\n\n Nhận được lệnh dừng khẩn cấp (Ctrl+C) từ bạn!")
            print("Đang tự động kích hoạt quy trình lưu nốt dữ liệu còn sót lại...")

        # KHỐI FINALLY: LUÔN CHẠY DÙ LÀ CHẠY XONG HẾT HAY BỊ BẤM DỪNG
        finally:
            # Lưu vét phần còn dư trong bộ nhớ
            if transfer_data:
                # Logic xác định:
                # Nếu chưa lưu đợt nào (count <= số lượng trong mảng dư) thì tạo bảng mới (replace)
                # Nếu đã từng lưu rồi (count > số lượng trong mảng dư) thì ghi nối tiếp (append)
                mode = 'replace' if count <= len(transfer_data) else 'append'

                df_batch = pd.DataFrame(transfer_data)
                self.save_to_sqlite(df_batch, table_name="player_transfer_values", mode=mode)
                print(f"--- Đã LƯU VÉT an toàn {len(transfer_data)} cầu thủ cuối cùng ---")

            print(f"--- TỔNG KẾT: Đã cào và lưu thành công {count} cầu thủ ---")

        # Lưu vét phần còn dư (nếu số lượng không chia hết cho 20)
        if transfer_data:
            mode = 'replace' if count <= 20 else 'append'
            df_batch = pd.DataFrame(transfer_data)
            self.save_to_sqlite(df_batch, table_name="player_transfer_values", mode=mode)
            print(f"--- Đã lưu tổng cộng {count} cầu thủ ---")

    def close_browser(self):
        self.driver.quit()
if __name__ == "__main__":
    scraper = TransferScraper()
    try:
        scraper.scrape_transfer_values()
    finally:
        # Luôn đảm bảo trình duyệt được đóng dù có lỗi xảy ra
        scraper.close_browser()
