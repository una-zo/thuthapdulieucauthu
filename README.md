Bài Tập Lập Trình Với Python
I.
Viết chương trình Python thu thập dữ liệu phân tích cầu thủ với yêu cầu như sau:
I.1
- Thu thập dữ liệu thống kê của tất cả các cầu thủ có số phút thi đấu nhiều hơn 90 phút tại giải bóng đá ngoại hạng Anh mùa 2024-2025.
- Nguồn dữ liệu: https://fbref.com/en/
- Ghi kết quả vào một bảng trong cơ sở dữ liệu SQLite, bảng kết quả có cấu trúc như sau:
	+ Mỗi cột tương ứng với một chỉ số.
	+ Chỉ số nào không có hoặc không áp dụng thì để là N/a
	+ Tham khảo: https://fbref.com/en/squads/822bd0ba/2023-2024//en/squads/822bd0ba/2023-2024/Liverpool-Stats
I.2
-  Với mỗi cầu thủ được ghi trong bảng trên, thu thập giá chuyển nhượng của cầu thủ trong mùa 2024-2025 từ trang web https://www.footballtransfers.com. Nếu không có dữ liệu thì để là N/a
- Kết quả ghi vào một bảng thứ hai trong cơ sở dữ liệu SQLite.
Chú ý: 
Trong khi crawl dữ liệu, có thể gặp các tình huống như Capchar và hoặc rate-limit. Đề xuất phương pháp khắc phục nếu có
Có thể dùng module request hoặc selenium để cào dữ liệu.
II.
II.1
Sử dụng module Python Flask để tạo các Restful API tra cứu chỉ số cầu thủ trong cơ sở dữ liệu vừa tạo ở câu 1 theo các tiêu chí sau:
-	Tên cầu thủ: trả về toàn bộ chỉ số của cầu thủ có tên tương ứng.
-	Câu lạc bộ: Trả về toàn bộ chỉ số của các cầu thủ thuộc về câu lạc bộ đó.
II.2
Sử dụng module Request, viết 1 chương trình python để tra cứu dữ liệu cầu thủ theo 2 tiêu chí như trên. Tên cầu thủ hoặc câu lạc bộ được truyền vào lúc chạy chương trình có cú pháp như sau:
./> python lookup.py  --name  <tên cầu thủ>  --club <tên câu lạc bộ> 
-	Kết quả trả ra được in ra màn hình dưới dạng bảng, và 1 file CSV. Tên file được đặt theo tên cầu thủ hoặc câu lạc bộ, tùy theo sử dụng tham số đầu vào.
III.
III.1
- Tìm trung vị, trung bình và độ lệch chuẩn của mỗi chỉ số các cầu thủ của mỗi đội. Ghi kết quả vào 1 file CSV.
- Tìm đội bóng có chỉ số điểm số cao nhất ở mỗi chỉ số. Theo bạn đội nào có phong độ tốt nhất giải ngoại Hạng Anh mùa 2024-2025
III.2
- Dựa vào kết quả từ câu I, đề xuất 1 phương pháp định giá cầu thủ.
IV.
- Sử dụng thuật toán K-means để phân loại các cầu thủ thành các nhóm có chỉ số tương tự nhau.
- Theo bạn thì nên phân loại cầu thủ thành bao nhiêu nhóm? Vì sao (gợi ý: sử dụng biểu đồ Elbow và Silhoute, vẽ 2 biểu đồ này)? Bạn có Nhận xét gì về kết quả.
- Sử dụng thuật toán PCA, giảm số chiều dữ liệu xuống 2 chiều, 3 chiều, vẽ hình scatter plot phân cụm các điểm dữ liệu trên mặt 2D, và khối 3D.

Hướng dẫn nộp bài:
-	Mỗi nhóm tối đa 3 thành viên
-	Bài làm bao gồm  Python code và báo cáo (định dạng pdf).
-	Báo cáo cần trình bày lý giải cách làm, thuật toán áp dụng và các kết quả đạt được
-	Cách nộp: 
o	Mỗi nhóm tạo một github repository, để chế độ private và add giảng viên vào repository này. Tên github của giảng viên: vinhlv.ptit@gmail.com
o	Repository được chia làm 2 thư mục:
	1 thư mục chứa file báo cáo
	1 thư mục chứ source code
-	Deadline: 23:59 Ngày 4/05/2026
-	Các nhóm cũng sẽ phải thực hiện chạy thử source code trên lớp.
