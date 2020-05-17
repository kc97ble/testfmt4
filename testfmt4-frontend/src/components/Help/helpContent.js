export const helpContent = `

TEST FORMATTER 4

Trang web chuyển định dạng bộ test

Tác giả: Nguyễn Tiến Trung Kiên
Link GitHub: https://github.com/kc97ble/testfmt4

HƯỚNG DẪN

Để định dạng một bộ test, các bạn làm theo các bước sau:
1. Nén bộ test lại thành một file ZIP
2. Vào trang chủ của Test Formatter 4, upload nó lên
3. Có hai cột: Before (trước) và After (sau). Điền định dạng của bộ test vào đây.
(Xem mục "Cú pháp cho format" để biết thêm chi tiết)
4. Xem trước kết quả ở phần Preview bên dưới.
5. Nhấn Download để tải về.

CÚ PHÁP CHO FORMAT

Format là một xâu ký tự chứa đúng một wildcard. Có các loại wildcard sau đây:
- '*' (dấu sao): khớp một xâu bất kỳ
- '0' (số 0): khớp dãy 0, 1, 2, 3, ..., 9, 10, 11, 12, ...
- '1' (số 1): khớp dãy 1, 2, 3, 4, ..., 9, 10, 11, 12, ...
- '00': khớp dãy 00, 01, 02, 03, ..., 09, 10, 11, 12, ..., 99, 100, 101, ...
- '01': khớp dãy 01, 02, 03, 04, ..., 09, 10, 11, 12, ..., 99, 100, 101, ...
- '000', '001', '0000', '0001': tương tự như trên

VÍ DỤ

1. CMS
Để chuyển đổi bộ test sang format của CMS, các bạn có thể sử dụng format sau:
- Input format: input.000
- Output format: output.000

2. THEMIS
Để chuyển đổi bộ test sang format của Themis, các bạn có thể sử dụng format sau:
- Input format: TEST01/APPLE.INP
- Output format: TEST01/APPLE.OUT

LƯU Ý

- Hiện tại, trang web chỉ hỗ trợ tệp ZIP
- Sử dụng dấu '/' (slash) thay vì dấu '\' (backslash) trong đường dẫn.
- Các bạn có thể copy link để chia sẻ bộ test cho người khác. Tuy nhiên, các bộ test lâu ngày sẽ bị xóa đi sau một thời gian.

BÁO LỖI

Nếu thấy lỗi, vui lòng tạo Issue trên GitHub: https://github.com/kc97ble/testfmt4
Hoặc nhắn tin qua Facebook cho mình: https://www.facebook.com/nttkien

THÔNG TIN KHÁC

Trang web này là một sản phầm của "Thử thách 36 tiếng".
Mình đã code nó trong 3 ngày, mỗi ngày 12 tiếng.

`;
