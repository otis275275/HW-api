---
name: api-test-generator
description: >-
  AI-driven API test generator and end-to-end testing pipeline for EShop (HW06 API Testing) - Customized for Member M4.
  Specialized for Pool A (FR-03: Forgot/Reset Password), Pool B (FR-09: Apply Coupon), and Pool C (FR-19: Admin Users).
---

# API Test Generator Skill — Member M4 Specialization

This skill is tailored exclusively for **Member M4** in the HW06 API Testing assignment for the EShop SUT. It automates and structures the entire testing lifecycle across the 3 designated API sets to achieve Bloom-AI Level G9.2–G9.5.

---

## 1. Designated Scope for Member M4

| Pool | Feature ID | Target Endpoints | Focus Areas & Known SUT Flaws |
| :--- | :--- | :--- | :--- |
| **Pool A** (Auth) | **FR-03** | `POST /api/forgot-password`<br>`POST /api/reset-password` | • **OTP Entropy:** Sinh mã 4 số thay vì tối thiểu 6 số (SEC-07, FR-03).<br>• **Password Storage:** Lưu plaintext không hash (SEC-01).<br>• **Validation:** Thiếu kiểm tra độ phức tạp mật khẩu mới, không có rate-limiting/brute-force OTP. |
| **Pool B** (Cart/Order) | **FR-09** | `POST /api/apply-coupon` | • **5 Điều kiện (C1–C5):** Mã tồn tại, còn hạn, ngưỡng tối thiểu, đăng nhập, số lần dùng.<br>• **Boundary Bug:** `>` thay vì `>=` tại ngưỡng đơn hàng.<br>• **Math Bug:** `1 - discount_value` gây ra số âm.<br>• **Auth Bug:** Thiếu middleware xác thực JWT (C4). |
| **Pool C** (Admin) | **FR-19** | `GET /api/admin/users`<br>`DELETE /api/admin/users/:id` | • **Broken Access Control (SEC-03):** Middleware chỉ verify JWT, KHÔNG kiểm tra `role === 'admin'`. User thường có thể xem và xóa user khác!<br>• **Self-Deletion Guard:** Admin tự xóa chính mình (vi phạm ràng buộc FR-19).<br>• **Data Exposure:** Trả về thông tin nhạy cảm. |

---

## 2. Test Generation Strategy for Member M4 (Target: >= 35 Tests / API)

### 2.1. API 1 (Pool A): FR-03 — Forgot & Reset Password
Target: `POST /api/forgot-password` & `POST /api/reset-password`
1. **Domain Partitioning & Boundary Value Analysis (BVA):**
   - Email format: valid email, empty string, malformed email (`plainaddress`, `@missinguser.com`), non-existent email, SQL injection string (`' OR '1'='1`).
   - OTP / Reset Token: valid token, invalid token, empty token, wrong length (4-digit vs 6-digit), expired token, reused token.
   - New Password complexity: valid strong password, < 8 chars, missing uppercase, missing lowercase, missing digit, missing special char, empty password.
2. **State Transition Testing:**
   - Request OTP -> Reset password successfully -> Login with new password (Success).
   - Request OTP -> Reset password -> Attempt to reset again with same token (Fail - Token invalidation).
   - Request OTP for User A -> Attempt to use Token to reset User B's password (Fail - Cross-user token attack).
3. **Security Testing (SEC-01, SEC-07):**
   - SEC-07: Verify OTP length has $\ge 6$ digits and sufficient entropy.
   - Brute-force OTP resistance (rate limiting).
   - SEC-01: Verify password is not logged or leaked in response.
4. **Schema Validation:**
   - Validate response schema for success (200 OK) and errors (400, 404, 500).

### 2.2. API 2 (Pool B): FR-09 — Apply Coupon
Target: `POST /api/apply-coupon`
1. **Domain Partitioning & BVA (The 5 Conditions C1-C5):**
   - **C1 (Code Existence & Active):** Active code (`SAVE10`), inactive/deleted code, non-existent code, empty code, SQLi in code.
   - **C2 (Expiry Date):** Valid unexpired code, expired code (`EXPIRED`), boundary of expiration date.
   - **C3 (Min Order Amount Boundary):**
     - $total < min\_order\_amount$ (Fail: 400).
     - $total == min\_order\_amount$ (**CRITICAL BOUNDARY TEST** - Catches the strict `>` bug).
     - $total > min\_order\_amount$ (Success: 200).
     - Extreme amounts: 0, negative amounts, float numbers.
   - **C4 (Authentication):** Request without token, invalid token, regular user token, admin token.
   - **C5 (Usage Limit):** First usage (usage = 0), repeat usage until `max_uses_per_user` is reached, exceeding limit.
2. **State Transitions:**
   - Coupon state progression: Unused -> Applied & Checked out -> Re-applied (limit reached).
3. **Security & Calculation Integrity:**
   - Verify calculation logic for `percent` vs `fixed` types (detect negative final amount bug).
   - Tampering `user_id` to bypass usage count limits.
4. **Schema Validation:**
   - Response contract: `success` (boolean), `coupon_id` (integer), `discount_amount` (number), `final_amount` (number), `message` (string).

### 2.3. API 3 (Pool C): FR-19 — Admin User Management
Target: `GET /api/admin/users` & `DELETE /api/admin/users/:id`
1. **Domain Partitioning & BVA:**
   - User ID param: valid user ID, non-existent ID, negative ID, ID = 0, string/special chars in ID, SQL injection in path param.
2. **Access Control & Security (SEC-02, SEC-03, SEC-06):**
   - Anonymous access (No Bearer token) -> Expected: 401 Unauthorized.
   - Regular User access (`role = 'user'`) -> Expected: 403 Forbidden (**CRITICAL TEST** - Catches SEC-03 missing role check).
   - Admin access (`role = 'admin'`) -> Expected: 200 OK.
   - Self-deletion attempt (Admin deletes own ID from token) -> Expected: 400/403 (**CRITICAL TEST** - Catches FR-19 self-deletion bug).
   - Data exposure: Verify `password` field is NOT returned in `GET /api/admin/users`.
3. **State Transitions:**
   - Active user -> Deleted via admin -> Verify user no longer returned in `GET /api/admin/users` -> Attempt to login with deleted user (Expected 401).
   - User deleted -> Re-attempt deletion on same ID (Idempotency / 404 test).
4. **Schema Validation:**
   - Array of user objects: `id` (integer), `name` (string), `email` (string), `role` (string), `shipping_address`, without password hash or plaintext.

---

## 3. Postman + Newman Execution Guide for M4

### Mandatory Headers & Pre-request Script
Every single request in the M4 Postman Collection must carry the header:
```http
X-Student-Id: {{studentId}}
```
Set at collection root level:
```javascript
const studentId = pm.environment.get("studentId") || "M4_STUDENT_ID";
pm.request.headers.upsert({
    key: "X-Student-Id",
    value: studentId
});
console.log("Pre-request: X-Student-Id injected:", studentId);
```

### Newman Run Command
```powershell
newman run postman/m4_eshop_collection.json `
  -e postman/eshop_environment.json `
  -r cli,htmlextra `
  --reporter-htmlextra-export report/m4_newman_report.html
```

---

## 4. Deliverables Checklist for Member M4
- [ ] $\ge 35$ Test cases for API 1: FR-03 (Forgot/Reset Password)
- [ ] $\ge 35$ Test cases for API 2: FR-09 (Apply Coupon)
- [ ] $\ge 35$ Test cases for API 3: FR-19 (Admin Users)
- [ ] Human audit table (VALID / INVALID / INCOMPLETE with justification)
- [ ] $\ge 5$ Extended test cases per API with analytical explanation of AI blind spots
- [ ] Exported Postman Collection JSON & Environment JSON
- [ ] Newman HTML execution report with hostname `localhost:3000` & `X-Student-Id`
- [ ] Bug reports for all genuine bugs found in M4's APIs (with GitHub Issues screenshots)
- [ ] AI Critique paragraph (200-300 words)
- [ ] Complete log in `report/ai_audit.md`
