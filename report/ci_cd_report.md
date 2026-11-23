# Báo Cáo Tích Hợp CI/CD (CI/CD Pipeline Report) — Phân Hệ M4

**MSSV:** 23120228 | **Thành viên:** M4  
**Repository:** https://github.com/otis275275/HW-api  
**CI/CD Engine:** GitHub Actions  
**Workflow File:** `.github/workflows/api-tests.yml` (hoặc `ci-cd/api-tests.yml`)

---

## 1. Cấu Hình Pipeline Tự Động Hóa (Pipeline Configuration)

Quy trình CI/CD được thiết lập theo chuẩn công nghiệp trên runner Ubuntu-latest, kích hoạt tự động mỗi khi có sự kiện `push` hoặc `pull_request` vào nhánh `main`:

```yaml
name: EShop API Automated Testing CI/CD

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  api-tests:
    name: Run Newman API Tests (Member M4 - 23120228)
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Node.js 20.x
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Backend Dependencies
        run: |
          cd backend
          npm rebuild sqlite3 || (rm -rf node_modules && npm install)

      - name: Install Global Newman and HTMLExtra Reporter
        run: npm install -g newman newman-reporter-htmlextra

      - name: Initialize & Seed SQLite Database
        run: node backend/database.js

      - name: Start Backend Server in Background
        run: |
          nohup node backend/server.js > server.log 2>&1 &
          sleep 3
          curl -I http://localhost:3000/api/products || exit 1

      - name: Run Newman Test Suite (Pool A, Pool B, Pool C)
        run: |
          mkdir -p report
          newman run postman/m4_eshop_collection.json \
            --environment postman/eshop_environment.json \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export report/newman_report.html

      - name: Upload Test Report Artifact
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: newman-api-test-report
          path: report/newman_report.html
```

---

## 2. Báo Cáo Hai Lần Chạy Mẫu (Two Sample Pipeline Runs)

Theo yêu cầu tại Mục 6 và Mục 14 của đề bài, hệ thống cung cấp 2 kịch bản commit tương ứng với 2 trạng thái kiểm thử:

### Lần Chạy 1: Toàn bộ Test Cases Đều Vượt Qua (All API Test Cases Passing)
* **Kịch bản:** Sử dụng bộ kiểm thử hợp chuẩn [postman/m4_passing_collection.json](file:///d:/ALL_SOURCE_CODE/Learning/Testing/HW-api/eshop-sut/postman/m4_passing_collection.json) bao gồm các API cốt lõi hoạt động đúng đặc tả (Admin Login, User Login, Forgot password hợp lệ, Áp dụng coupon cố định BIGBUY, Admin lấy danh sách user).
* **Kết quả thực thi trên Newman:**
  - **Executed Requests:** 5 / 5
  - **Assertions Passed:** 5 / 5 (100%)
  - **Assertions Failed:** 0
  - **Exit Code:** `0` (Success — Trạng thái GitHub Actions: **Green Checkmark ✅**)
* **Ý nghĩa:** Chứng minh quy trình CI/CD hoạt động ổn định, server khởi động thành công, cơ sở dữ liệu được nạp hạt giống (seed) chuẩn xác và hệ thống API sẵn sàng triển khai.

---

### Lần Chạy 2: Phát Hiện Lỗi Phần Mềm — Pipeline Báo Đỏ (One Failing Test Case)
* **Kịch bản:** Kích hoạt bộ kiểm thử phát hiện lỗi hồi quy (Regression Defect), cụ thể là kiểm tra mã giảm giá phần trăm `SAVE10` trên đơn hàng 500.000 ₫.
* **Chi tiết lỗi bắt được:**
  - Assertion vi phạm: `pm.expect(json.discount_amount).to.eql(50000)`
  - Giá trị thực tế server trả về: `discount_amount: -4500000` (Âm 4,5 triệu do lỗi công thức `1 - discount_value` — **BUG-M4-04**).
* **Kết quả thực thi trên Newman:**
  - **Assertions Failed:** 1
  - **Exit Code:** `1` (Non-zero exit code — Trạng thái GitHub Actions: **Red Cross ❌**)
* **Ý nghĩa:** Chứng minh bộ kiểm thử tự động trong CI/CD có khả năng chặn đứng lỗi nghiêm trọng (Quality Gate), ngăn không cho mã nguồn lỗi được merge hoặc deploy lên môi trường Production.

---

## 3. Lưu Ý Triển Khai Trên GitHub Token
Do cơ chế bảo mật của GitHub Push Protection đối với Personal Access Token (PAT), để GitHub nhận diện và tự động chạy workflow trong tab **Actions**:
1. Đảm bảo file cấu hình nằm tại đường dẫn `.github/workflows/api-tests.yml`.
2. Token cá nhân cần được tích chọn scope **`workflow`** trong [GitHub Token Settings](https://github.com/settings/tokens) khi đẩy qua Git CLI, hoặc tạo tệp trực tiếp qua giao diện GitHub Web.
