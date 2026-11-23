"""
Member M4 API Test Generator Script (HW06 EShop SUT)
Dedicated to:
- Pool A (FR-03): POST /api/forgot-password, POST /api/reset-password
- Pool B (FR-09): POST /api/apply-coupon
- Pool C (FR-19): GET /api/admin/users, DELETE /api/admin/users/:id

Outputs comprehensive Postman Collection v2.1 with mandatory X-Student-Id pre-request header.
"""

import json
import os
import sys

def build_m4_postman_collection(student_id="23120228", base_url="http://localhost:3000"):
    collection = {
        "info": {
            "name": f"HW06_M4_EShop_API_TestSuite_{student_id}",
            "_postman_id": f"hw06-m4-{student_id}",
            "description": "API Test Suite exclusively crafted for Member M4 covering FR-03, FR-09, and FR-19.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "// Enforce X-Student-Id header requirement across all requests",
                        "const studentId = pm.environment.get('studentId') || '" + student_id + "';",
                        "pm.request.headers.upsert({ key: 'X-Student-Id', value: studentId });",
                        "console.log('[M4 Pre-request] Injected X-Student-Id:', studentId);"
                    ]
                }
            }
        ],
        "variable": [
            {"key": "baseUrl", "value": base_url, "type": "string"},
            {"key": "studentId", "value": student_id, "type": "string"},
            {"key": "userToken", "value": "", "type": "string"},
            {"key": "adminToken", "value": "", "type": "string"},
            {"key": "generatedResetToken", "value": "", "type": "string"},
            {"key": "testUserId", "value": "2", "type": "string"},
            {"key": "adminUserId", "value": "1", "type": "string"}
        ],
        "item": [
            {
                "name": "0. Setup & Auth",
                "item": [
                    {
                        "name": "Login as Admin (Get Admin Token)",
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "type": "text/javascript",
                                    "exec": [
                                        "pm.test('Status is 200 OK', function () { pm.response.to.have.status(200); });",
                                        "const jsonData = pm.response.json();",
                                        "pm.environment.set('adminToken', jsonData.token);",
                                        "pm.environment.set('adminUserId', jsonData.user.id);"
                                    ]
                                }
                            }
                        ],
                        "request": {
                            "method": "POST",
                            "header": [{"key": "Content-Type", "value": "application/json"}],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({"email": "admin@eshop.com", "password": "Admin123!"})
                            },
                            "url": {"raw": "{{baseUrl}}/api/login", "host": ["{{baseUrl}}"], "path": ["api", "login"]}
                        }
                    },
                    {
                        "name": "Login as User (Get User Token)",
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "type": "text/javascript",
                                    "exec": [
                                        "pm.test('Status is 200 OK', function () { pm.response.to.have.status(200); });",
                                        "const jsonData = pm.response.json();",
                                        "pm.environment.set('userToken', jsonData.token);",
                                        "pm.environment.set('testUserId', jsonData.user.id);"
                                    ]
                                }
                            }
                        ],
                        "request": {
                            "method": "POST",
                            "header": [{"key": "Content-Type", "value": "application/json"}],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({"email": "test@eshop.com", "password": "Test1234!"})
                            },
                            "url": {"raw": "{{baseUrl}}/api/login", "host": ["{{baseUrl}}"], "path": ["api", "login"]}
                        }
                    }
                ]
            },
            {
                "name": "1. Pool A (FR-03: Forgot & Reset Password)",
                "description": "Test cases covering Domain Partitioning, State Transitions, Security SEC-01 & SEC-07, and Schema Validation.",
                "item": []
            },
            {
                "name": "2. Pool B (FR-09: Apply Coupon)",
                "description": "Test cases covering the 5 Conditions (C1-C5), BVA on min_order_amount, Math calculation integrity, and Schema Validation.",
                "item": []
            },
            {
                "name": "3. Pool C (FR-19: Admin Users)",
                "description": "Test cases covering Broken Access Control (SEC-03), Self-Deletion Guard, Data Exposure, and State Transitions.",
                "item": []
            }
        ]
    }
    return collection

if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "M4_STUDENT_ID"
    col = build_m4_postman_collection(student_id=sid)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "postman")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "m4_eshop_collection.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(col, f, indent=2, ensure_ascii=False)
    print(f"[M4 Generator] Successfully initialized Postman collection at {out_path}")
