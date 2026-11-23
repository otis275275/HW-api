# Test Case Specification — Pool C: FR-19 (Admin User Management)

**MSSV:** 23120228 | **Thành viên:** M4  
**Target Endpoints:**
- `GET /api/admin/users`
- `DELETE /api/admin/users/:id`  
**Base URL:** `http://localhost:3000`  
**Header bắt buộc:** `X-Student-Id: 23120228`

---

## 1. Danh sách Test Cases sinh bởi AI (Target $\ge 35$ Test Cases)

| Test Case ID | Mục kiểm thử | Endpoint & Method | Quyền / Header / Params | Kết quả mong đợi (Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FR19-01** | SEC - Admin lấy danh sách user hợp lệ | `GET /api/admin/users` | Token Admin (`role = 'admin'`) | 200 OK, trả về danh sách user |
| **TC-FR19-02** | **SEC - User thường gọi API lấy danh sách user (SEC-03)** | `GET /api/admin/users` | Token User (`role = 'user'`) | **403 Forbidden (Broken Access Control)** |
| **TC-FR19-03** | SEC - Không có token gọi lấy danh sách user | `GET /api/admin/users` | Không gửi header Authorization | 401 Unauthorized |
| **TC-FR19-04** | SEC - Token giả mạo/không hợp lệ | `GET /api/admin/users` | `Bearer invalid_token_123` | 403 Forbidden |
| **TC-FR19-05** | SEC - Token hết hạn | `GET /api/admin/users` | `Bearer expired_token` | 403 Forbidden |
| **TC-FR19-06** | Data Exposure - Không để lộ password trong danh sách | `GET /api/admin/users` | Token Admin | Trong mảng user trả về KHÔNG có trường `password` |
| **TC-FR19-07** | Data Exposure - Không để lộ reset_token | `GET /api/admin/users` | Token Admin | Trong mảng user trả về KHÔNG có trường `reset_token` |
| **TC-FR19-08** | DP - Admin xóa user thành công | `DELETE /api/admin/users/2` | Token Admin, ID user thường tồn tại | 200 OK, `User deleted` |
| **TC-FR19-09** | **SEC - User thường gọi API xóa user khác (SEC-03)** | `DELETE /api/admin/users/2` | Token User (`role = 'user'`) | **403 Forbidden (Broken Access Control)** |
| **TC-FR19-10** | **SEC - User thường cố tình xóa Admin (SEC-03)** | `DELETE /api/admin/users/1` | Token User (`role = 'user'`) | **403 Forbidden** |
| **TC-FR19-11** | SEC - Không có token gọi API xóa user | `DELETE /api/admin/users/2` | Không gửi Authorization | 401 Unauthorized |
| **TC-FR19-12** | **Ràng buộc FR-19 - Admin tự xóa chính tài khoản đang đăng nhập** | `DELETE /api/admin/users/1` | Token Admin (id = 1), param id = 1 | **400 Bad Request / 403 Forbidden (Cấm tự xóa chính mình)** |
| **TC-FR19-13** | DP - Xóa user không tồn tại | `DELETE /api/admin/users/9999` | Token Admin, ID = 9999 | 404 Not Found |
| **TC-FR19-14** | DP - ID user là số 0 | `DELETE /api/admin/users/0` | Token Admin, ID = 0 | 400 Bad Request / 404 Not Found |
| **TC-FR19-15** | DP - ID user là số âm | `DELETE /api/admin/users/-5` | Token Admin, ID = -5 | 400 Bad Request |
| **TC-FR19-16** | DP - ID user là chuỗi chữ | `DELETE /api/admin/users/abc` | Token Admin, ID = "abc" | 400 Bad Request |
| **TC-FR19-17** | DP - ID user chứa ký tự đặc biệt | `DELETE /api/admin/users/@!#` | Token Admin, ID = "@!#" | 400 Bad Request |
| **TC-FR19-18** | DP - SQLi trong tham số ID | `DELETE /api/admin/users/1 OR 1=1` | Token Admin, SQLi payload | 400 Bad Request |
| **TC-FR19-19** | DP - ID user là số cực lớn (Overflow) | `DELETE /api/admin/users/999999999999999` | Token Admin | 404 Not Found |
| **TC-FR19-20** | ST - Vòng đời xóa user: Xóa -> Kiểm tra danh sách | Sequence: DELETE /api/admin/users/2 -> GET /api/admin/users | Token Admin | User ID 2 không còn xuất hiện trong danh sách |
| **TC-FR19-21** | ST - User bị xóa không thể đăng nhập | Sequence: DELETE User 2 -> POST /api/login với User 2 | Credentials User 2 | 401 Unauthorized |
| **TC-FR19-22** | ST - Xóa user đã bị xóa trước đó (Idempotency) | Sequence: DELETE User 2 (lần 1) -> DELETE User 2 (lần 2) | Token Admin | Lần 1: 200 OK, Lần 2: 404 Not Found |
| **TC-FR19-23** | ST - User bị xóa thì token cũ bị vô hiệu hóa | Sequence: User 2 lấy token -> Admin xóa User 2 -> User 2 gọi API | Token cũ của User 2 | 401 Unauthorized / 403 Forbidden |
| **TC-FR19-24** | SEC - Kiểm tra role escalation qua JWT header | `GET /api/admin/users` | Token sửa role thành admin nhưng sai signature | 403 Forbidden |
| **TC-FR19-25** | Schema - Schema của `GET /api/admin/users` | `GET /api/admin/users` | Token Admin | Trả về mảng JSON đúng schema các trường |
| **TC-FR19-26** | Schema - Kiểu dữ liệu trường trong user object | `GET /api/admin/users` | Token Admin | `id` là integer, `email` là string, `role` là string |
| **TC-FR19-27** | Schema - Schema của `DELETE /api/admin/users/:id` | `DELETE /api/admin/users/2` | Token Admin | Trả về `{ "message": "User deleted" }` |
| **TC-FR19-28** | DP - Admin xóa một user có đơn hàng | `DELETE /api/admin/users/2` | User 2 đã có đơn hàng | Xử lý toàn vẹn dữ liệu (Cascade/Restricted) |
| **TC-FR19-29** | DP - Header Content-Type khi DELETE | `DELETE /api/admin/users/2` | Kiểm tra Content-Type | `application/json` |
| **TC-FR19-30** | DP - HTTP Method không hợp lệ trên `/api/admin/users` | `POST /api/admin/users` | Không hỗ trợ POST tại endpoint này | 404 Not Found / 405 Method Not Allowed |
| **TC-FR19-31** | DP - HTTP Method không hợp lệ trên `/api/admin/users/:id` | `POST /api/admin/users/1` | Không hỗ trợ POST tại endpoint này | 404 Not Found / 405 Method Not Allowed |
| **TC-FR19-32** | Schema - Error Schema khi thiếu Authorization | `GET /api/admin/users` | Không token | `{ "error": "Unauthorized" }` (401) |
| **TC-FR19-33** | Schema - Error Schema khi token không hợp lệ | `GET /api/admin/users` | Sai Bearer | `{ "error": "Forbidden" }` (403) |
| **TC-FR19-34** | SEC - Kiểm tra SQL Injection qua Header Authorization | `GET /api/admin/users` | `Authorization: Bearer ' OR 1=1 --` | 403 Forbidden |
| **TC-FR19-35** | SEC - Kiểm tra XSS trong danh sách trả về | `GET /api/admin/users` | User có tên chứa thẻ HTML/Script | Dữ liệu trả về dạng JSON thuần, không trigger script |

---

## 2. Bảng Human Audit Từng Test Case (35/35 Test Cases Evaluated)

Dưới đây là kết quả kiểm toán độc lập của sinh viên đối với từng ca kiểm thử của FR-19, phân loại VALID / INVALID / INCOMPLETE kèm căn cứ kỹ thuật và biện pháp khắc phục:

| Test Case ID | Nhãn Kiểm toán | Lý do đánh giá của Sinh viên | Hành động Hiệu chỉnh (Correction) |
| :--- | :---: | :--- | :--- |
| **TC-FR19-01** | **VALID** | Happy-path chuẩn: Admin có token hợp lệ lấy danh sách người dùng. | Giữ nguyên assertion `status === 200` và kiểm tra body là array. |
| **TC-FR19-02** | **INVALID / CRITICAL** | **Lỗ hổng kiểm soát truy cập (BAC - SEC-03):** AI ban đầu dự kiến 403, nhưng middleware `authenticateToken` chỉ kiểm tra chữ ký JWT mà **hoàn toàn không kiểm tra `role === 'admin'`**. | **Hiệu chỉnh:** Sử dụng token thật của Regular User (`userToken`) và assert nghiêm ngặt `pm.response.to.have.status(403)` $\rightarrow$ Bắt chính xác **BUG-M4-06** (SUT trả về 200 OK để lộ danh sách user cho người dùng thường)! |
| **TC-FR19-03** | **VALID** | Kiểm thử truy cập ẩn danh không mang Header Authorization. | Giữ nguyên mong đợi 401 Unauthorized. |
| **TC-FR19-04** | **VALID** | Kiểm thử gửi chuỗi token rác không hợp lệ. | Giữ nguyên mong đợi 403 Forbidden. |
| **TC-FR19-05** | **VALID** | Kiểm thử token JWT đã hết hạn sử dụng. | Giữ nguyên mong đợi 403 Forbidden. |
| **TC-FR19-06** | **VALID** | Yêu cầu bảo mật: danh sách user trả về không được để lộ mật khẩu. | Bổ sung assertion duyệt mảng: `arr.forEach(u => pm.expect(u).to.not.have.property('password'))`. |
| **TC-FR19-07** | **VALID** | Yêu cầu bảo mật: không để lộ mã `reset_token`. | Bổ sung assertion duyệt mảng: `arr.forEach(u => pm.expect(u).to.not.have.property('reset_token'))`. |
| **TC-FR19-08** | **VALID** | Admin xóa tài khoản người dùng thường (User 2) thành công. | Giữ nguyên mong đợi 200 OK. |
| **TC-FR19-09** | **INVALID / CRITICAL** | **Lỗ hổng leo quyền xóa user (BAC - SEC-03):** Người dùng thường gọi lệnh xóa User 2. AI ban đầu nhầm endpoint gọi sang xóa Admin 1. | **Hiệu chỉnh:** Chỉnh đúng endpoint `DELETE /api/admin/users/2` mang header của `userToken`, mong đợi 403 Forbidden $\rightarrow$ Bắt chính xác **BUG-M4-06** (SUT trả về 200 OK cho phép user thường tự ý xóa user khác). |
| **TC-FR19-10** | **INVALID / CRITICAL** | **User thường xóa tài khoản Admin:** Người dùng thường gửi lệnh `DELETE /api/admin/users/1`. | **Hiệu chỉnh:** Sử dụng `userToken` gọi xóa ID 1, mong đợi 403 Forbidden $\rightarrow$ Bắt chính xác **BUG-M4-06** (SUT trả về 200 OK xóa luôn tài khoản Admin!). |
| **TC-FR19-11** | **VALID** | Khách vãng lai không token gọi API xóa user. | Giữ nguyên mong đợi 401 Unauthorized. |
| **TC-FR19-12** | **INVALID / CRITICAL** | **Vi phạm ràng buộc chống tự xóa (FR-19):** Đề bài quy định *"Admin không được xóa chính tài khoản đang đăng nhập"*. Code SUT thiếu lệnh `if (req.params.id == req.user.id)`. | **Hiệu chỉnh:** Admin (ID 1) gửi `DELETE /api/admin/users/1`, assert mong đợi 400 hoặc 403 $\rightarrow$ Bắt chính xác **BUG-M4-07** (SUT xóa luôn tài khoản Admin đang login với 200 OK)! |
| **TC-FR19-13** | **INVALID / CRITICAL** | **Lỗi hợp đồng REST API:** Xóa ID không tồn tại (`9999`), code SUT không kiểm tra `this.changes === 0` nên luôn trả về 200 OK. | **Hiệu chỉnh:** Đặt assertion mong đợi 404 Not Found $\rightarrow$ Bắt chính xác **BUG-M4-08** (SUT trả về 200 OK giả mạo 'User deleted'). |
| **TC-FR19-14** | **VALID** | Phân hoạch ID = 0. | Giữ nguyên mong đợi 400 Bad Request hoặc 404. |
| **TC-FR19-15** | **VALID** | Phân hoạch ID âm (`-5`). | Giữ nguyên mong đợi 400 Bad Request hoặc 404. |
| **TC-FR19-16** | **VALID** | Phân hoạch ID dạng chuỗi chữ (`"abc"`). | Giữ nguyên mong đợi 400 Bad Request hoặc 404. |
| **TC-FR19-17** | **VALID** | Phân hoạch ID chứa ký tự đặc biệt (`"@!#"`). | Giữ nguyên mong đợi 400 Bad Request hoặc 404. |
| **TC-FR19-18** | **VALID** | Kiểm thử SQL Injection trong path param (`1 OR 1=1`). | Giữ nguyên mong đợi 400/404 an toàn. |
| **TC-FR19-19** | **VALID** | Phân tích giá trị biên số nguyên tràn bộ nhớ (Overflow ID). | Giữ nguyên mong đợi 404 Not Found. |
| **TC-FR19-20** | **VALID** | Chuyển trạng thái: Kiểm tra User 2 đã biến mất khỏi danh sách user sau khi xóa. | Bổ sung assertion: `pm.expect(users.find(u => u.id === 2)).to.be.undefined`. |
| **TC-FR19-21** | **VALID** | Chuyển trạng thái: User 2 đã bị xóa không thể đăng nhập lại. | Gửi `POST /api/login` với credentials của User 2, mong đợi 401 Unauthorized. |
| **TC-FR19-22** | **INVALID / CRITICAL** | **Tính lũy thừa (Idempotency):** Gọi lệnh xóa User 2 lần thứ 2. | **Hiệu chỉnh:** Đặt assertion mong đợi 404 Not Found $\rightarrow$ Bắt **BUG-M4-08** (SUT vẫn báo 200 OK 'User deleted' dù bản ghi không còn). |
| **TC-FR19-23** | **VALID** | Kiểm thử vô hiệu hóa JWT Token cũ của user đã bị xóa. | Giữ nguyên. |
| **TC-FR19-24** | **VALID** | Kiểm thử tấn công leo quyền: Tự sửa payload JWT `role: "admin"` nhưng sai signature bí mật. | Giữ nguyên mong đợi 403 Forbidden. |
| **TC-FR19-25** | **VALID** | Xác thực JSON Schema của mảng danh sách người dùng. | Giữ nguyên. |
| **TC-FR19-26** | **VALID** | Xác thực kiểu dữ liệu từng thuộc tính trong đối tượng user (`id: number`, `name: string`, `email: string`, `role: string`). | Giữ nguyên. |
| **TC-FR19-27** | **VALID** | Xác thực JSON Schema phản hồi của `DELETE /api/admin/users/:id`. | Kiểm tra body có thuộc tính `message`. |
| **TC-FR19-28** | **VALID** | Kiểm tra toàn vẹn tham chiếu khi xóa user đã có đơn hàng trong CSDL. | Giữ nguyên. |
| **TC-FR19-29** | **VALID** | Xác thực Header `Content-Type: application/json` của phản hồi xóa. | Giữ nguyên. |
| **TC-FR19-30** | **VALID** | Kiểm thử phương thức HTTP không được hỗ trợ (`POST /api/admin/users`). | Giữ nguyên mong đợi 404/405. |
| **TC-FR19-31** | **VALID** | Kiểm thử phương thức HTTP không được hỗ trợ (`POST /api/admin/users/:id`). | Giữ nguyên mong đợi 404/405. |
| **TC-FR19-32** | **VALID** | Xác thực JSON Schema phản hồi lỗi 401 Unauthorized. | Kiểm tra body `{ "error": "Unauthorized" }`. |
| **TC-FR19-33** | **VALID** | Xác thực JSON Schema phản hồi lỗi 403 Forbidden. | Kiểm tra body `{ "error": "Forbidden" }`. |
| **TC-FR19-34** | **VALID** | Kiểm thử SQL Injection chèn vào Header Authorization. | Giữ nguyên mong đợi 403 Forbidden. |
| **TC-FR19-35** | **VALID** | Kiểm tra hiển thị an toàn chống XSS trong danh sách người dùng. | Giữ nguyên. |

---

## 3. Mở rộng (+5 Test Cases nâng cao AI bỏ sót & Giải thích)

| Test Case ID | Mục kiểm thử mở rộng | Input / Kịch bản thực thi | Kết quả mong đợi | Giải thích tại sao AI bỏ sót |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FR19-EXT01** | **Xử lý toàn vẹn dữ liệu đơn hàng khi User bị xóa (Orphaned Records)** | User 2 tạo đơn hàng. Admin xóa User 2. Admin gọi `GET /api/admin/orders`. | Các đơn hàng cũ của User 2 vẫn phải bảo toàn dữ liệu lịch sử hoặc hiển thị `user_name: "[Deleted User]"`, không bị lỗi crash SQL JOIN `500 Internal Server Error`. | AI thường chỉ test cục bộ bảng `users` mà không kiểm tra tính toàn vẹn tham chiếu (Foreign Key Integrity) giữa các bảng `orders`, `cart`, `coupon_usage` với `users`. |
| **TC-FR19-EXT02** | **Ngăn chặn xóa tài khoản Admin CUỐI CÙNG của hệ thống** | Hệ thống chỉ còn duy nhất 1 tài khoản Admin. Một tài khoản khác cố gắng xóa Admin này. | 400 Bad Request (Hệ thống phải có tối thiểu một Quản trị viên đang hoạt động). | AI chỉ bám vào việc cấm tự xóa chính mình (Self-deletion) mà bỏ qua bài toán quản trị hệ thống: không bao giờ được phép xóa sạch toàn bộ admin khiến hệ thống mất quyền quản trị. |
| **TC-FR19-EXT03** | **Xóa người dùng đang trong trạng thái bị KHÓA (Account Lockout)** | User đăng nhập sai 3 lần $\rightarrow$ bị khóa tạm thời (`locked_until`). Admin gọi `DELETE /api/admin/users/:id`. | Xóa thành công hoặc có cảnh báo tài khoản đang bị khóa. | AI thường coi các thuộc tính bảo mật như `locked_until` là độc lập, không kết hợp trạng thái khóa tài khoản (Security Lock State) với tính năng CRUD của Admin. |
| **TC-FR19-EXT04** | **Phân trang và giới hạn tải trọng (Pagination & DoS Prevention)** | Tạo giả lập 1.000 users trong CSDL, sau đó gọi `GET /api/admin/users`. | API phải hỗ trợ query phân trang `?page=1&limit=20`, không được load toàn bộ 1.000 users cùng lúc gây cạn kiệt bộ nhớ. | Trong đặc tả API, endpoint không nhắc đến phân trang nên AI mặc định chỉ test lấy toàn bộ (`SELECT * FROM users`), bỏ qua bài toán hiệu năng và tấn công từ chối dịch vụ (DoS / Resource Exhaustion). |
| **TC-FR19-EXT05** | **Tranh chấp xóa người dùng đồng thời (Concurrent Delete)** | 2 Admin đồng thời gửi lệnh xóa cùng User ID 2 trong cùng 1 mili-giây. | 1 request trả về 200 OK, request thứ 2 trả về 404 Not Found (Xử lý đồng thời nhất quán). | AI không tự động xây dựng các bài test bất đồng bộ phức tạp để kiểm tra cơ chế khóa bản ghi (Row-level Locking) của CSDL SQLite. |
