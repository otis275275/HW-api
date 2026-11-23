"""
Full Postman Collection Generator implementing ALL 106 test cases + setup requests
for Member M4 (HW06 EShop API Testing).
- 36 Test cases for Pool A (FR-03)
- 35 Test cases for Pool B (FR-09)
- 35 Test cases for Pool C (FR-19)
- 2 Setup requests (Admin & User login)
All assertions use IIFE scoped variables to prevent Newman sandbox collision.
"""

import json
import os

def build_full_suite(student_id="23120228", base_url="http://localhost:3000"):
    collection = {
        "info": {
            "name": f"HW06_M4_EShop_Automated_Suite_{student_id}",
            "_postman_id": f"hw06-m4-{student_id}-complete",
            "description": "Complete 106 Test Case Suite for Member M4 (FR-03, FR-09, FR-19).",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "// Global Pre-request: Inforce X-Student-Id",
                        f"const studentId = pm.environment.get('studentId') || '{student_id}';",
                        "pm.request.headers.upsert({ key: 'X-Student-Id', value: studentId });"
                    ]
                }
            }
        ],
        "variable": [
            {"key": "baseUrl", "value": base_url, "type": "string"},
            {"key": "studentId", "value": student_id, "type": "string"},
            {"key": "adminToken", "value": "", "type": "string"},
            {"key": "userToken", "value": "", "type": "string"},
            {"key": "activeResetToken", "value": "", "type": "string"},
            {"key": "freshResetToken", "value": "", "type": "string"},
            {"key": "adminUserId", "value": "1", "type": "string"},
            {"key": "testUserId", "value": "2", "type": "string"}
        ],
        "item": []
    }

    def req(name, method, url_path, headers=None, body=None, tests=None, prerequest=None):
        hdr = [{"key": "Content-Type", "value": "application/json"}]
        if headers:
            for k, v in headers.items():
                hdr.append({"key": k, "value": v})
        item = {
            "name": name,
            "request": {
                "method": method,
                "header": hdr,
                "url": {
                    "raw": "{{baseUrl}}" + url_path,
                    "host": ["{{baseUrl}}"],
                    "path": [p for p in url_path.split("/") if p]
                }
            }
        }
        if body is not None:
            item["request"]["body"] = {
                "mode": "raw",
                "raw": json.dumps(body) if isinstance(body, (dict, list)) else str(body)
            }
        events = []
        if prerequest:
            events.append({"listen": "prerequest", "script": {"type": "text/javascript", "exec": prerequest}})
        if tests:
            # Wrap all test code inside an IIFE to eliminate variable collision in Newman sandbox
            wrapped = ["(function() {"] + [f"    {line}" for line in tests] + ["})();"]
            events.append({"listen": "test", "script": {"type": "text/javascript", "exec": wrapped}})
        if events:
            item["event"] = events
        return item

    # ==============================================================
    # 0. SETUP & AUTH FOLDER (2 Requests)
    # ==============================================================
    setup_items = [
        req(
            "0.1 Setup - Login Admin (Acquire Admin JWT)",
            "POST",
            "/api/login",
            body={"email": "admin@eshop.com", "password": "Admin123!"},
            tests=[
                "pm.test('0.1 Admin Login returns 200 OK', () => pm.response.to.have.status(200));",
                "const json = pm.response.json();",
                "pm.environment.set('adminToken', json.token);",
                "pm.environment.set('adminUserId', json.user.id.toString());"
            ]
        ),
        req(
            "0.2 Setup - Login Regular User (Acquire User JWT)",
            "POST",
            "/api/login",
            body={"email": "test@eshop.com", "password": "Test1234!"},
            tests=[
                "pm.test('0.2 User Login returns 200 OK', () => pm.response.to.have.status(200));",
                "const json = pm.response.json();",
                "pm.environment.set('userToken', json.token);",
                "pm.environment.set('testUserId', json.user.id.toString());"
            ]
        )
    ]
    collection["item"].append({"name": "0. Setup & Auth", "item": setup_items})

    # ==============================================================
    # 1. POOL A (FR-03: FORGOT & RESET PASSWORD - 36 TEST CASES)
    # ==============================================================
    pool_a = []
    
    # TC-FR03-01 to TC-FR03-11: Domain Partitioning on Email in /api/forgot-password
    pool_a.append(req(
        "TC-FR03-01: DP - Valid Registered Email",
        "POST", "/api/forgot-password", body={"email": "test@eshop.com"},
        tests=[
            "pm.test('Status is 200 OK', () => pm.response.to.have.status(200));",
            "const json = pm.response.json();",
            "pm.test('Has resetToken', () => pm.expect(json).to.have.property('resetToken'));",
            "pm.environment.set('activeResetToken', json.resetToken);"
        ]
    ))
    pool_a.append(req(
        "TC-FR03-02: DP - Non-existent Registered Email",
        "POST", "/api/forgot-password", body={"email": "notfound@domain.com"},
        tests=["pm.test('Status is 404 Not Found', () => pm.response.to.have.status(404));"]
    ))
    pool_a.append(req(
        "TC-FR03-03: DP - Empty Email String",
        "POST", "/api/forgot-password", body={"email": ""},
        tests=["pm.test('Spec expects 400 Bad Request for empty email', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-04: DP - Missing Email Field",
        "POST", "/api/forgot-password", body={},
        tests=["pm.test('Missing email field yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-05: DP - Email Missing @ Symbol",
        "POST", "/api/forgot-password", body={"email": "testeshop.com"},
        tests=["pm.test('Malformed email yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-06: DP - Email Missing Domain",
        "POST", "/api/forgot-password", body={"email": "test@"},
        tests=["pm.test('Malformed email yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-07: DP - Email with Extra Whitespace",
        "POST", "/api/forgot-password", body={"email": "  test@eshop.com  "},
        tests=["pm.test('Trimmed email accepted 200 or 400 rejected', () => pm.expect(pm.response.code).to.be.oneOf([200, 400]));"]
    ))
    pool_a.append(req(
        "TC-FR03-08: DP - Email Exceeding Max Length (>255 chars)",
        "POST", "/api/forgot-password", body={"email": "a"*250 + "@eshop.com"},
        tests=["pm.test('Overly long email yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-09: DP - SQL Injection in Email Field",
        "POST", "/api/forgot-password", body={"email": "' OR '1'='1"},
        tests=["pm.test('SQL injection handled safely with 400/404 (Not 500)', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_a.append(req(
        "TC-FR03-10: DP - XSS Script in Email Field",
        "POST", "/api/forgot-password", body={"email": "<script>alert(1)</script>@domain.com"},
        tests=["pm.test('XSS email rejected with 400/404', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_a.append(req(
        "TC-FR03-11: DP - Email Uppercase Format",
        "POST", "/api/forgot-password", body={"email": "TEST@ESHOP.COM"},
        tests=["pm.test('Case-insensitive email yields 200 OK or 404', () => pm.expect(pm.response.code).to.be.oneOf([200, 404]));"]
    ))

    # TC-FR03-12 to TC-FR03-19: DP on resetToken in /api/reset-password
    pool_a.append(req(
        "TC-FR03-12: DP - Reset Password with Valid Token & Password",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "{{activeResetToken}}", "newPassword": "NewPassword123!"},
        tests=[
            "pm.test('Reset password succeeds with 200 OK', () => pm.response.to.have.status(200));",
            "pm.test('Response message matches', () => pm.expect(pm.response.json().message).to.include('successfully'));"
        ]
    ))
    pool_a.append(req(
        "TC-FR03-13: DP - Invalid ResetToken (000000)",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "000000", "newPassword": "NewPassword123!"},
        tests=["pm.test('Invalid token yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-14: DP - Empty ResetToken",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "", "newPassword": "NewPassword123!"},
        tests=["pm.test('Empty token yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-15: DP - Missing ResetToken Field",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "newPassword": "NewPassword123!"},
        tests=["pm.test('Missing token yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-16: DP - Non-numeric String Token (ABCDEF)",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "ABCDEF", "newPassword": "NewPassword123!"},
        tests=["pm.test('Non-numeric token yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-17: DP - Short Token (<4 digits)",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "12", "newPassword": "NewPassword123!"},
        tests=["pm.test('Short token yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-18: DP - Long Token (>6 digits)",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "12345678", "newPassword": "NewPassword123!"},
        tests=["pm.test('Long token yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-19: DP - SQL Injection in ResetToken Field",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "' OR 1=1 --", "newPassword": "NewPassword123!"},
        tests=["pm.test('SQLi in token rejected with 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))

    # Helper request to acquire a fresh token for weak password tests:
    pool_a.append(req(
        "Helper: Acquire Fresh Token for Password Complexity Tests",
        "POST", "/api/forgot-password", body={"email": "test@eshop.com"},
        tests=[
            "pm.test('Helper forgot-password 200 OK', () => pm.response.to.have.status(200));",
            "pm.environment.set('freshResetToken', pm.response.json().resetToken);"
        ]
    ))

    # TC-FR03-20 to TC-FR03-27: Password Complexity Tests
    pool_a.append(req(
        "TC-FR03-20: DP - Valid Strong Password (SecurePass123!)",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": "SecurePass123!"},
        tests=["pm.test('Valid strong password accepted 200 OK', () => pm.response.to.have.status(200));"]
    ))

    weak_cases = [
        ("TC-FR03-21: DP - Weak Password Short (<8 chars)", "Pass1!"),
        ("TC-FR03-22: DP - Password Missing Uppercase Letter", "password123!"),
        ("TC-FR03-23: DP - Password Missing Lowercase Letter", "PASSWORD123!"),
        ("TC-FR03-24: DP - Password Missing Digit", "PasswordSpecial!"),
        ("TC-FR03-25: DP - Password Missing Special Character", "Password123"),
        ("TC-FR03-26: DP - Empty Password String", ""),
        ("TC-FR03-27: DP - Whitespace-only Password", "        ")
    ]
    for tc_id_name, weak_pwd in weak_cases:
        pool_a.append(req(
            f"{tc_id_name} (BUG CHECK: SUT lacks password validator)",
            "POST", "/api/reset-password",
            body={"email": "test@eshop.com", "resetToken": "{{freshResetToken}}", "newPassword": weak_pwd},
            prerequest=[
                "// Refresh token dynamically before sending so the test tests password validation, not token validity",
                "pm.sendRequest({",
                "    url: pm.variables.get('baseUrl') + '/api/forgot-password',",
                "    method: 'POST',",
                "    header: { 'Content-Type': 'application/json' },",
                "    body: { mode: 'raw', raw: JSON.stringify({ email: 'test@eshop.com' }) }",
                "}, function (err, res) {",
                "    if (!err && res.code === 200) {",
                "        pm.environment.set('freshResetToken', res.json().resetToken);",
                "    }",
                "});"
            ],
            tests=[
                "pm.test('[BUG-M4-02] Spec requires strong password, expect 400 Bad Request', () => {",
                "    pm.response.to.have.status(400);",
                "});"
            ]
        ))

    # State Transitions (TC-FR03-28 to TC-FR03-31)
    pool_a.append(req(
        "TC-FR03-28: ST - Complete Flow Step 1: Request OTP",
        "POST", "/api/forgot-password", body={"email": "test@eshop.com"},
        tests=[
            "pm.test('Step 1 OTP generated 200 OK', () => pm.response.to.have.status(200));",
            "pm.environment.set('stResetToken', pm.response.json().resetToken);"
        ]
    ))
    pool_a.append(req(
        "TC-FR03-28: ST - Complete Flow Step 2: Reset to 'FinalPass123!'",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "{{stResetToken}}", "newPassword": "FinalPass123!"},
        tests=["pm.test('Step 2 Reset password 200 OK', () => pm.response.to.have.status(200));"]
    ))
    pool_a.append(req(
        "TC-FR03-28: ST - Complete Flow Step 3: Login with 'FinalPass123!'",
        "POST", "/api/login",
        body={"email": "test@eshop.com", "password": "FinalPass123!"},
        tests=[
            "pm.test('Step 3 Login with new password succeeds 200 OK', () => pm.response.to.have.status(200));",
            "pm.test('Token returned', () => pm.expect(pm.response.json()).to.have.property('token'));"
        ]
    ))
    pool_a.append(req(
        "TC-FR03-29: ST - One-Time Use Guard: Reuse Same Token (Expect 400)",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "{{stResetToken}}", "newPassword": "AnotherPassword123!"},
        tests=["pm.test('Reusing spent token yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-30: ST - Login with OLD Password 'Test1234!' (Expect 401)",
        "POST", "/api/login",
        body={"email": "test@eshop.com", "password": "Test1234!"},
        tests=["pm.test('Old password is now invalid, expect 401 Unauthorized', () => pm.response.to.have.status(401));"]
    ))
    pool_a.append(req(
        "TC-FR03-31: ST - Request OTP Twice in a Row (Token 1 vs Token 2)",
        "POST", "/api/forgot-password", body={"email": "test@eshop.com"},
        tests=[
            "pm.test('Second OTP request succeeds 200 OK', () => pm.response.to.have.status(200));",
            "pm.test('New resetToken is generated', () => pm.expect(pm.response.json()).to.have.property('resetToken'));"
        ]
    ))

    # Security & Schema (TC-FR03-32 to TC-FR03-36)
    pool_a.append(req(
        "TC-FR03-32: SEC - Verify OTP Entropy >= 6 Digits (SEC-07 BUG CHECK)",
        "POST", "/api/forgot-password", body={"email": "test@eshop.com"},
        tests=[
            "pm.test('Status is 200 OK', () => pm.response.to.have.status(200));",
            "const json = pm.response.json();",
            "pm.test('[BUG-M4-01 / SEC-07] OTP must be at least 6 digits long', () => {",
            "    pm.expect(json.resetToken.length).to.be.at.least(6);",
            "});"
        ]
    ))
    pool_a.append(req(
        "TC-FR03-33: SEC - Cross-Account Token Replay Attack",
        "POST", "/api/reset-password",
        body={"email": "admin@eshop.com", "resetToken": "{{activeResetToken}}", "newPassword": "HackedAdmin123!"},
        tests=["pm.test('Cross-account reset rejected with 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_a.append(req(
        "TC-FR03-34: SEC - Response Does Not Leak Plaintext Password (SEC-01)",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "000000", "newPassword": "SecretPassword123!"},
        tests=["pm.test('Password not leaked in response body', () => pm.expect(pm.response.text()).to.not.include('SecretPassword123!'));"]
    ))
    pool_a.append(req(
        "TC-FR03-35: Schema - Forgot Password JSON Schema Contract",
        "POST", "/api/forgot-password", body={"email": "test@eshop.com"},
        tests=[
            "pm.test('Forgot-password matches contract', () => {",
            "    const json = pm.response.json();",
            "    pm.expect(json).to.have.property('message').that.is.a('string');",
            "    pm.expect(json).to.have.property('resetToken').that.is.a('string');",
            "});"
        ]
    ))
    pool_a.append(req(
        "TC-FR03-36: Schema - Reset Password JSON Schema Contract",
        "POST", "/api/reset-password",
        body={"email": "test@eshop.com", "resetToken": "000000", "newPassword": "Password123!"},
        tests=[
            "pm.test('Error response matches contract', () => {",
            "    pm.expect(pm.response.json()).to.have.property('error').that.is.a('string');",
            "});"
        ]
    ))
    collection["item"].append({"name": "1. Pool A (FR-03: Forgot & Reset Password)", "item": pool_a})

    # ==============================================================
    # 2. POOL B (FR-09: APPLY COUPON - 35 TEST CASES)
    # ==============================================================
    pool_b = []
    
    # C1 (Code existence & Active)
    pool_b.append(req(
        "TC-FR09-01: C1 - Valid Percent Coupon (SAVE10 - 10%) (BUG CHECK)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 500000, "user_id": 2},
        tests=[
            "pm.test('Status is 200 OK', () => pm.response.to.have.status(200));",
            "const json = pm.response.json();",
            "pm.test('[BUG-M4-04] Math check: 10% of 500k is 50,000, final is 450,000', () => {",
            "    pm.expect(json.discount_amount).to.eql(50000);",
            "    pm.expect(json.final_amount).to.eql(450000);",
            "});"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-02: C1 - Valid Fixed Coupon (BIGBUY - 50k)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "BIGBUY", "total_amount": 600000, "user_id": 2},
        tests=[
            "pm.test('Status is 200 OK', () => pm.response.to.have.status(200));",
            "const json = pm.response.json();",
            "pm.test('Fixed discount is 50,000, final is 550,000', () => {",
            "    pm.expect(json.discount_amount).to.eql(50000);",
            "    pm.expect(json.final_amount).to.eql(550000);",
            "});"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-03: C1 - Non-existent Coupon Code (UNKNOWN99)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "UNKNOWN99", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('Non-existent coupon yields 404 Not Found', () => pm.response.to.have.status(404));"]
    ))
    pool_b.append(req(
        "TC-FR09-04: C1 - Inactive Coupon Code (is_active = 0)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "INACTIVE10", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('Inactive coupon yields 404 Not Found', () => pm.response.to.have.status(404));"]
    ))
    pool_b.append(req(
        "TC-FR09-05: C1 - Empty Coupon Code String",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('Empty code yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-06: C1 - Missing Code Field",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"total_amount": 500000, "user_id": 2},
        tests=["pm.test('Missing code yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-07: C1 - SQL Injection in Coupon Code",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "' OR '1'='1", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('SQLi handled safely with 404 Not Found (Not 500)', () => pm.response.to.have.status(404));"]
    ))
    pool_b.append(req(
        "TC-FR09-08: C1 - Lowercase Coupon Code (save10)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "save10", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('Case sensitivity check: 200 OK or 404', () => pm.expect(pm.response.code).to.be.oneOf([200, 404]));"]
    ))

    # C2 (Expiry Date)
    pool_b.append(req(
        "TC-FR09-09: C2 - Expired Coupon (EXPIRED - total 200,000)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "EXPIRED", "total_amount": 200000, "user_id": 2},
        tests=[
            "pm.test('Expired coupon yields 400 Bad Request', () => pm.response.to.have.status(400));",
            "pm.test('Error specifies expired', () => pm.expect(pm.response.json().error).to.include('hết hạn'));"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-10: C2 - Just Expired Boundary Coupon",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "JUST_EXPIRED", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('Expired boundary yields 400 or 404', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_b.append(req(
        "TC-FR09-11: C2 - Long Validity Coupon (2099-12-31)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 400000, "user_id": 2},
        tests=["pm.test('Valid unexpired coupon yields 200 OK', () => pm.response.to.have.status(200));"]
    ))

    # C3 (Min Order Amount Boundary)
    pool_b.append(req(
        "TC-FR09-12: C3 - Below Minimum Amount (299,999 < 300,000)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 299999, "user_id": 2},
        tests=["pm.test('Below min amount yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-13: C3 - EXACT Minimum Amount (300,000 == 300,000) (BUG CHECK)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 300000, "user_id": 2},
        tests=[
            "pm.test('[BUG-M4-03] Spec requires >= min_order_amount, expect 200 OK', () => {",
            "    pm.response.to.have.status(200);",
            "});"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-14: C3 - Above Minimum Amount (300,001 > 300,000)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 300001, "user_id": 2},
        tests=["pm.test('Above min amount yields 200 OK', () => pm.response.to.have.status(200));"]
    ))
    pool_b.append(req(
        "TC-FR09-15: C3 - Order Amount is Zero (0)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 0, "user_id": 2},
        tests=["pm.test('Zero order amount yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-16: C3 - Order Amount is Negative (-100,000)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": -100000, "user_id": 2},
        tests=["pm.test('Negative total yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-17: C3 - Missing total_amount Field",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "user_id": 2},
        tests=["pm.test('Missing total_amount yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-18: C3 - total_amount is String ('abc')",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": "abc", "user_id": 2},
        tests=["pm.test('String amount yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-19: C3 - total_amount is Float (350,000.5)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 350000.5, "user_id": 2},
        tests=["pm.test('Float amount yields 200 OK', () => pm.response.to.have.status(200));"]
    ))

    # C4 (Authentication & User ID)
    pool_b.append(req(
        "TC-FR09-20: C4 - Missing Authentication Token (BUG CHECK)",
        "POST", "/api/apply-coupon",
        body={"code": "SAVE10", "total_amount": 500000},
        tests=[
            "pm.test('[BUG-M4-05] Spec C4 requires valid login token, expect 401 Unauthorized', () => {",
            "    pm.response.to.have.status(401);",
            "});"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-21: C4 - Invalid / Expired Bearer Token",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer invalid_token_xyz"},
        body={"code": "SAVE10", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('Invalid token yields 401/403 or 200 (if unauthenticated)', () => pm.expect(pm.response.code).to.be.oneOf([200, 401, 403]));"]
    ))
    pool_b.append(req(
        "TC-FR09-22: C4 - Tampering user_id Mismatch",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 500000, "user_id": 999},
        tests=["pm.test('IDOR user tampering check', () => pm.expect(pm.response.code).to.be.oneOf([200, 403]));"]
    ))

    # C5 (Usage Limits)
    pool_b.append(req(
        "TC-FR09-23: C5 - First Usage (usage_count = 0)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 500000, "user_id": 2},
        tests=["pm.test('First usage yields 200 OK', () => pm.response.to.have.status(200));"]
    ))
    pool_b.append(req(
        "TC-FR09-24: C5 - Exceed Usage Limit for max_uses = 1 (BUG CHECK)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 500000, "user_id": 2},
        prerequest=[
            "// Record 1st usage into coupon_usage",
            "pm.sendRequest({",
            "    url: pm.variables.get('baseUrl') + '/api/coupon-usage',",
            "    method: 'POST',",
            "    header: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + pm.environment.get('userToken') },",
            "    body: { mode: 'raw', raw: JSON.stringify({ coupon_id: 1 }) }",
            "}, function (err, res) {});"
        ],
        tests=[
            "pm.test('Exceeded limit yields 400 Bad Request', () => pm.response.to.have.status(400));",
            "pm.test('Error indicates limit reached', () => pm.expect(pm.response.json().error).to.include('giới hạn'));"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-25: C5 - VIP100 Usage 1 of 2",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "VIP100", "total_amount": 400000, "user_id": 2},
        tests=["pm.test('VIP100 usage 1 yields 200 OK', () => pm.response.to.have.status(200));"]
    ))
    pool_b.append(req(
        "TC-FR09-26: C5 - VIP100 Usage 2 of 2",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "VIP100", "total_amount": 400000, "user_id": 2},
        prerequest=[
            "pm.sendRequest({",
            "    url: pm.variables.get('baseUrl') + '/api/coupon-usage',",
            "    method: 'POST',",
            "    header: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + pm.environment.get('userToken') },",
            "    body: { mode: 'raw', raw: JSON.stringify({ coupon_id: 3 }) }",
            "}, function (err, res) {});"
        ],
        tests=["pm.test('VIP100 usage 2 yields 200 OK', () => pm.response.to.have.status(200));"]
    ))
    pool_b.append(req(
        "TC-FR09-27: C5 - VIP100 Usage 3 of 2 (Exceeded)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "VIP100", "total_amount": 400000, "user_id": 2},
        prerequest=[
            "pm.sendRequest({",
            "    url: pm.variables.get('baseUrl') + '/api/coupon-usage',",
            "    method: 'POST',",
            "    header: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + pm.environment.get('userToken') },",
            "    body: { mode: 'raw', raw: JSON.stringify({ coupon_id: 3 }) }",
            "}, function (err, res) {});"
        ],
        tests=["pm.test('VIP100 usage 3 yields 400 Bad Request', () => pm.response.to.have.status(400));"]
    ))

    # Math & State
    pool_b.append(req(
        "TC-FR09-28: Math - Percent Discount Calculation (10% of 500k = 50k)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "SAVE10", "total_amount": 500000, "user_id": 1},
        tests=[
            "pm.test('Status is 200 OK', () => pm.response.to.have.status(200));",
            "const json = pm.response.json();",
            "pm.test('[BUG-M4-04] Math check', () => {",
            "    pm.expect(json.discount_amount).to.eql(50000);",
            "    pm.expect(json.final_amount).to.eql(450000);",
            "});"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-29: Math - Fixed Discount Calculation (50k off 500k)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "BIGBUY", "total_amount": 500000, "user_id": 1},
        tests=[
            "pm.test('Status is 200 OK', () => pm.response.to.have.status(200));",
            "const json = pm.response.json();",
            "pm.test('Discount is 50,000, final is 450,000', () => {",
            "    pm.expect(json.discount_amount).to.eql(50000);",
            "    pm.expect(json.final_amount).to.eql(450000);",
            "});"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-30: Math - Fixed Discount Exceeds Order Total (40k total vs 50k discount)",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "BIGBUY", "total_amount": 40000, "user_id": 1},
        tests=["pm.test('Order below min_order_amount 500k rejected with 400', () => pm.response.to.have.status(400));"]
    ))
    pool_b.append(req(
        "TC-FR09-31: ST - User 2 Exhausted, User 1 Still Eligible",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{adminToken}}"},
        body={"code": "SAVE10", "total_amount": 500000, "user_id": 1},
        tests=["pm.test('Independent user quota yields 200 OK', () => pm.response.to.have.status(200));"]
    ))

    # Schema
    pool_b.append(req(
        "TC-FR09-32: Schema - Complete Success JSON Shape",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "BIGBUY", "total_amount": 600000, "user_id": 2},
        tests=[
            "pm.test('Has success property', () => pm.expect(pm.response.json()).to.have.property('success', true));",
            "pm.test('Has coupon_id', () => pm.expect(pm.response.json()).to.have.property('coupon_id'));",
            "pm.test('Has discount_amount', () => pm.expect(pm.response.json()).to.have.property('discount_amount'));",
            "pm.test('Has final_amount', () => pm.expect(pm.response.json()).to.have.property('final_amount'));",
            "pm.test('Has message', () => pm.expect(pm.response.json()).to.have.property('message'));"
        ]
    ))
    pool_b.append(req(
        "TC-FR09-33: Schema - final_amount Must Be Number",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "BIGBUY", "total_amount": 600000, "user_id": 2},
        tests=["pm.test('final_amount is type number', () => pm.expect(pm.response.json().final_amount).to.be.a('number'));"]
    ))
    pool_b.append(req(
        "TC-FR09-34: Schema - Error Schema when Missing Code",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"total_amount": 500000},
        tests=["pm.test('Error response has error string', () => pm.expect(pm.response.json()).to.have.property('error').that.is.a('string'));"]
    ))
    pool_b.append(req(
        "TC-FR09-35: Schema - Error Schema when Coupon Expired",
        "POST", "/api/apply-coupon",
        headers={"Authorization": "Bearer {{userToken}}"},
        body={"code": "EXPIRED", "total_amount": 500000},
        tests=["pm.test('Expired response has error string', () => pm.expect(pm.response.json()).to.have.property('error').that.is.a('string'));"]
    ))
    collection["item"].append({"name": "2. Pool B (FR-09: Apply Coupon)", "item": pool_b})

    # ==============================================================
    # 3. POOL C (FR-19: ADMIN USER MANAGEMENT - 35 TEST CASES)
    # ==============================================================
    pool_c = []
    
    # Access Control (TC-FR19-01 to TC-FR19-05)
    pool_c.append(req(
        "TC-FR19-01: SEC - Admin GET Users with Valid Admin Token",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('Admin token yields 200 OK', () => pm.response.to.have.status(200));",
            "pm.test('Response is array of users', () => pm.expect(pm.response.json()).to.be.an('array'));"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-02: SEC - Regular User GET Users (SEC-03 BAC BUG CHECK)",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{userToken}}"},
        tests=[
            "pm.test('[BUG-M4-06 / SEC-03] Regular user must receive 403 Forbidden', () => {",
            "    pm.response.to.have.status(403);",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-03: SEC - Anonymous GET Users (No Token)",
        "GET", "/api/admin/users",
        tests=["pm.test('Missing token yields 401 Unauthorized', () => pm.response.to.have.status(401));"]
    ))
    pool_c.append(req(
        "TC-FR19-04: SEC - Invalid Bearer Token GET Users",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer invalid_token_123"},
        tests=["pm.test('Invalid token yields 403 Forbidden', () => pm.response.to.have.status(403));"]
    ))
    pool_c.append(req(
        "TC-FR19-05: SEC - Expired Bearer Token GET Users",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer expired_token_abc"},
        tests=["pm.test('Expired token yields 403 Forbidden', () => pm.response.to.have.status(403));"]
    ))

    # Data Exposure (TC-FR19-06, TC-FR19-07)
    pool_c.append(req(
        "TC-FR19-06: Data Exposure - Password Not Exposed in GET Users",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('Users list does NOT contain password property', () => {",
            "    const arr = pm.response.json();",
            "    arr.forEach(u => pm.expect(u).to.not.have.property('password'));",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-07: Data Exposure - reset_token Not Exposed in GET Users",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('Users list does NOT contain reset_token property', () => {",
            "    const arr = pm.response.json();",
            "    arr.forEach(u => pm.expect(u).to.not.have.property('reset_token'));",
            "});"
        ]
    ))

    # DELETE operations (TC-FR19-08 to TC-FR19-19)
    pool_c.append(req(
        "TC-FR19-08: DP - Admin Deletes User 2 Successfully",
        "DELETE", "/api/admin/users/2",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('Admin deletes user yields 200 OK', () => pm.response.to.have.status(200));",
            "pm.test('Message confirms deleted', () => pm.expect(pm.response.json().message).to.include('deleted'));"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-09: SEC - Regular User Deletes User 2 (SEC-03 BAC BUG CHECK)",
        "DELETE", "/api/admin/users/2",
        headers={"Authorization": "Bearer {{userToken}}"},
        tests=[
            "pm.test('[BUG-M4-06 / SEC-03] Regular user cannot delete user 2, expect 403 Forbidden', () => {",
            "    pm.response.to.have.status(403);",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-10: SEC - Regular User Attempts to Delete Admin 1 (SEC-03 BAC BUG CHECK)",
        "DELETE", "/api/admin/users/1",
        headers={"Authorization": "Bearer {{userToken}}"},
        tests=[
            "pm.test('[BUG-M4-06 / SEC-03] Regular user cannot delete admin 1, expect 403 Forbidden', () => {",
            "    pm.response.to.have.status(403);",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-11: SEC - Anonymous Deletes User (No Token)",
        "DELETE", "/api/admin/users/2",
        tests=["pm.test('Missing token yields 401 Unauthorized', () => pm.response.to.have.status(401));"]
    ))
    pool_c.append(req(
        "TC-FR19-12: FR-19 Constraint - Admin Deletes Own Account (BUG CHECK)",
        "DELETE", "/api/admin/users/{{adminUserId}}",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('[BUG-M4-07 / FR-19] System must prevent Admin from deleting own account, expect 400/403', () => {",
            "    pm.expect(pm.response.code).to.be.oneOf([400, 403]);",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-13: DP - Delete Non-existent User (9999) (BUG CHECK)",
        "DELETE", "/api/admin/users/9999",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('[BUG-M4-08] Non-existent user deletion should return 404 Not Found', () => {",
            "    pm.response.to.have.status(404);",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-14: DP - User ID is Zero (0)",
        "DELETE", "/api/admin/users/0",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('ID 0 yields 400 or 404', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_c.append(req(
        "TC-FR19-15: DP - User ID is Negative (-5)",
        "DELETE", "/api/admin/users/-5",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Negative ID yields 400 or 404', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_c.append(req(
        "TC-FR19-16: DP - User ID is Non-numeric String ('abc')",
        "DELETE", "/api/admin/users/abc",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('String ID yields 400 or 404', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_c.append(req(
        "TC-FR19-17: DP - User ID has Special Characters (@!#)",
        "DELETE", "/api/admin/users/@!#",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Special characters ID yields 400 or 404', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_c.append(req(
        "TC-FR19-18: DP - SQL Injection in User ID Param (1 OR 1=1)",
        "DELETE", "/api/admin/users/1 OR 1=1",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('SQLi handled safely with 400 or 404', () => pm.expect(pm.response.code).to.be.oneOf([400, 404]));"]
    ))
    pool_c.append(req(
        "TC-FR19-19: DP - Extremely Large Overflow ID",
        "DELETE", "/api/admin/users/999999999999999",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Overflow ID yields 404 Not Found', () => pm.response.to.have.status(404));"]
    ))

    # State Transitions (TC-FR19-20 to TC-FR19-23)
    pool_c.append(req(
        "TC-FR19-20: ST - Verify Deleted User 2 Is Absent From User List",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('User 2 is not present in active user list', () => {",
            "    const users = pm.response.json();",
            "    const user2 = users.find(u => u.id === 2);",
            "    pm.expect(user2).to.be.undefined;",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-21: ST - Deleted User 2 Cannot Login",
        "POST", "/api/login",
        body={"email": "test@eshop.com", "password": "Test1234!"},
        tests=["pm.test('Deleted user login is rejected with 401 Unauthorized', () => pm.response.to.have.status(401));"]
    ))
    pool_c.append(req(
        "TC-FR19-22: ST - Idempotency: Delete User 2 Again (Expect 404)",
        "DELETE", "/api/admin/users/2",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('[BUG-M4-08] Second deletion of already deleted user should return 404', () => {",
            "    pm.response.to.have.status(404);",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-23: ST - Deleted User Token Revocation Check",
        "GET", "/api/users/me",
        headers={"Authorization": "Bearer {{userToken}}"},
        tests=["pm.test('Revoked user token yields 401/403 or null user', () => pm.expect(pm.response.code).to.be.oneOf([200, 401, 403]));"]
    ))

    # Role escalation & Schema (TC-FR19-24 to TC-FR19-35)
    pool_c.append(req(
        "TC-FR19-24: SEC - Role Escalation Forged JWT Token",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6ImFkbWluIn0.fake_signature"},
        tests=["pm.test('Forged signature rejected with 403 Forbidden', () => pm.response.to.have.status(403));"]
    ))
    pool_c.append(req(
        "TC-FR19-25: Schema - Admin Users Array Schema Validation",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Response is array', () => pm.expect(pm.response.json()).to.be.an('array'));"]
    ))
    pool_c.append(req(
        "TC-FR19-26: Schema - User Object Property Types",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=[
            "pm.test('User objects have correct types', () => {",
            "    const arr = pm.response.json();",
            "    if (arr.length > 0) {",
            "        pm.expect(arr[0].id).to.be.a('number');",
            "        pm.expect(arr[0].name).to.be.a('string');",
            "        pm.expect(arr[0].email).to.be.a('string');",
            "        pm.expect(arr[0].role).to.be.a('string');",
            "    }",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-27: Schema - DELETE User Response Schema",
        "DELETE", "/api/admin/users/999",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Response contains message property', () => pm.expect(pm.response.json()).to.have.property('message'));"]
    ))
    pool_c.append(req(
        "TC-FR19-28: DP - Delete User With Orders Check",
        "DELETE", "/api/admin/users/1",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Delete operation returns valid HTTP response', () => pm.expect(pm.response.code).to.be.oneOf([200, 400, 403]));"]
    ))
    pool_c.append(req(
        "TC-FR19-29: DP - Content-Type Header on DELETE",
        "DELETE", "/api/admin/users/999",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Content-Type is JSON', () => pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json'));"]
    ))
    pool_c.append(req(
        "TC-FR19-30: DP - Invalid Method POST on /api/admin/users",
        "POST", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        body={"name": "New Admin"},
        tests=["pm.test('Unsupported POST on /api/admin/users yields 404 or 405', () => pm.expect(pm.response.code).to.be.oneOf([404, 405]));"]
    ))
    pool_c.append(req(
        "TC-FR19-31: DP - Invalid Method POST on /api/admin/users/:id",
        "POST", "/api/admin/users/1",
        headers={"Authorization": "Bearer {{adminToken}}"},
        body={},
        tests=["pm.test('Unsupported POST on /api/admin/users/1 yields 404 or 405', () => pm.expect(pm.response.code).to.be.oneOf([404, 405]));"]
    ))
    pool_c.append(req(
        "TC-FR19-32: Schema - Error Schema for 401 Unauthorized",
        "GET", "/api/admin/users",
        tests=[
            "pm.test('401 error body matches schema', () => {",
            "    pm.response.to.have.status(401);",
            "    pm.expect(pm.response.json()).to.have.property('error', 'Unauthorized');",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-33: Schema - Error Schema for 403 Forbidden",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer invalid_token"},
        tests=[
            "pm.test('403 error body matches schema', () => {",
            "    pm.response.to.have.status(403);",
            "    pm.expect(pm.response.json()).to.have.property('error', 'Forbidden');",
            "});"
        ]
    ))
    pool_c.append(req(
        "TC-FR19-34: SEC - SQL Injection in Authorization Header",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer ' OR 1=1 --"},
        tests=["pm.test('SQLi in header rejected with 403 Forbidden', () => pm.response.to.have.status(403));"]
    ))
    pool_c.append(req(
        "TC-FR19-35: SEC - XSS Injection via User Data",
        "GET", "/api/admin/users",
        headers={"Authorization": "Bearer {{adminToken}}"},
        tests=["pm.test('Response is safe JSON', () => pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json'));"]
    ))
    collection["item"].append({"name": "3. Pool C (FR-19: Admin Users)", "item": pool_c})

    out_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "postman", "m4_eshop_collection.json")
    if not os.path.exists(os.path.dirname(out_path)):
        out_path = os.path.abspath("postman/m4_eshop_collection.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    total = len(setup_items) + len(pool_a) + len(pool_b) + len(pool_c)
    print(f"Generated 100% complete collection with {total} total requests ({len(pool_a)} in Pool A, {len(pool_b)} in Pool B, {len(pool_c)} in Pool C) at: {out_path}")

if __name__ == "__main__":
    build_full_suite()
