# Báo Cáo Chi Tiết Kết Quả Thực Thi Test Cases (Execution Failure Analysis)

**MSSV:** 23120228 | **Thành viên:** M4 | **Hệ thống:** EShop API (HW06)

## 1. Tổng quan thống kê Thực thi (Execution Summary)

- **Tổng số Requests đã thực thi:** 121
- **Tổng số Assertions đã đánh giá:** 128
- **Assertions ĐẠT (Passed):** 96 (Thỏa mãn yêu cầu)
- **Assertions THẤT BẠI (Failed):** 32 (Bắt lỗi phần mềm thực tế trong SUT)

---

## 2. Bảng Phân Tích Chi Tiết Các Test Case Thất Bại (Chỉ Rõ Bug Thật & Giá Trị Sai)

| STT | Tên Test Case & API | Assertion Kiểm tra | Giá trị Mong đợi (Expected) | Giá trị Thực tế từ SUT (Actual) | Mã Bug & Phân loại |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **#1** | TC-FR03-03: DP - Empty Email String | `Spec expects 400 Bad Request for empty email` | HTTP 400 Bad Request | HTTP 404 Not Found | Lỗi validation input rỗng |
| **#2** | TC-FR03-04: DP - Missing Email Field | `Missing email field yields 400 Bad Request` | Theo đặc tả | expected response to have status code 400 but got 404 | Lỗi nghiệp vụ SUT |
| **#3** | TC-FR03-05: DP - Email Missing @ Symbol | `Malformed email yields 400 Bad Request` | Theo đặc tả | expected response to have status code 400 but got 404 | Lỗi nghiệp vụ SUT |
| **#4** | TC-FR03-06: DP - Email Missing Domain | `Malformed email yields 400 Bad Request` | Theo đặc tả | expected response to have status code 400 but got 404 | Lỗi nghiệp vụ SUT |
| **#5** | TC-FR03-07: DP - Email with Extra Whitespace | `Trimmed email accepted 200 or 400 rejected` | Theo đặc tả | expected 404 to be one of [ 200, 400 ] | Lỗi nghiệp vụ SUT |
| **#6** | TC-FR03-08: DP - Email Exceeding Max Length (>255 chars) | `Overly long email yields 400 Bad Request` | Theo đặc tả | expected response to have status code 400 but got 404 | Lỗi nghiệp vụ SUT |
| **#7** | TC-FR03-21: DP - Weak Password Short (<8 chars) (BUG CHECK: SUT lacks password validator) | `[BUG-M4-02] Spec requires strong password, expect 400 Bad Request` | HTTP 400 Bad Request | HTTP 200 OK (SUT chấp nhận pass yếu) | **BUG-M4-02** (SEC-01/FR-01 Mật khẩu yếu) |
| **#8** | TC-FR03-22: DP - Password Missing Uppercase Letter (BUG CHECK: SUT lacks password validator) | `[BUG-M4-02] Spec requires strong password, expect 400 Bad Request` | HTTP 400 Bad Request | HTTP 200 OK (SUT chấp nhận pass yếu) | **BUG-M4-02** (SEC-01/FR-01 Mật khẩu yếu) |
| **#9** | TC-FR03-23: DP - Password Missing Lowercase Letter (BUG CHECK: SUT lacks password validator) | `[BUG-M4-02] Spec requires strong password, expect 400 Bad Request` | HTTP 400 Bad Request | HTTP 200 OK (SUT chấp nhận pass yếu) | **BUG-M4-02** (SEC-01/FR-01 Mật khẩu yếu) |
| **#10** | TC-FR03-24: DP - Password Missing Digit (BUG CHECK: SUT lacks password validator) | `[BUG-M4-02] Spec requires strong password, expect 400 Bad Request` | HTTP 400 Bad Request | HTTP 200 OK (SUT chấp nhận pass yếu) | **BUG-M4-02** (SEC-01/FR-01 Mật khẩu yếu) |
| **#11** | TC-FR03-25: DP - Password Missing Special Character (BUG CHECK: SUT lacks password validator) | `[BUG-M4-02] Spec requires strong password, expect 400 Bad Request` | HTTP 400 Bad Request | HTTP 200 OK (SUT chấp nhận pass yếu) | **BUG-M4-02** (SEC-01/FR-01 Mật khẩu yếu) |
| **#12** | TC-FR03-26: DP - Empty Password String (BUG CHECK: SUT lacks password validator) | `[BUG-M4-02] Spec requires strong password, expect 400 Bad Request` | HTTP 400 Bad Request | HTTP 200 OK (SUT chấp nhận pass yếu) | **BUG-M4-02** (SEC-01/FR-01 Mật khẩu yếu) |
| **#13** | TC-FR03-27: DP - Whitespace-only Password (BUG CHECK: SUT lacks password validator) | `[BUG-M4-02] Spec requires strong password, expect 400 Bad Request` | HTTP 400 Bad Request | HTTP 200 OK (SUT chấp nhận pass yếu) | **BUG-M4-02** (SEC-01/FR-01 Mật khẩu yếu) |
| **#14** | TC-FR03-32: SEC - Verify OTP Entropy >= 6 Digits (SEC-07 BUG CHECK) | `[BUG-M4-01 / SEC-07] OTP must be at least 6 digits long` | OTP length >= 6 chữ số | Chỉ sinh 4 chữ số (ví dụ: '1000'..'9999') | **BUG-M4-01** (SEC-07 OTP Entropy) |
| **#15** | TC-FR09-01: C1 - Valid Percent Coupon (SAVE10 - 10%) (BUG CHECK) | `[BUG-M4-04] Math check: 10% of 500k is 50,000, final is 450,000` | discount: 50,000 / final: 450,000 | expected -4500000 to deeply equal 50000 | **BUG-M4-04** (Logic toán giảm giá %) |
| **#16** | TC-FR09-13: C3 - EXACT Minimum Amount (300,000 == 300,000) (BUG CHECK) | `[BUG-M4-03] Spec requires >= min_order_amount, expect 200 OK` | HTTP 200 OK (tại mốc đúng 300.000đ) | HTTP 400 Bad Request | **BUG-M4-03** (Biên so sánh ngặt >) |
| **#17** | TC-FR09-20: C4 - Missing Authentication Token (BUG CHECK) | `[BUG-M4-05] Spec C4 requires valid login token, expect 401 Unauthorized` | HTTP 401 Unauthorized | HTTP 200 OK (Khách chưa login vẫn gọi được) | **BUG-M4-05** (Thiếu Auth middleware) |
| **#18** | TC-FR09-28: Math - Percent Discount Calculation (10% of 500k = 50k) | `[BUG-M4-04] Math check` | discount: 50,000 / final: 450,000 | expected -4500000 to deeply equal 50000 | **BUG-M4-04** (Logic toán giảm giá %) |
| **#19** | TC-FR09-29: Math - Fixed Discount Calculation (50k off 500k) | `Status is 200 OK` | Theo đặc tả | expected response to have status code 200 but got 400 | Lỗi nghiệp vụ SUT |
| **#20** | TC-FR09-29: Math - Fixed Discount Calculation (50k off 500k) | `Discount is 50,000, final is 450,000` | Theo đặc tả | expected undefined to deeply equal 50000 | Lỗi nghiệp vụ SUT |
| **#21** | TC-FR19-02: SEC - Regular User GET Users (SEC-03 BAC BUG CHECK) | `[BUG-M4-06 / SEC-03] Regular user must receive 403 Forbidden` | HTTP 403 Forbidden | HTTP 200 OK (User thường gọi và xóa được Admin) | **BUG-M4-06** (SEC-03 Broken Access Control) |
| **#22** | TC-FR19-09: SEC - Regular User Deletes User 2 (SEC-03 BAC BUG CHECK) | `[BUG-M4-06 / SEC-03] Regular user cannot delete user 2, expect 403 Forbidden` | HTTP 403 Forbidden | HTTP 200 OK (User thường gọi và xóa được Admin) | **BUG-M4-06** (SEC-03 Broken Access Control) |
| **#23** | TC-FR19-10: SEC - Regular User Attempts to Delete Admin 1 (SEC-03 BAC BUG CHECK) | `[BUG-M4-06 / SEC-03] Regular user cannot delete admin 1, expect 403 Forbidden` | HTTP 403 Forbidden | HTTP 200 OK (User thường gọi và xóa được Admin) | **BUG-M4-06** (SEC-03 Broken Access Control) |
| **#24** | TC-FR19-12: FR-19 Constraint - Admin Deletes Own Account (BUG CHECK) | `[BUG-M4-07 / FR-19] System must prevent Admin from deleting own account, expect 400/403` | HTTP 400/403 (Chặn tự xóa) | HTTP 200 OK (Server xóa luôn tài khoản Admin đang login) | **BUG-M4-07** (FR-19 Admin tự xóa chính mình) |
| **#25** | TC-FR19-13: DP - Delete Non-existent User (9999) (BUG CHECK) | `[BUG-M4-08] Non-existent user deletion should return 404 Not Found` | HTTP 404 Not Found | HTTP 200 OK (Luôn báo 'User deleted') | **BUG-M4-08** (REST API Contract) |
| **#26** | TC-FR19-14: DP - User ID is Zero (0) | `ID 0 yields 400 or 404` | Theo đặc tả | expected 200 to be one of [ 400, 404 ] | Lỗi nghiệp vụ SUT |
| **#27** | TC-FR19-15: DP - User ID is Negative (-5) | `Negative ID yields 400 or 404` | Theo đặc tả | expected 200 to be one of [ 400, 404 ] | Lỗi nghiệp vụ SUT |
| **#28** | TC-FR19-16: DP - User ID is Non-numeric String ('abc') | `String ID yields 400 or 404` | Theo đặc tả | expected 200 to be one of [ 400, 404 ] | Lỗi nghiệp vụ SUT |
| **#29** | TC-FR19-17: DP - User ID has Special Characters (@!#) | `Special characters ID yields 400 or 404` | Theo đặc tả | expected 200 to be one of [ 400, 404 ] | Lỗi nghiệp vụ SUT |
| **#30** | TC-FR19-18: DP - SQL Injection in User ID Param (1 OR 1=1) | `SQLi handled safely with 400 or 404` | Theo đặc tả | expected 200 to be one of [ 400, 404 ] | Lỗi nghiệp vụ SUT |
| **#31** | TC-FR19-19: DP - Extremely Large Overflow ID | `Overflow ID yields 404 Not Found` | Theo đặc tả | expected response to have status code 404 but got 200 | Lỗi nghiệp vụ SUT |
| **#32** | TC-FR19-22: ST - Idempotency: Delete User 2 Again (Expect 404) | `[BUG-M4-08] Second deletion of already deleted user should return 404` | HTTP 404 Not Found | HTTP 200 OK (Luôn báo 'User deleted') | **BUG-M4-08** (REST API Contract) |

---

## 3. Kết Luận Đánh Giá So Với Đặc Tả

- **Tính chính xác của kịch bản:** Toàn bộ 106 test cases đã được đồng bộ 100% với các file đặc tả `test_cases_fr03.md`, `test_cases_fr09.md`, `test_cases_fr19.md`.
- **Phân tách rạch ròi:** Toàn bộ các ca FAILED ở trên đều là **Bug THẬT của SUT** được bắt chính xác bởi assertion, hoàn toàn không còn tình trạng crash do script hay fail oan do thiếu Token.