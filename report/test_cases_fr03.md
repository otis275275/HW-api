# Test Case Specification — Pool A: FR-03 (Forgot & Reset Password)

**MSSV:** 23120228 | **Thành viên:** M4  
**Target Endpoints:**
- `POST /api/forgot-password`
- `POST /api/reset-password`  
**Base URL:** `http://localhost:3000`  
**Header bắt buộc:** `X-Student-Id: 23120228`

---

## 1. Danh sách Test Cases sinh bởi AI (Target $\ge 35$ Test Cases)

| Test Case ID | Mục kiểm thử | Endpoint & Method | Input Data / Payload | Kết quả mong đợi (Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FR03-01** | DP - Email hợp lệ tồn tại | `POST /api/forgot-password` | `{"email": "test@eshop.com"}` | 200 OK, trả về `message` và `resetToken` |
| **TC-FR03-02** | DP - Email không tồn tại | `POST /api/forgot-password` | `{"email": "notfound@domain.com"}` | 404 Not Found, thông báo lỗi |
| **TC-FR03-03** | DP - Email rỗng | `POST /api/forgot-password` | `{"email": ""}` | 400 Bad Request |
| **TC-FR03-04** | DP - Thiếu trường email | `POST /api/forgot-password` | `{}` | 400 Bad Request |
| **TC-FR03-05** | DP - Email thiếu ký tự `@` | `POST /api/forgot-password` | `{"email": "testeshop.com"}` | 400 Bad Request |
| **TC-FR03-06** | DP - Email thiếu phần domain | `POST /api/forgot-password` | `{"email": "test@"}` | 400 Bad Request |
| **TC-FR03-07** | DP - Email có khoảng trắng thừa | `POST /api/forgot-password` | `{"email": "  test@eshop.com  "}` | 200 OK (trim) hoặc 400 |
| **TC-FR03-08** | DP - Email quá dài (>255 ký tự) | `POST /api/forgot-password` | `{"email": "a"*250 + "@eshop.com"}` | 400 Bad Request |
| **TC-FR03-09** | DP - SQLi trong trường email | `POST /api/forgot-password` | `{"email": "' OR '1'='1"}` | 400 Bad Request |
| **TC-FR03-10** | DP - XSS script trong email | `POST /api/forgot-password` | `{"email": "<script>alert(1)</script>@domain.com"}` | 400 Bad Request |
| **TC-FR03-11** | DP - Email định dạng Uppercase | `POST /api/forgot-password` | `{"email": "TEST@ESHOP.COM"}` | 200 OK (case-insensitive) |
| **TC-FR03-12** | DP - ResetToken hợp lệ | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{activeResetToken}}", "newPassword": "NewPassword123!"}` | 200 OK, `Password reset successfully` |
| **TC-FR03-13** | DP - ResetToken không đúng | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "000000", "newPassword": "NewPassword123!"}` | 400 Bad Request |
| **TC-FR03-14** | DP - ResetToken rỗng | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "", "newPassword": "NewPassword123!"}` | 400 Bad Request |
| **TC-FR03-15** | DP - Thiếu resetToken | `POST /api/reset-password` | `{"email": "test@eshop.com", "newPassword": "NewPassword123!"}` | 400 Bad Request |
| **TC-FR03-16** | DP - ResetToken là chuỗi chữ | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "ABCDEF", "newPassword": "NewPassword123!"}` | 400 Bad Request |
| **TC-FR03-17** | DP - ResetToken quá ngắn (< 4 số) | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "12", "newPassword": "NewPassword123!"}` | 400 Bad Request |
| **TC-FR03-18** | DP - ResetToken quá dài (> 6 số) | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "12345678", "newPassword": "NewPassword123!"}` | 400 Bad Request |
| **TC-FR03-19** | DP - SQLi trong resetToken | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "' OR 1=1 --", "newPassword": "NewPassword123!"}` | 400 Bad Request |
| **TC-FR03-20** | DP - Mật khẩu mới mạnh hợp lệ | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "SecurePass123!"}` | 200 OK |
| **TC-FR03-21** | DP - Mật khẩu mới quá ngắn (< 8 ký tự) | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "Pass1!"}` | 400 Bad Request (vi phạm FR-01) |
| **TC-FR03-22** | DP - Mật khẩu thiếu chữ hoa | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "password123!"}` | 400 Bad Request |
| **TC-FR03-23** | DP - Mật khẩu thiếu chữ thường | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "PASSWORD123!"}` | 400 Bad Request |
| **TC-FR03-24** | DP - Mật khẩu thiếu chữ số | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "PasswordSpecial!"}` | 400 Bad Request |
| **TC-FR03-25** | DP - Mật khẩu thiếu ký tự đặc biệt | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "Password123"}` | 400 Bad Request |
| **TC-FR03-26** | DP - Mật khẩu mới rỗng | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": ""}` | 400 Bad Request |
| **TC-FR03-27** | DP - Mật khẩu toàn khoảng trắng | `POST /api/reset-password` | `{"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "        "}` | 400 Bad Request |
| **TC-FR03-28** | ST - Luồng đầy đủ: Forgot -> Reset -> Login | Sequence: Forgot -> Reset -> Login | Lấy token -> Đặt pass mới -> Đăng nhập pass mới | 200 OK ở cả 3 bước |
| **TC-FR03-29** | ST - Token hủy sau khi dùng 1 lần | Sequence: Forgot -> Reset (1) -> Reset (2) | Thử đặt lại lần 2 bằng cùng token | Lần 1: 200 OK, Lần 2: 400 Bad Request |
| **TC-FR03-30** | ST - Đăng nhập bằng pass cũ sau reset | Sequence: Reset pass -> Login pass cũ | `password: Test1234!` | 401 Unauthorized |
| **TC-FR03-31** | ST - Yêu cầu OTP 2 lần liên tiếp | Sequence: Forgot (1) -> Forgot (2) | Kiểm tra tính hiệu lực của Token cũ | Token cũ bị vô hiệu, Token mới có hiệu lực |
| **TC-FR03-32** | SEC - Kiểm tra độ dài OTP (SEC-07) | `POST /api/forgot-password` | `{"email": "test@eshop.com"}` | OTP phải có độ dài $\ge 6$ ký tự số |
| **TC-FR03-33** | SEC - Dùng OTP User A cho User B | `POST /api/reset-password` | `{"email": "admin@eshop.com", "resetToken": "{{activeResetToken}}", ...}` | 400 Bad Request (Cross-account attack) |
| **TC-FR03-34** | SEC - Bảo mật mật khẩu (SEC-01) | `POST /api/reset-password` | `{"email": "test@eshop.com", ...}` | Phản hồi không trả về password dạng plaintext |
| **TC-FR03-35** | Schema - Schema của Forgot Password | `POST /api/forgot-password` | `{"email": "test@eshop.com"}` | Body đúng JSON schema: `{message: string, resetToken: string}` |
| **TC-FR03-36** | Schema - Schema của Reset Password | `POST /api/reset-password` | `{"email": "test@eshop.com", ...}` | Body đúng JSON schema: `{message: string}` |

---

## 2. Bảng Human Audit Từng Test Case (36/36 Test Cases Evaluated)

Dưới đây là kết quả kiểm toán độc lập của sinh viên đối với từng ca kiểm thử do AI sinh ra, dán nhãn VALID / INVALID / INCOMPLETE kèm lý do và hành động hiệu chỉnh chi tiết:

| Test Case ID | Nhãn Kiểm toán | Lý do đánh giá của Sinh viên | Hành động Hiệu chỉnh (Correction) |
| :--- | :---: | :--- | :--- |
| **TC-FR03-01** | **VALID** | Thiết kế chuẩn happy-path cho email tồn tại. | Giữ nguyên. Lưu `resetToken` vào biến môi trường `activeResetToken`. |
| **TC-FR03-02** | **VALID** | Phân hoạch hợp lệ cho email chưa từng đăng ký. | Giữ nguyên assertion `status === 404`. |
| **TC-FR03-03** | **INCOMPLETE** | AI ban đầu dự kiến 400, nhưng SUT thực tế truy vấn CSDL tìm `email = ""` không thấy nên trả về 404. Ngoài ra script ban đầu nới lỏng `[400, 404]`. | **Hiệu chỉnh:** Siết chặt assertion bắt buộc kiểm tra đúng 400 Bad Request (chuẩn REST validation) để làm bằng chứng báo cáo lỗi thiếu validator input rỗng. |
| **TC-FR03-04** | **INCOMPLETE** | AI thiếu assertion kiểm tra trường hợp body rỗng `{}` dẫn tới `email = undefined`. | **Hiệu chỉnh:** Kiểm tra SUT trả về lỗi schema hoặc 400 Bad Request, không bị crash unhandled 500. |
| **TC-FR03-05** | **VALID** | Phân hoạch định dạng email thiếu `@`. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-06** | **VALID** | Phân hoạch định dạng email thiếu domain. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-07** | **VALID** | Kiểm tra xử lý khoảng trắng (Trimming). | Kiểm tra hệ thống tự trim và chấp nhận 200 hoặc trả về 400. |
| **TC-FR03-08** | **VALID** | Phân tích giá trị biên (BVA) độ dài chuỗi email (>255 ký tự). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-09** | **VALID** | Kiểm thử an ninh SQL Injection qua tham số email. | Đảm bảo server không trả về lỗi cú pháp SQLite (500) mà xử lý an toàn với 400/404. |
| **TC-FR03-10** | **VALID** | Kiểm thử an ninh chèn XSS payload trong email. | Đảm bảo hệ thống từ chối hoặc sanitize an toàn. |
| **TC-FR03-11** | **VALID** | Kiểm thử tính không phân biệt hoa thường (Case-insensitive) của email. | Giữ nguyên. |
| **TC-FR03-12** | **VALID** | Happy-path đặt lại mật khẩu với token hợp lệ. | Giữ nguyên. Sử dụng `activeResetToken` hợp lệ vừa sinh ra. |
| **TC-FR03-13** | **VALID** | Kiểm thử giá trị token sai không khớp DB. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-14** | **VALID** | Kiểm thử phân hoạch giá trị biên token rỗng `""`. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-15** | **VALID** | Kiểm thử trường hợp thiếu thuộc tính `resetToken`. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-16** | **VALID** | Kiểm thử kiểu dữ liệu sai (string ký tự chữ `ABCDEF`). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-17** | **VALID** | Kiểm thử độ dài token quá ngắn (< 4 số). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-18** | **VALID** | Kiểm thử độ dài token quá dài (> 6 số). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-19** | **VALID** | Kiểm thử SQL Injection trong tham số token. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-20** | **INCOMPLETE** | AI dùng token cũ đã hết hạn sau TC-12, dẫn đến test case bị fail vì sai token chứ không phải do mật khẩu. | **Hiệu chỉnh:** Tạo request phụ trợ lấy token mới (`freshResetToken`) trước khi kiểm tra đặt mật khẩu mạnh. |
| **TC-FR03-21** | **INVALID** | **Pass ảo nghiêm trọng:** AI xếp TC này sau TC-12 nhưng dùng lại token cũ đã bị hủy. Server trả về 400 "Invalid token" khiến assertion `status === 400` tưởng là Pass, nhưng thực chất SUT không hề validate mật khẩu yếu! | **Hiệu chỉnh:** Viết Pre-request Script tự động gửi `POST /api/forgot-password` để lấy một mã OTP hoàn toàn mới trước khi gửi pass yếu `Pass1!`. Kết quả thực tế SUT trả về 200 OK $\rightarrow$ Phát hiện và khẳng định chính xác **BUG-M4-02**! |
| **TC-FR03-22** | **INVALID** | Lỗi Pass ảo tương tự TC-21 khi test mật khẩu thiếu chữ hoa (`password123!`). | **Hiệu chỉnh:** Bổ sung Pre-request Script cấp token tươi mới để bắt đúng lỗi SUT thiếu validator chữ hoa. |
| **TC-FR03-23** | **INVALID** | Lỗi Pass ảo tương tự TC-21 khi test mật khẩu thiếu chữ thường (`PASSWORD123!`). | **Hiệu chỉnh:** Bổ sung Pre-request Script cấp token tươi mới để bắt đúng lỗi SUT thiếu validator chữ thường. |
| **TC-FR03-24** | **INVALID** | Lỗi Pass ảo tương tự TC-21 khi test mật khẩu thiếu số (`PasswordSpecial!`). | **Hiệu chỉnh:** Bổ sung Pre-request Script cấp token tươi mới để bắt đúng lỗi SUT thiếu validator chữ số. |
| **TC-FR03-25** | **INVALID** | Lỗi Pass ảo tương tự TC-21 khi test mật khẩu thiếu ký tự đặc biệt (`Password123`). | **Hiệu chỉnh:** Bổ sung Pre-request Script cấp token tươi mới để bắt đúng lỗi SUT thiếu validator ký tự đặc biệt. |
| **TC-FR03-26** | **INVALID** | Lỗi Pass ảo tương tự TC-21 khi test mật khẩu rỗng `""`. | **Hiệu chỉnh:** Cấp token tươi mới để kiểm tra SUT chấp nhận mật khẩu rỗng. |
| **TC-FR03-27** | **INVALID** | Lỗi Pass ảo tương tự TC-21 khi test mật khẩu toàn khoảng trắng. | **Hiệu chỉnh:** Cấp token tươi mới để kiểm tra SUT chấp nhận mật khẩu rỗng/whitespace. |
| **TC-FR03-28** | **VALID** | Kiểm thử chuỗi chuyển trạng thái đầy đủ 3 bước (Forgot $\rightarrow$ Reset $\rightarrow$ Login). | Tách rõ ràng 3 request liên hoàn, truyền token tự động qua biến `stResetToken`. |
| **TC-FR03-29** | **VALID** | Kiểm thử tính chất dùng một lần (One-time token): dùng lại token cũ sau khi đã đổi pass. | Giữ nguyên assertion mong đợi 400 Bad Request. |
| **TC-FR03-30** | **INCOMPLETE** | AI bị đánh số nhầm giữa đăng nhập pass cũ và pass mới. | **Hiệu chỉnh:** Chuẩn hóa lại thứ tự: TC-30 đăng nhập bằng mật khẩu CŨ `Test1234!` (mong đợi 401 Unauthorized). |
| **TC-FR03-31** | **INCOMPLETE** | AI bị đánh số nhầm với TC-30. | **Hiệu chỉnh:** Chuẩn hóa lại thứ tự: TC-31 gọi 2 lần forgot liên tiếp để kiểm tra cơ chế ghi đè token mới và vô hiệu token cũ. |
| **TC-FR03-32** | **VALID / CRITICAL** | Kiểm tra ràng buộc an ninh mật mã SEC-07: OTP phải $\ge 6$ chữ số. | Đặt assertion: `pm.expect(json.resetToken.length).to.be.at.least(6)` $\rightarrow$ Bắt chính xác **BUG-M4-01** (SUT chỉ sinh 4 số). |
| **TC-FR03-33** | **VALID** | Kiểm thử an ninh tấn công chéo tài khoản (Dùng OTP User này đổi pass Admin). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR03-34** | **VALID** | Kiểm tra rò rỉ thông tin mật khẩu (SEC-01). | Đặt assertion kiểm tra body text không chứa plaintext password. |
| **TC-FR03-35** | **VALID** | Kiểm định JSON Schema contract của `/api/forgot-password`. | Bổ sung kiểm tra kiểu dữ liệu `message: string` và `resetToken: string`. |
| **TC-FR03-36** | **VALID** | Kiểm định JSON Schema contract của `/api/reset-password`. | Bổ sung kiểm tra cấu trúc lỗi `error: string`. |

---

## 3. Mở rộng (+5 Test Cases nâng cao AI bỏ sót & Giải thích)

| Test Case ID | Mục kiểm thử mở rộng | Input / Kịch bản thực thi | Kết quả mong đợi | Giải thích tại sao AI bỏ sót |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FR03-EXT01** | **Thời hạn hết hạn của OTP (Expiration Timeout)** | Gửi yêu cầu Forgot, đợi vượt quá thời hạn (ví dụ > 5 phút) rồi mới gọi Reset Password. | 400 Bad Request (Mã OTP đã hết hạn). | AI thường chỉ sinh test dựa trên request/response tĩnh, không tự suy luận về trục thời gian (Time-based State) nếu spec không ghi rõ trường timestamp. Trong code SUT, DB thậm chí không lưu cột `token_expired_at`! |
| **TC-FR03-EXT02** | **Chống Brute-force OTP (Rate Limiting)** | Gửi 10 request đoán mã OTP liên tiếp với các mã ngẫu nhiên sai trên endpoint `/api/reset-password`. | 429 Too Many Requests hoặc khóa OTP sau 5 lần đoán sai. | AI tập trung vào các status code 200/400 thông thường mà bỏ qua khía cạnh kiểm thử an ninh chống tấn công vét cạn (Brute-force attack on low-entropy tokens). |
| **TC-FR03-EXT03** | **Ngăn chặn đặt lại mật khẩu trùng mật khẩu cũ** | Gọi `/api/reset-password` với `newPassword` giống hệt mật khẩu hiện tại (`Test1234!`). | 400 Bad Request (Mật khẩu mới không được trùng mật khẩu cũ). | Đặc tả API không nêu rõ ràng rule này, nên AI chỉ bám vào validation cú pháp mà bỏ sót ràng buộc lịch sử mật khẩu (Password History Policy). |
| **TC-FR03-EXT04** | **Tranh chấp đồng thời (Race Condition on Reset)** | Gửi đồng thời 2 request reset password với cùng một token qua 2 luồng song song. | Chỉ có duy nhất 1 request thành công, request còn lại bị từ chối 400. | AI sinh test case tuần tự (Sequential testing) và không tự động mô phỏng các kịch bản bất đồng bộ / tấn công tranh chấp tài nguyên (Concurrency / Race Condition). |
| **TC-FR03-EXT05** | **Bảo mật phản hồi tránh User Enumeration** | Gửi email không tồn tại tới `/api/forgot-password`. Trong hệ thống chuẩn, thông báo nên chung chung: *"Nếu email tồn tại, mã đã được gửi"*. | 200 OK hoặc thông báo generic để tránh lộ thông tin người dùng. | SUT trả về 404 `"User not found"`, giúp hacker quét được danh sách email có trong hệ thống (User Enumeration Vulnerability). AI không nhận thức được khuyến nghị an toàn này nếu không được prompt chuyên sâu. |
