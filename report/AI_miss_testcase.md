# Additional Test Cases Missed by AI (Security & State Transitions)

**MSSV:** 23120228 | **Thành viên:** M4  
**Phạm vi:** FR-03 (Forgot & Reset Password), FR-09 (Apply Coupon), FR-19 (Admin User Management)

---

## Danh sách 5 Test Cases bổ sung & Phân tích nguyên nhân AI bỏ sót

| STT | Test Case ID & Feature | Loại kiểm thử | Kịch bản thực thi (Scenario) | Kết quả mong đợi (Expected Result) | Lý do AI bỏ sót (Root Cause Analysis) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **TC-FR03-EXT01**<br>*(FR-03: Reset Password)* | **State Transition**<br>*(Time-based)* | Gọi `POST /api/forgot-password` để lấy `resetToken`, chờ vượt quá thời hạn hiệu lực (ví dụ $> 5$ phút) rồi mới gửi `POST /api/reset-password`. | `400 Bad Request` (Thông báo mã OTP đã hết hạn). | **Characteristics of the API & Model limitations:** Đặc tả API và CSDL của SUT không có trường timestamp (`token_expired_at`). Đồng thời, AI thường chỉ sinh test tĩnh theo cặp request/response mà bỏ qua chuyển đổi trạng thái theo trục thời gian (Time-based State). |
| **2** | **TC-FR03-EXT02**<br>*(FR-03: Reset Password)* | **Security**<br>*(Brute-force / Rate Limit)* | Gửi liên tiếp 10 request đoán mã OTP ngẫu nhiên sai tới `POST /api/reset-password` cho cùng một email. | `429 Too Many Requests` hoặc khóa/vô hiệu hóa OTP sau 5 lần nhập sai liên tiếp. | **Prompt quality & Model limitations:** AI mặc định ưu tiên các mã lỗi chức năng phổ biến (`200`/`400`) và không tự sinh kịch bản kiểm thử an ninh chống tấn công vét cạn (Brute-force / Rate Limiting) nếu prompt không chỉ định rõ yêu cầu phi chức năng này. |
| **3** | **TC-FR09-EXT02**<br>*(FR-09: Apply Coupon)* | **State Transition**<br>*(Cross-endpoint)* | User áp dụng mã `SAVE10` (giới hạn 1 lần/user) và đặt hàng thành công $\rightarrow$ gọi `PUT /api/orders/:id/cancel` để hủy đơn $\rightarrow$ gọi lại `POST /api/apply-coupon` với mã `SAVE10`. | `200 OK` (Lượt sử dụng mã giảm giá được hoàn lại cho user sau khi hủy đơn). | **Prompt quality & Characteristics of the API:** Prompt chỉ cung cấp ngữ cảnh cô lập của endpoint `/api/apply-coupon`, nên AI không tự liên kết vòng đời mã giảm giá với chu trình hủy đơn (Order Cancellation Lifecycle) ở một endpoint khác. |
| **4** | **TC-FR09-EXT01**<br>*(FR-09: Apply Coupon)* | **Security & State Transition**<br>*(Race Condition)* | Gửi đồng thời 2 request sử dụng cùng mã `SAVE10` (giới hạn 1 lần dùng) trên cùng một tài khoản trong cùng một mili-giây. | Chỉ duy nhất 1 đơn hàng được áp dụng mã giảm giá; request thứ 2 bị từ chối với `400 Bad Request`. | **Model limitations:** AI có xu hướng thiết kế test case chạy tuần tự (Sequential testing), không tự động mô phỏng các kịch bản bất đồng bộ và tấn công tranh chấp đồng thời (Concurrency / Race Condition) khi DB chưa kịp ghi nhận vào bảng `coupon_usage`. |
| **5** | **TC-FR19-EXT02**<br>*(FR-19: Admin Users)* | **Security & State Integrity** | Khi hệ thống chỉ còn duy nhất 1 tài khoản có quyền `admin`, thực hiện gọi `DELETE /api/admin/users/:id` lên chính tài khoản Admin cuối cùng đó. | `400 Bad Request` (Từ chối xóa vì hệ thống phải duy trì tối thiểu 1 Quản trị viên hoạt động). | **Characteristics of the API:** Đặc tả FR-19 chỉ nêu ràng buộc cục bộ là *"không tự xóa chính mình"* (self-deletion), không đề cập đến ràng buộc bất biến toàn hệ thống (system-wide invariant), nên AI không tự suy luận ra kịch bản mất hoàn toàn quyền quản trị. |

---

## Tóm tắt nhóm nguyên nhân AI bỏ sót

1. **Prompt Quality:** Khi prompt chỉ tập trung vào từng endpoint riêng lẻ và các luồng chức năng chính, AI sẽ bỏ qua các yêu cầu phi chức năng (Rate Limiting) và các luồng nghiệp vụ liên kết giữa nhiều endpoint (Cross-endpoint State Transitions).
2. **Model Limitations:** Mô hình ngôn ngữ có xu hướng sinh test case theo luồng tĩnh và tuần tự, ít khi tự suy luận các bài test phụ thuộc trục thời gian (Expiration Timeout) hoặc tranh chấp đồng thời (Race Condition).
3. **Characteristics of the API:** Đặc tả API thiếu các trường dữ liệu thời gian (như `token_expired_at`) và chỉ mô tả ràng buộc cục bộ thay vì các ràng buộc toàn vẹn ở mức toàn hệ thống (System-wide Invariants).