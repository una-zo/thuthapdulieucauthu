# PHÂN TÍCH DỮ LIỆU CẦU THỦ NGOẠI HẠNG ANH MÙA GIẢI 2024–2025

## Giới thiệu

Dự án được thực hiện trong khuôn khổ bài tập nhóm môn Lập trình Python, với mục tiêu thu thập, lưu trữ, truy vấn và phân tích dữ liệu cầu thủ thuộc giải bóng đá Ngoại hạng Anh (Premier League) mùa giải 2024–2025.

Dự án sử dụng Python để thu thập dữ liệu từ các nguồn trực tuyến, lưu trữ bằng SQLite, xây dựng API phục vụ truy vấn thông tin và thực hiện phân tích thống kê nhằm đánh giá hiệu suất cầu thủ cũng như đề xuất phương pháp định giá cầu thủ dựa trên dữ liệu.

## I. Thu thập và lưu trữ dữ liệu

### I.1. Thu thập dữ liệu thống kê cầu thủ

- Thu thập dữ liệu thống kê cầu thủ Ngoại hạng Anh mùa giải 2024–2025 từ FBref.
- Lựa chọn các cầu thủ có tổng thời gian thi đấu lớn hơn 90 phút.
- Lưu trữ thông tin và các chỉ số thống kê của cầu thủ vào cơ sở dữ liệu SQLite.
- Xử lý các giá trị bị thiếu hoặc không áp dụng theo yêu cầu của đề bài.

### I.2. Thu thập giá trị chuyển nhượng cầu thủ

- Thu thập thông tin giá trị chuyển nhượng của cầu thủ từ FootballTransfers.
- Kết hợp dữ liệu giá trị chuyển nhượng với dữ liệu thống kê cầu thủ.
- Lưu trữ thông tin vào bảng dữ liệu riêng trong SQLite để phục vụ truy vấn và phân tích.

### Công nghệ sử dụng

Python, Requests/Selenium, SQLite.

## II. Xây dựng API và chương trình truy vấn dữ liệu

### II.1. Xây dựng RESTful API

- Sử dụng Flask để xây dựng API truy vấn dữ liệu cầu thủ.
- Hỗ trợ tìm kiếm thông tin cầu thủ theo tên hoặc câu lạc bộ.
- Trả về dữ liệu từ cơ sở dữ liệu để các chương trình khác có thể sử dụng.

### II.2. Xây dựng chương trình truy vấn bằng Python

- Sử dụng thư viện Requests để gửi yêu cầu đến API.
- Xây dựng chương trình dòng lệnh cho phép tra cứu cầu thủ theo tên hoặc câu lạc bộ.
- Hiển thị kết quả truy vấn dưới dạng bảng.
- Hỗ trợ xuất dữ liệu truy vấn ra tệp CSV.

### Công nghệ sử dụng

Python, Flask, Requests, SQLite, CSV.

## III. Phân tích và đánh giá dữ liệu

### III.1. Phân tích thống kê cầu thủ theo câu lạc bộ

- Tính giá trị trung bình (Mean), trung vị (Median) và độ lệch chuẩn (Standard Deviation) của các chỉ số thống kê cầu thủ theo từng câu lạc bộ.
- Xuất kết quả thống kê ra tệp CSV để thuận tiện cho việc tổng hợp và so sánh.
- Xác định câu lạc bộ có giá trị cao nhất đối với từng chỉ số.
- Dựa trên kết quả thu được để thảo luận về hiệu suất thi đấu của các câu lạc bộ trong mùa giải 2024–2025.

### III.2. Đề xuất phương pháp định giá cầu thủ

- Phân tích mối liên hệ giữa các chỉ số thống kê thi đấu và giá trị chuyển nhượng của cầu thủ.
- Đề xuất phương pháp định giá dựa trên các đặc trưng dữ liệu phù hợp.
- Đánh giá những yếu tố có thể ảnh hưởng đến giá trị cầu thủ và các hạn chế của phương pháp đề xuất.

### Kết quả

- Bộ dữ liệu cầu thủ được thu thập và lưu trữ trong SQLite.
- Các kết quả thống kê được tổng hợp và xuất ra CSV.
- Báo cáo phân tích hiệu suất cầu thủ theo câu lạc bộ.
- Đề xuất phương pháp định giá cầu thủ dựa trên dữ liệu thống kê.

## Công nghệ sử dụng

- **Ngôn ngữ:** Python
- **Thu thập dữ liệu:** Requests, Selenium
- **Cơ sở dữ liệu:** SQLite
- **Xử lý dữ liệu:** Pandas, NumPy
- **Xây dựng API:** Flask
- **Lưu trữ kết quả:** CSV

## Mục đích dự án

Dự án giúp vận dụng Python vào quy trình thu thập, lưu trữ, truy vấn và phân tích dữ liệu thực tế; đồng thời rèn luyện kỹ năng xử lý dữ liệu, làm việc với cơ sở dữ liệu và xây dựng API.
