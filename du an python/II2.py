import requests
import argparse
import pandas as pd

# Địa chỉ Server Flask đang chạy (đảm bảo vẫn đang chạy app.py ở terminal khác)
BASE_URL = "http://127.0.0.1:5000/api"

def lookup():
    # Thiết lập bộ đọc tham số dòng lệnh (argparse)
    parser = argparse.ArgumentParser(description="Công cụ tra cứu dữ liệu cầu thủ Ngoại hạng Anh.")
    parser.add_argument("--name", type=str, help="Tìm kiếm theo tên cầu thủ")
    parser.add_argument("--club", type=str, help="Tìm kiếm theo tên câu lạc bộ")
    
    args = parser.parse_args()

    # Kiểm tra xem người dùng có nhập tham số nào không
    if not args.name and not args.club:
        print("Lỗi: Bạn phải nhập ít nhất một tham số --name hoặc --club.")
        parser.print_help()
        return

    # Xác định API cần gọi và tên file CSV sẽ lưu
    if args.name:
        api_url = f"{BASE_URL}/player?name={args.name}"
        filename = f"{args.name.replace(' ', '_')}.csv"
        search_type = "Cầu thủ"
    else:
        api_url = f"{BASE_URL}/club?name={args.club}"
        filename = f"{args.club.replace(' ', '_')}.csv"
        search_type = "Câu lạc bộ"

    try:
        # Gọi API bằng module requests
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Chuyển dữ liệu sang DataFrame để xử lý
            df = pd.DataFrame(data)
            
            # In kết quả ra màn hình dưới dạng bảng
            print(f"\n Kết quả tìm kiếm cho {search_type}:")
            print("=" * 50)
            print(df.to_string(index=False)) # In bảng đẹp đẽ
            print("=" * 50)
            
            # Xuất ra file CSV
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f" Đã lưu dữ liệu vào file: {filename}")
            
        else:
            # Xử lý khi không tìm thấy hoặc server lỗi
            error_msg = response.json().get('message', 'Lỗi không xác định')
            print(f" Không tìm thấy kết quả: {error_msg}")

    except requests.exceptions.ConnectionError:
        print(" Lỗi: Không thể kết nối tới Server Flask")

if __name__ == "__main__":
    lookup()
