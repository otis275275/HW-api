# Báo Cáo Tổng Hợp Kiểm Thử (Test Summary & Self-Assessment)

**MSSV:** 23120228 | **Thành viên:** M4  
**Học phần:** Kiểm thử Phần mềm (HW06 – API Testing)  
**Phân hệ phụ trách:**
- Pool A (Auth): FR-03 (`POST /api/forgot-password`, `POST /api/reset-password`)
- Pool B (Cart/Order): FR-09 (`POST /api/apply-coupon`)
- Pool C (Admin): FR-19 (`GET /api/admin/users`, `DELETE /api/admin/users/:id`)

---

## 1. Bảng Tự Đánh Giá (Self-Assessment Table — Mục 15)

| STT | Tiêu chí đánh giá | Điểm tối đa | Điểm tự đánh giá | Minh chứng & Ghi chú |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **API 1 (FR-03):** Toàn bộ pipeline (Sinh test $\ge 35$ + Audit + Extend + Thực thi Postman/Newman + Báo cáo bug) | **30** | **30** | Đã sinh 36 test cases AI + Audit chi tiết + Mở rộng 5 test cases + Báo cáo BUG-M4-01, BUG-M4-02. |
| **2** | **API 2 (FR-09):** Toàn bộ pipeline (cùng tiêu chí) | **30** | **30** | Đã sinh 35 test cases AI + Audit chi tiết + Mở rộng 5 test cases + Báo cáo BUG-M4-03 (biên >), BUG-M4-04 (công thức âm), BUG-M4-05. |
| **3** | **API 3 (FR-19):** Toàn bộ pipeline (cùng tiêu chí) | **30** | **30** | Đã sinh 35 test cases AI + Audit chi tiết + Mở rộng 5 test cases + Báo cáo BUG-M4-06 (SEC-03 BAC), BUG-M4-07 (tự xóa), BUG-M4-08. |
| **4** | **Agent Skills (AI-Driven Test Generator):** Thiết kế bộ sinh test tự động (Cấp độ G9.5 Create) | **10** | **10** | Đầy đủ sơ đồ kiến trúc Mermaid tự vẽ, thuật toán mã giả chi tiết, script `generator.py` tiêm header `X-Student-Id: 23120228` tự động. |
| **TỔNG** | **Tổng điểm đồ án HW06** | **100** | **100** | Tên file nộp: `23120228_HW06_AI_API_100.zip` |

---

## 2. Thống Kê Tổng Lượng Test Cases (Test Metrics)

| Phân hệ API | Số test AI sinh | Số test Audit | Số test Mở rộng (+5) | Tổng số Test Cases | Số Bug phát hiện |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pool A (FR-03: Forgot/Reset Password)** | 36 | 36 | 5 | **41** | 2 |
| **Pool B (FR-09: Apply Coupon)** | 35 | 35 | 5 | **40** | 3 |
| **Pool C (FR-19: Admin Users)** | 35 | 35 | 5 | **40** | 3 |
| **TỔNG CỘNG** | **106** | **106** | **15** | **121** | **8** |

---

## 3. Danh Sách Các Tính Năng Postman Đã Áp Dụng (Postman Features Checklist)

Theo yêu cầu Mục 6 của đề bài, toàn bộ bộ test suite của M4 sử dụng triệt để các tính năng nâng cao của Postman:
1. **Workspaces:** Tạo workspace riêng biệt cho đồ án EShop API Testing.
2. **Collections & Folders:** Tổ chức phân cấp rõ ràng theo 3 phân hệ (FR-03, FR-09, FR-19) kèm thư mục `0. Setup & Auth`.
3. **Variables:** Sử dụng biến ở nhiều tầng:
   - *Collection Variables:* `baseUrl`, `studentId`.
   - *Environment Variables:* `adminToken`, `userToken`, `generatedResetToken`, `testUserId`, `adminUserId`.
4. **Environments:** File môi trường [eshop_environment.json](file:///d:/ALL_SOURCE_CODE/Learning/Testing/HW-api/eshop-sut/postman/eshop_environment.json) chuẩn.
5. **Pre-request Scripts:**
   - Tự động tiêm header bắt buộc `X-Student-Id: 23120228` cho mọi request để vượt qua kiểm tra chống gian lận.
   - In thông tin header ra Console để lấy minh chứng screenshot.
6. **Tests Scripts & Assertions:**
   - Sử dụng thư viện Chai.js (`pm.test`, `pm.response.to.have.status`, `pm.expect`).
   - Kiểm định cấu trúc schema JSON (`tv4` / `Ajv`).
7. **Collection Runner & Newman CLI:** Chạy tự động toàn bộ 121 test cases bằng lệnh CLI và xuất báo cáo HTML trực quan (`htmlextra`).
