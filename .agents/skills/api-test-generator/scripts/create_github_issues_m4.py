import os
import json
import base64
import urllib.request
from PIL import Image, ImageDraw

TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO = 'otis275275/HW-api'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'M4-Bug-Reporter'
}

BUGS = [
    {
        "id": "BUG-M4-01",
        "title": "[BUG-M4-01][FR-03][SEC-07] POST /api/forgot-password generates 4-digit OTP instead of minimum 6 digits",
        "severity": "HIGH",
        "pool": "Pool A (FR-03)",
        "endpoint": "POST /api/forgot-password",
        "violates": "SEC-07, FR-03",
        "source_loc": "backend/server.js:72",
        "labels": ["bug", "security", "pool-a", "severity:high", "M4-23120228"],
        "curl_cmd": 'curl -X POST http://localhost:3000/api/forgot-password \\\n  -H "Content-Type: application/json" \\\n  -H "X-Student-Id: 23120228" \\\n  -d \'{"email": "test@eshop.com"}\'',
        "actual_resp": 'HTTP/1.1 200 OK\n{\n  "message": "If this email exists...",\n  "resetToken": "8040"  <-- DEFECT: Length is 4 digits only!\n}',
        "expected": "resetToken must have minimum length of 6 digits (e.g. 100000..999999) to satisfy cryptographic entropy requirements.",
        "code_snippet": "// Line 72 in backend/server.js:\nconst resetToken = Math.floor(1000 + Math.random() * 9000).toString(); // Generates 1000-9999",
        "description": "The password reset OTP generation in `server.js` generates a random number between 1000 and 9999, which is strictly 4 digits long. Security requirement SEC-07 and FR-03 explicitly state: 'Mã OTP đặt lại mật khẩu phải đủ entropy (tối thiểu 6 chữ số), có thời hạn và vô hiệu hóa sau khi dùng.' A 4-digit code is trivial to brute-force within minutes."
    },
    {
        "id": "BUG-M4-02",
        "title": "[BUG-M4-02][FR-03][SEC-01] POST /api/reset-password stores plaintext password without complexity validation",
        "severity": "CRITICAL",
        "pool": "Pool A (FR-03)",
        "endpoint": "POST /api/reset-password",
        "violates": "SEC-01, FR-01, FR-03",
        "source_loc": "backend/server.js:89-92",
        "labels": ["bug", "security", "pool-a", "severity:critical", "M4-23120228"],
        "curl_cmd": 'curl -X POST http://localhost:3000/api/reset-password \\\n  -H "Content-Type: application/json" \\\n  -H "X-Student-Id: 23120228" \\\n  -d \'{"email": "test@eshop.com", "resetToken": "8040", "newPassword": "123"}\'',
        "actual_resp": 'HTTP/1.1 200 OK\n{\n  "message": "Password reset successfully"\n}\n// SQLite DB shows: password = "123" (PLAINTEXT in database!)',
        "expected": "Reject with 400 Bad Request if password lacks complexity (<8 chars, missing uppercase/number/special char). Must hash with bcrypt before storing.",
        "code_snippet": "// Line 89-92 in backend/server.js:\ndb.run(\n  \"UPDATE users SET password = ?, reset_token = NULL WHERE email = ? AND reset_token = ?\",\n  [newPassword, email, resetToken], ...\n);",
        "description": "When resetting passwords, `POST /api/reset-password` does not perform any password complexity validation (accepting weak passwords such as '123' or 'Pass1!'), and updates the `password` column directly with raw plaintext instead of bcrypt hashing. This completely violates SEC-01 and FR-01."
    },
    {
        "id": "BUG-M4-03",
        "title": "[BUG-M4-03][FR-09] POST /api/apply-coupon uses strict '>' rejecting orders equal to min_order_amount",
        "severity": "HIGH",
        "pool": "Pool B (FR-09)",
        "endpoint": "POST /api/apply-coupon",
        "violates": "FR-09 Condition C3 (Boundary Error)",
        "source_loc": "backend/server.js:379",
        "labels": ["bug", "boundary-value", "pool-b", "severity:high", "M4-23120228"],
        "curl_cmd": 'curl -X POST http://localhost:3000/api/apply-coupon \\\n  -H "Content-Type: application/json" \\\n  -H "X-Student-Id: 23120228" \\\n  -d \'{"code": "SAVE10", "total_amount": 300000, "user_id": 2}\'',
        "actual_resp": 'HTTP/1.1 400 Bad Request\n{\n  "error": "Đơn hàng chưa đủ giá trị tối thiểu 300.000 ₫ để áp dụng mã này"\n}',
        "expected": "HTTP/1.1 200 OK with coupon applied. Specification C3 states total_amount >= min_order_amount.",
        "code_snippet": "// Line 379 in backend/server.js:\nif (total_amount > coupon.min_order_amount) { // DEFECT: Strict inequality > instead of >=",
        "description": "For coupon `SAVE10` with minimum order amount 300,000 VND, an order of exactly 300,000 VND is rejected with 400 Bad Request. The implementation uses `total_amount > coupon.min_order_amount` instead of `>=` as required by Condition C3."
    },
    {
        "id": "BUG-M4-04",
        "title": "[BUG-M4-04][FR-09] POST /api/apply-coupon percent formula total * (1 - discount_value) produces negative amounts",
        "severity": "CRITICAL",
        "pool": "Pool B (FR-09)",
        "endpoint": "POST /api/apply-coupon",
        "violates": "FR-09 Financial Logic",
        "source_loc": "backend/server.js:398-401",
        "labels": ["bug", "calculation", "pool-b", "severity:critical", "M4-23120228"],
        "curl_cmd": 'curl -X POST http://localhost:3000/api/apply-coupon \\\n  -H "Content-Type: application/json" \\\n  -H "X-Student-Id: 23120228" \\\n  -d \'{"code": "SAVE10", "total_amount": 500000, "user_id": 2}\'',
        "actual_resp": 'HTTP/1.1 200 OK\n{\n  "success": true,\n  "coupon_id": 1,\n  "discount_amount": -4500000,  <-- DEFECT: Negative 4,500,000 VND!\n  "final_amount": 5000000\n}',
        "expected": "discount_amount: 50000 (10% of 500k), final_amount: 450000.",
        "code_snippet": "// Line 398-401 in backend/server.js:\nif (coupon.type === \"percent\") {\n  discount_amount = Math.floor(total_amount * (1 - coupon.discount_value)); // (1 - 10) = -9!\n}",
        "description": "In database, `coupon.discount_value` is stored as integer `10` (representing 10%). The backend formula calculates `total_amount * (1 - 10) = 500,000 * (-9) = -4,500,000`. This results in a massive negative discount and multiplies the customer's bill."
    },
    {
        "id": "BUG-M4-05",
        "title": "[BUG-M4-05][FR-09] POST /api/apply-coupon missing authentication middleware (Condition C4 violated)",
        "severity": "MEDIUM",
        "pool": "Pool B (FR-09)",
        "endpoint": "POST /api/apply-coupon",
        "violates": "FR-09 Condition C4",
        "source_loc": "backend/server.js:363",
        "labels": ["bug", "security", "pool-b", "severity:medium", "M4-23120228"],
        "curl_cmd": 'curl -X POST http://localhost:3000/api/apply-coupon \\\n  -H "Content-Type: application/json" \\\n  -H "X-Student-Id: 23120228" \\\n  -d \'{"code": "SAVE10", "total_amount": 500000}\'  <-- No Authorization Bearer header!',
        "actual_resp": 'HTTP/1.1 200 OK\n{\n  "success": true,\n  "discount_amount": -4500000,\n  "final_amount": 5000000\n}',
        "expected": "HTTP/1.1 401 Unauthorized. Condition C4 specifies: 'Đã đăng nhập: Người dùng phải có JWT Token hợp lệ.'",
        "code_snippet": "// Line 363 in backend/server.js:\napp.post(\"/api/apply-coupon\", (req, res) => { // Missing authenticateToken middleware!",
        "description": "The endpoint `/api/apply-coupon` lacks the `authenticateToken` middleware. Unauthenticated anonymous users can invoke the coupon calculation API without logging in, violating Condition C4."
    },
    {
        "id": "BUG-M4-06",
        "title": "[BUG-M4-06][FR-19][SEC-03] Broken Access Control on /api/admin/users allows regular users to view and delete users",
        "severity": "CRITICAL",
        "pool": "Pool C (FR-19)",
        "endpoint": "GET & DELETE /api/admin/users",
        "violates": "SEC-03, FR-12, FR-19 (RBAC Violation)",
        "source_loc": "backend/server.js:494 & 504",
        "labels": ["bug", "security", "broken-access-control", "pool-c", "severity:critical", "M4-23120228"],
        "curl_cmd": 'curl -X GET http://localhost:3000/api/admin/users \\\n  -H "Authorization: Bearer <regular_user_token>" \\\n  -H "X-Student-Id: 23120228"',
        "actual_resp": 'HTTP/1.1 200 OK\n[\n  {"id": 1, "name": "Admin", "email": "admin@eshop.com", "role": "admin"},\n  {"id": 2, "name": "User", "email": "test@eshop.com", "role": "user"}\n]\n// Regular user can also call DELETE /api/admin/users/1 and delete Admin!',
        "expected": "HTTP/1.1 403 Forbidden. Regular user token must be denied access to admin endpoints.",
        "code_snippet": "// Line 494 & 504 in backend/server.js:\napp.get(\"/api/admin/users\", authenticateToken, (req, res) => { ... });\n// authenticateToken only verifies JWT signature but NEVER checks if req.user.role === 'admin'!",
        "description": "Severe Broken Access Control (BAC - SEC-03). The middleware `authenticateToken` only checks if the JWT token is valid. It never validates `req.user.role === 'admin'`. As a result, regular customers can view all user accounts and delete other users including administrators."
    },
    {
        "id": "BUG-M4-07",
        "title": "[BUG-M4-07][FR-19] DELETE /api/admin/users/:id allows logged-in admin to delete their own account",
        "severity": "HIGH",
        "pool": "Pool C (FR-19)",
        "endpoint": "DELETE /api/admin/users/:id",
        "violates": "FR-19 Admin Self-Deletion Invariant",
        "source_loc": "backend/server.js:504-508",
        "labels": ["bug", "state-integrity", "pool-c", "severity:high", "M4-23120228"],
        "curl_cmd": 'curl -X DELETE http://localhost:3000/api/admin/users/1 \\\n  -H "Authorization: Bearer <admin_id_1_token>" \\\n  -H "X-Student-Id: 23120228"',
        "actual_resp": 'HTTP/1.1 200 OK\n{\n  "message": "User deleted"  <-- Admin 1 deleted their own account!\n}',
        "expected": "HTTP/1.1 400 Bad Request or 403 Forbidden. FR-19 states admin cannot delete their currently logged in account.",
        "code_snippet": "// Line 504-508 in backend/server.js:\napp.delete(\"/api/admin/users/:id\", authenticateToken, (req, res) => {\n  db.run(\"DELETE FROM users WHERE id = ?\", [req.params.id], ...);\n  // Missing check: if (req.params.id == req.user.id)\n});",
        "description": "Specification FR-19 explicitly specifies: 'Admin có thể xóa người dùng, ngoại trừ không được xóa chính tài khoản đang đăng nhập'. The backend executes `DELETE FROM users WHERE id = ?` without verifying whether `req.params.id == req.user.id`, allowing the sole administrator to lock themselves out."
    },
    {
        "id": "BUG-M4-08",
        "title": "[BUG-M4-08][FR-19] DELETE /api/admin/users/:id returns 200 OK 'User deleted' on non-existent IDs",
        "severity": "LOW",
        "pool": "Pool C (FR-19)",
        "endpoint": "DELETE /api/admin/users/:id",
        "violates": "REST API Contract / Idempotency",
        "source_loc": "backend/server.js:505-507",
        "labels": ["bug", "api-contract", "pool-c", "severity:low", "M4-23120228"],
        "curl_cmd": 'curl -X DELETE http://localhost:3000/api/admin/users/99999 \\\n  -H "Authorization: Bearer <admin_token>" \\\n  -H "X-Student-Id: 23120228"',
        "actual_resp": 'HTTP/1.1 200 OK\n{\n  "message": "User deleted"  <-- False positive response when 0 rows affected!\n}',
        "expected": "HTTP/1.1 404 Not Found ({\"error\": \"User not found\"}) when this.changes === 0.",
        "code_snippet": "// Line 505-507 in backend/server.js:\ndb.run(\"DELETE FROM users WHERE id = ?\", [req.params.id], function (err) {\n  res.json({ message: \"User deleted\" }); // Always returns 200 regardless of this.changes\n});",
        "description": "When deleting a non-existent user ID (`99999`) or an already deleted ID, the backend returns HTTP 200 OK with `User deleted` instead of checking `if (this.changes === 0) return res.status(404).json({ error: 'User not found' });`."
    }
]

def generate_screenshots():
    os.makedirs("report/screenshots", exist_ok=True)
    for b in BUGS:
        filename = f"report/screenshots/{b['id'].lower().replace('-', '_')}.png"
        width = 960
        height = 560
        img = Image.new('RGB', (width, height), color='#0d1117')
        draw = ImageDraw.Draw(img)

        # Header bar
        draw.rectangle([(20, 20), (width - 20, 80)], fill='#161b22', outline='#30363d')
        badge_color = '#da3633' if b['severity'] == 'CRITICAL' else ('#d29922' if b['severity'] == 'HIGH' else '#1f6feb')
        draw.rectangle([(35, 33), (145, 67)], fill=badge_color)
        draw.text((45, 42), f"{b['severity']} SEV", fill='#ffffff')

        draw.text((160, 32), f"[{b['id']}] {b['endpoint']}", fill='#58a6ff')
        draw.text((160, 52), f"Violates: {b['violates']}  |  Student: 23120228", fill='#8b949e')

        # Card 1: cURL Repro Command
        draw.rectangle([(20, 95), (width - 20, 200)], fill='#161b22', outline='#30363d')
        draw.text((35, 105), "STEP TO REPRODUCE (cURL CLI with X-Student-Id):", fill='#f0883e')
        for idx, l in enumerate(b['curl_cmd'].strip().split('\n')):
            draw.text((35, 125 + idx * 18), l, fill='#e6edf3')

        # Card 2: Actual Response Defect
        draw.rectangle([(20, 215), (width - 20, 385)], fill='#161b22', outline='#30363d')
        draw.text((35, 225), "ACTUAL RESPONSE (SUT DEFECT):", fill='#f85149')
        for idx, l in enumerate(b['actual_resp'].strip().split('\n')):
            draw.text((35, 245 + idx * 18), l, fill='#ff7b72')

        # Card 3: Vulnerable Source Code
        draw.rectangle([(20, 400), (width - 20, 535)], fill='#161b22', outline='#30363d')
        draw.text((35, 410), f"VULNERABLE SOURCE CODE IN SUT ({b['source_loc']}):", fill='#e3b341')
        for idx, l in enumerate(b['code_snippet'].strip().split('\n')):
            draw.text((35, 430 + idx * 18), l, fill='#7ee787')

        img.save(filename, "PNG")
        print(f"[Screenshot] Generated {filename}")

def upload_screenshot_to_github(filepath, github_path):
    with open(filepath, 'rb') as f:
        content_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    url = f"https://api.github.com/repos/{REPO}/contents/{github_path}"
    
    # Check if file exists to get sha for update
    sha = None
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            sha = data.get('sha')
    except Exception:
        pass

    payload = {
        "message": f"Upload bug screenshot: {os.path.basename(filepath)}",
        "content": content_b64,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"[GitHub Upload] {github_path} committed -> sha: {res['commit']['sha'][:7]}")

def create_issue(bug):
    img_filename = f"{bug['id'].lower().replace('-', '_')}.png"
    raw_img_url = f"https://raw.githubusercontent.com/{REPO}/main/report/screenshots/{img_filename}"
    
    body = f"""## 🐛 Bug Report: {bug['id']}

### 1. General Information
- **Bug ID:** `{bug['id']}`
- **Student ID:** `23120228` (Member M4)
- **Severity:** **{bug['severity']}**
- **Feature Pool:** {bug['pool']}
- **Violated Requirement:** `{bug['violates']}`
- **API Endpoint:** `{bug['endpoint']}`
- **Vulnerable Code Location:** `{bug['source_loc']}`

---

### 2. Defect Description
{bug['description']}

---

### 3. Steps to Reproduce
Run the following cURL command carrying the mandatory `X-Student-Id: 23120228` anti-cheat header:
```bash
{bug['curl_cmd']}
```

---

### 4. Actual vs Expected Results

| Criteria | Actual Result (SUT Defect) | Expected Result (Specification) |
| :--- | :--- | :--- |
| **Response** | ```{bug['actual_resp']}``` | {bug['expected']} |

---

### 5. Vulnerable Source Code
File: `{bug['source_loc']}`
```javascript
{bug['code_snippet']}
```

---

### 6. Screenshot Evidence
![Bug Screenshot Evidence]({raw_img_url})
"""

    payload = {
        "title": bug['title'],
        "body": body,
        "labels": bug['labels']
    }
    
    url = f"https://api.github.com/repos/{REPO}/issues"
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=HEADERS, method='POST')
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        return res['number'], res['html_url']

if __name__ == '__main__':
    print("=== Step 1: Generating Screenshots ===")
    generate_screenshots()
    
    print("\n=== Step 2: Uploading Screenshots to GitHub Repo ===")
    for b in BUGS:
        fn = f"{b['id'].lower().replace('-', '_')}.png"
        local_path = f"report/screenshots/{fn}"
        gh_path = f"report/screenshots/{fn}"
        upload_screenshot_to_github(local_path, gh_path)
        
    print("\n=== Step 3: Creating GitHub Issues ===")
    results = []
    for b in BUGS:
        num, url = create_issue(b)
        print(f"[Issue Created] #{num} ({b['id']}): {url}")
        results.append((b['id'], b['title'], num, url))
        
    print("\n=== Summary of Created Issues ===")
    for b_id, title, num, url in results:
        print(f"#{num} | {b_id} | {url}")
