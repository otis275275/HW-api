# Test Case Specification — Pool B: FR-09 (Apply Coupon)

**MSSV:** 23120228 | **Thành viên:** M4  
**Target Endpoint:** `POST /api/apply-coupon`  
**Base URL:** `http://localhost:3000`  
**Header bắt buộc:** `X-Student-Id: 23120228`

---

## 1. Danh sách Test Cases sinh bởi AI (Target $\ge 35$ Test Cases)

| Test Case ID | Mục kiểm thử | Dữ liệu đầu vào (Payload) | Điều kiện kiểm tra | Kết quả mong đợi (Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FR09-01** | C1 - Mã giảm giá hợp lệ hoạt động | `{"code": "SAVE10", "total_amount": 500000, "user_id": 2}` | SAVE10 (10%, min 300k, còn hạn) | 200 OK, giảm 50.000, còn 450.000 |
| **TC-FR09-02** | C1 - Mã cố định (fixed) hợp lệ | `{"code": "BIGBUY", "total_amount": 600000, "user_id": 2}` | BIGBUY (50k, min 500k, còn hạn) | 200 OK, giảm 50.000, còn 550.000 |
| **TC-FR09-03** | C1 - Mã không tồn tại trong CSDL | `{"code": "UNKNOWN99", "total_amount": 500000, "user_id": 2}` | Mã không có trong bảng coupons | 404 Not Found |
| **TC-FR09-04** | C1 - Mã bị vô hiệu hóa (`is_active = 0`) | `{"code": "INACTIVE10", "total_amount": 500000, "user_id": 2}` | Mã có `is_active = 0` | 404 Not Found |
| **TC-FR09-05** | C1 - Mã giảm giá rỗng | `{"code": "", "total_amount": 500000, "user_id": 2}` | Chuỗi rỗng | 400 Bad Request |
| **TC-FR09-06** | C1 - Thiếu trường `code` | `{"total_amount": 500000, "user_id": 2}` | Không truyền key `code` | 400 Bad Request |
| **TC-FR09-07** | C1 - SQLi trong mã giảm giá | `{"code": "' OR '1'='1", "total_amount": 500000, "user_id": 2}` | SQL Injection payload | 404 Not Found (hoặc 400) |
| **TC-FR09-08** | C1 - Mã dạng chữ thường | `{"code": "save10", "total_amount": 500000, "user_id": 2}` | Kiểm tra case-insensitivity | 200 OK hoặc 404 |
| **TC-FR09-09** | C2 - Mã đã hết hạn | `{"code": "EXPIRED", "total_amount": 200000, "user_id": 2}` | EXPIRED (`expired_at: 2020-01-01`) | 400 Bad Request ("Mã đã hết hạn") |
| **TC-FR09-10** | C2 - Mã vừa hết hạn (Biên quá khứ 1 giây) | `{"code": "JUST_EXPIRED", "total_amount": 500000, "user_id": 2}` | Ngày hiện tại > `expired_at` | 400 Bad Request |
| **TC-FR09-11** | C2 - Mã còn hạn dài (2099-12-31) | `{"code": "SAVE10", "total_amount": 400000, "user_id": 2}` | Ngày hiện tại < `expired_at` | 200 OK |
| **TC-FR09-12** | C3 - Đơn hàng nhỏ hơn mức tối thiểu | `{"code": "SAVE10", "total_amount": 299999, "user_id": 2}` | min: 300.000, input: 299.999 | 400 Bad Request |
| **TC-FR09-13** | **C3 - Đơn hàng BẰNG CHÍNH XÁC mức tối thiểu** | `{"code": "SAVE10", "total_amount": 300000, "user_id": 2}` | min: 300.000, input: 300.000 | **200 OK (Spec: >= min_order_amount)** |
| **TC-FR09-14** | C3 - Đơn hàng lớn hơn mức tối thiểu 1 đơn vị | `{"code": "SAVE10", "total_amount": 300001, "user_id": 2}` | min: 300.000, input: 300.001 | 200 OK |
| **TC-FR09-15** | C3 - Đơn hàng giá trị 0 đồng | `{"code": "SAVE10", "total_amount": 0, "user_id": 2}` | input: 0 | 400 Bad Request |
| **TC-FR09-16** | C3 - Đơn hàng giá trị âm | `{"code": "SAVE10", "total_amount": -100000, "user_id": 2}` | input: -100.000 | 400 Bad Request |
| **TC-FR09-17** | C3 - Thiếu trường `total_amount` | `{"code": "SAVE10", "user_id": 2}` | Không truyền `total_amount` | 400 Bad Request |
| **TC-FR09-18** | C3 - `total_amount` là chuỗi chữ | `{"code": "SAVE10", "total_amount": "abc", "user_id": 2}` | Sai kiểu dữ liệu | 400 Bad Request |
| **TC-FR09-19** | C3 - `total_amount` là số thực (float) | `{"code": "SAVE10", "total_amount": 350000.5, "user_id": 2}` | Số thập phân | 200 OK |
| **TC-FR09-20** | C4 - Áp dụng khi chưa đăng nhập (Không token) | `{"code": "SAVE10", "total_amount": 500000}` (No Bearer) | Thiếu Header Authorization | 401 Unauthorized (vi phạm C4) |
| **TC-FR09-21** | C4 - Áp dụng với Token giả mạo/hết hạn | `{"code": "SAVE10", "total_amount": 500000}` (Token invalid) | Bearer invalid | 403 Forbidden |
| **TC-FR09-22** | C4 - Truyền `user_id` không khớp với Token | `{"code": "SAVE10", "total_amount": 500000, "user_id": 999}` | Token User 2, body user_id 999 | 403 Forbidden (chống giả mạo ID) |
| **TC-FR09-23** | C5 - Sử dụng mã lần đầu tiên (Usage = 0) | `{"code": "SAVE10", "total_amount": 500000, "user_id": 2}` | Chưa từng dùng SAVE10 | 200 OK |
| **TC-FR09-24** | C5 - Sử dụng mã lần 2 khi giới hạn là 1 | Sequence: Dùng SAVE10 -> Checkout -> Áp dụng lại | max_uses = 1, lần 2 | 400 Bad Request ("Đã đạt giới hạn") |
| **TC-FR09-25** | C5 - Dùng mã VIP100 lần 1 (max_uses = 2) | `{"code": "VIP100", "total_amount": 400000, "user_id": 2}` | Lần 1 trên 2 | 200 OK |
| **TC-FR09-26** | C5 - Dùng mã VIP100 lần 2 (max_uses = 2) | Sequence: Dùng VIP100 (1) -> Dùng VIP100 (2) | Lần 2 trên 2 | 200 OK |
| **TC-FR09-27** | C5 - Dùng mã VIP100 lần 3 (Vượt giới hạn) | Sequence: VIP100 (1) -> VIP100 (2) -> Lần 3 | Lần 3 trên 2 | 400 Bad Request ("Đã đạt giới hạn") |
| **TC-FR09-28** | Math - Kiểm tra tính giảm giá phần trăm | `{"code": "SAVE10", "total_amount": 500000, "user_id": 2}` | Giảm 10% của 500k | `discount_amount: 50000`, `final_amount: 450000` |
| **TC-FR09-29** | Math - Kiểm tra tính giảm giá cố định | `{"code": "BIGBUY", "total_amount": 500000, "user_id": 2}` | Giảm cố định 50k | `discount_amount: 50000`, `final_amount: 450000` |
| **TC-FR09-30** | Math - Tiền giảm cố định lớn hơn tổng đơn | `{"code": "BIGBUY", "total_amount": 40000, "user_id": 2}` | Giảm 50k trên đơn 40k | `final_amount >= 0` (không được âm) |
| **TC-FR09-31** | ST - User A dùng hết lượt, User B dùng | Sequence: User 2 dùng hết lượt -> User 3 dùng | Giới hạn theo từng user | User 3 vẫn dùng được 200 OK |
| **TC-FR09-32** | Schema - Schema thành công đầy đủ | `{"code": "SAVE10", "total_amount": 500000, "user_id": 2}` | Kiểm tra response keys | Chứa `success`, `coupon_id`, `discount_amount`, `final_amount`, `message` |
| **TC-FR09-33** | Schema - Kiểu dữ liệu số của `final_amount` | `{"code": "SAVE10", "total_amount": 500000, "user_id": 2}` | Type assertion | `typeof final_amount === 'number'` |
| **TC-FR09-34** | Schema - Error Schema khi thiếu code | `{"total_amount": 500000}` | Error schema | 400, `{error: string}` |
| **TC-FR09-35** | Schema - Error Schema khi mã hết hạn | `{"code": "EXPIRED", "total_amount": 500000}` | Error schema | 400, `{error: string}` |

---

## 2. Bảng Human Audit Từng Test Case (35/35 Test Cases Evaluated)

Dưới đây là kết quả kiểm toán độc lập của sinh viên đối với từng ca kiểm thử của FR-09, phân loại VALID / INVALID / INCOMPLETE kèm căn cứ kỹ thuật và biện pháp khắc phục:

| Test Case ID | Nhãn Kiểm toán | Lý do đánh giá của Sinh viên | Hành động Hiệu chỉnh (Correction) |
| :--- | :---: | :--- | :--- |
| **TC-FR09-01** | **INVALID / CRITICAL** | **Bug nghiêm trọng:** AI ban đầu chỉ assert `status === 200` mà không assert giá trị số tiền. Thực tế SUT tính `(1 - discount_value) = (1 - 10) = -9`, sinh ra số tiền âm `-4.500.000 ₫`. | **Hiệu chỉnh:** Bổ sung assertion toán học: `pm.expect(json.discount_amount).to.eql(50000)` và `pm.expect(json.final_amount).to.eql(450000)` $\rightarrow$ Bắt chính xác **BUG-M4-04**! |
| **TC-FR09-02** | **VALID** | Kiểm thử chuẩn cho mã giảm giá cố định (fixed discount). | Giữ nguyên assertion giảm 50.000 ₫ và thành tiền 550.000 ₫. |
| **TC-FR09-03** | **VALID** | Phân hoạch hợp lệ cho mã không tồn tại. | Giữ nguyên mong đợi 404 Not Found. |
| **TC-FR09-04** | **VALID** | Phân hoạch hợp lệ cho mã bị vô hiệu (`is_active = 0`). | Giữ nguyên mong đợi 404 Not Found. |
| **TC-FR09-05** | **VALID** | Phân hoạch giá trị biên mã rỗng `""`. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-06** | **VALID** | Phân hoạch thiếu trường `code`. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-07** | **VALID** | Kiểm thử SQL Injection trong mã coupon. | Đảm bảo server xử lý an toàn (404/400), không bị lỗi cú pháp SQL. |
| **TC-FR09-08** | **VALID** | Kiểm tra phân biệt hoa thường của mã coupon. | Giữ nguyên. |
| **TC-FR09-09** | **INCOMPLETE** | AI ban đầu để `total_amount: 500000`, lệch so với file đặc tả (đặc tả để 200.000 ₫). | **Hiệu chỉnh:** Chỉnh lại payload đúng `total_amount: 200000` và kiểm tra thông báo tiếng Việt "Mã giảm giá đã hết hạn". |
| **TC-FR09-10** | **VALID** | Kiểm thử giá trị biên thời gian vừa hết hạn. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-11** | **VALID** | Kiểm thử mã còn hạn dài trong tương lai. | Giữ nguyên mong đợi 200 OK. |
| **TC-FR09-12** | **VALID** | Phân hoạch giá trị biên dưới mức tối thiểu ($299.999 < 300.000$). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-13** | **INVALID / CRITICAL** | **Lỗi so sánh ngặt:** AI ban đầu giả định server đúng, nhưng code SUT viết `total_amount > min_order_amount` (dấu `>` thay vì `>=`). | **Hiệu chỉnh:** Đặt assertion nghiêm ngặt `pm.response.to.have.status(200)` tại mốc đúng 300.000 ₫ để bắt chính xác **BUG-M4-03** (SUT trả về 400 từ chối sai luật). |
| **TC-FR09-14** | **VALID** | Phân hoạch giá trị biên trên mức tối thiểu 1 đơn vị ($300.001 > 300.000$). | Giữ nguyên mong đợi 200 OK. |
| **TC-FR09-15** | **VALID** | Phân hoạch tổng đơn hàng bằng 0. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-16** | **VALID** | Phân hoạch giá trị âm ($-100.000$). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-17** | **VALID** | Phân hoạch thiếu trường `total_amount`. | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-18** | **VALID** | Phân hoạch sai kiểu dữ liệu (string `"abc"`). | Giữ nguyên mong đợi 400 Bad Request. |
| **TC-FR09-19** | **VALID** | Phân hoạch số thực (float `350000.5`). | Giữ nguyên mong đợi 200 OK. |
| **TC-FR09-20** | **INVALID / CRITICAL** | **Thiếu xác thực (C4):** Yêu cầu C4 quy định rõ người dùng phải đăng nhập có Token. Nhưng code SUT thiếu middleware `authenticateToken`. | **Hiệu chỉnh:** Gửi request KHÔNG có header Authorization và assert `pm.response.to.have.status(401)` $\rightarrow$ Bắt chính xác **BUG-M4-05** (SUT vẫn cho phép khách vãng lai gọi 200 OK). |
| **TC-FR09-21** | **VALID** | Kiểm thử token giả mạo / hết hạn. | Giữ nguyên. |
| **TC-FR09-22** | **VALID** | Kiểm thử tấn công giả mạo `user_id` (IDOR). | Giữ nguyên. |
| **TC-FR09-23** | **VALID** | Kiểm thử lần sử dụng đầu tiên của người dùng. | Giữ nguyên mong đợi 200 OK. |
| **TC-FR09-24** | **INCOMPLETE** | AI gọi apply 2 lần nhưng không qua bước checkout/ghi nhận `coupon_usage`, nên lần 2 vẫn là 0 lượt dùng. | **Hiệu chỉnh:** Thêm Pre-request Script tự động gửi `POST /api/coupon-usage` để ghi nhận lượt dùng 1 trước khi test lần 2 $\rightarrow$ Bắt lỗi vượt hạn mức (400). |
| **TC-FR09-25** | **VALID** | Kiểm thử lần 1 của mã có `max_uses = 2`. | Giữ nguyên mong đợi 200 OK. |
| **TC-FR09-26** | **INCOMPLETE** | Tương tự TC-24, cần ghi nhận lượt 1 vào CSDL trước khi test lần 2. | **Hiệu chỉnh:** Bổ sung Pre-request Script tiêm 1 bản ghi vào `coupon_usage` $\rightarrow$ mong đợi vẫn được phép 200 OK. |
| **TC-FR09-27** | **INCOMPLETE** | Cần ghi nhận 2 lượt dùng trước khi test lần 3 vượt hạn mức. | **Hiệu chỉnh:** Bổ sung Pre-request Script tiêm 2 bản ghi vào `coupon_usage` $\rightarrow$ mong đợi bị từ chối 400 Bad Request. |
| **TC-FR09-28** | **VALID / CRITICAL** | Kiểm tra độ toàn vẹn công thức tính % (nhân bản TC-01 để đối chiếu). | Bổ sung assertion kiểm tra giá trị số tiền $\rightarrow$ Bắt **BUG-M4-04**. |
| **TC-FR09-29** | **VALID** | Kiểm tra công thức giảm giá cố định (50k off 500k). | Giữ nguyên assertion `discount: 50000`, `final: 450000`. |
| **TC-FR09-30** | **VALID** | Kiểm thử logic tài chính khi tiền giảm lớn hơn tổng đơn (không được âm). | Giữ nguyên mong đợi 400 Bad Request (đơn chưa đủ ngưỡng). |
| **TC-FR09-31** | **VALID** | Kiểm thử tính độc lập quota theo từng người dùng (User A hết lượt, User B vẫn dùng được). | Sử dụng Token của Admin/User khác để kiểm chứng. |
| **TC-FR09-32** | **VALID** | Xác thực JSON Schema thành công đầy đủ 5 trường bắt buộc. | Kiểm tra có đủ: `success`, `coupon_id`, `discount_amount`, `final_amount`, `message`. |
| **TC-FR09-33** | **VALID** | Xác thực kiểu dữ liệu của `final_amount` là `number`. | Giữ nguyên. |
| **TC-FR09-34** | **VALID** | Xác thực JSON Schema phản hồi lỗi khi thiếu `code`. | Giữ nguyên. |
| **TC-FR09-35** | **VALID** | Xác thực JSON Schema phản hồi lỗi khi mã hết hạn. | Giữ nguyên. |

---

## 3. Mở rộng (+5 Test Cases nâng cao AI bỏ sót & Giải thích)

| Test Case ID | Mục kiểm thử mở rộng | Input / Kịch bản thực thi | Kết quả mong đợi | Giải thích tại sao AI bỏ sót |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FR09-EXT01** | **Tranh chấp đồng thời khi áp dụng mã 1 lần (Race Condition)** | Gửi cùng lúc 2 request Checkout sử dụng mã `SAVE10` (chỉ cho phép 1 lần dùng) trong cùng 1 mili-giây. | Chỉ có đúng 1 đơn hàng được giảm giá, đơn hàng thứ 2 bị báo lỗi đã hết lượt. | AI chỉ kiểm tra trạng thái tuần tự mà không tính đến lỗ hổng Race Condition khi database chưa kịp cập nhật bảng `coupon_usage` (Thiếu Transaction Lock / Mutex). |
| **TC-FR09-EXT02** | **Hoàn lại lượt sử dụng mã khi đơn hàng bị HỦY** | User dùng mã `SAVE10` (max 1 lần), đặt hàng thành công. Sau đó gọi `PUT /api/orders/:id/cancel` để hủy đơn, rồi thử dùng lại mã `SAVE10`. | Mã giảm giá phải được khôi phục quyền sử dụng cho user. | AI chỉ kiểm tra luồng áp dụng mã độc lập tại `/api/apply-coupon` mà không kết nối với chu trình hủy đơn (Order Cancellation Lifecycle). Thực tế SUT không hề xóa bản ghi trong `coupon_usage` khi hủy đơn! |
| **TC-FR09-EXT03** | **Chống cộng dồn nhiều mã (Coupon Stacking)** | Gửi mảng chứa 2 mã `["SAVE10", "BIGBUY"]` hoặc gọi liên tiếp 2 lần apply coupon trên cùng 1 giỏ hàng. | Hệ thống từ chối hoặc chỉ áp dụng mã có lợi nhất, không cho cộng dồn trái phép. | Đặc tả chỉ định nghĩa nhận vào 1 `code` dạng string đơn lẻ, nên AI không suy luận kịch bản attacker cố tình gửi cấu trúc dữ liệu dạng mảng hoặc lặp để cộng dồn giảm giá. |
| **TC-FR09-EXT04** | **Làm tròn tiền lẻ khi giảm theo phần trăm (Rounding Precision)** | Áp dụng mã giảm 15% trên đơn hàng có tổng tiền lẻ `333.333 ₫` (`discount = 49.999,95 ₫`). | Số tiền giảm phải được làm tròn nguyên vẹn (ví dụ `50.000 ₫` hoặc `49.999 ₫`), không sinh ra số float với nhiều số thập phân lẻ. | AI thường giả định dữ liệu test là các số tròn chục nghìn/trăm nghìn, bỏ qua kiểm thử sai số dấu phẩy động (Floating point precision). |
| **TC-FR09-EXT05** | **Bảo vệ ranh giới giảm giá không vượt quá tổng đơn** | Tạo mã giảm giá cố định `500.000 ₫`, áp dụng cho đơn hàng đúng `500.000 ₫` hoặc có phụ phí. | `final_amount` tối thiểu phải là `0 ₫`, không bao giờ được phép là số âm. | AI ít khi kiểm tra các trường hợp biên tài chính đặc biệt (Extreme boundary logic) dẫn đến việc cửa hàng phải trả ngược tiền cho khách. |
