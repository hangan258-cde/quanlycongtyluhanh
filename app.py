import streamlit as st
import pandas as pd
from datetime import datetime, date
import math

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN HỆ THỐNG
# ==========================================
st.set_page_config(
    page_title="Viet Travel Enterprise - Platform Điều Hành & Đặt Tour",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện
st.markdown("""
<style>
    .main-title {
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        padding-bottom: 10px;
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 20px;
    }
    .booking-card {
        background-color: #F0FDF4;
        border: 2px solid #16A34A;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO DỮ LIỆU BAN ĐẦU
# ==========================================
@st.cache_data
def get_initial_hotels():
    return [
        # --- PHÚ QUỐC ---
        {"Mã HS": "H001", "Tên Khách Sạn": "Vinpearl Resort & Spa", "Địa điểm": "Phú Quốc", "Hạng": "5 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 2500000},
        {"Mã HS": "H002", "Tên Khách Sạn": "Vinpearl Discovery VIP", "Địa điểm": "Phú Quốc", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 4800000},
        {"Mã HS": "H003", "Tên Khách Sạn": "JW Marriott Phu Quoc Emerald Bay", "Địa điểm": "Phú Quốc", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 8500000},
        {"Mã HS": "H004", "Tên Khách Sạn": "Novotel Phu Quoc Resort", "Địa điểm": "Phú Quốc", "Hạng": "4 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 1800000},
        {"Mã HS": "H005", "Tên Khách Sạn": "Sunset Sanato Resort", "Địa điểm": "Phú Quốc", "Hạng": "3 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 950000},

        # --- ĐÀ NẴNG ---
        {"Mã HS": "H006", "Tên Khách Sạn": "Sun World Hotel", "Địa điểm": "Đà Nẵng", "Hạng": "4 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 1200000},
        {"Mã HS": "H007", "Tên Khách Sạn": "Novotel Han River VIP", "Địa điểm": "Đà Nẵng", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 3800000},
        {"Mã HS": "H008", "Tên Khách Sạn": "InterContinental Danang Sun Peninsula", "Địa điểm": "Đà Nẵng", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 9200000},

        # --- SAPA ---
        {"Mã HS": "H011", "Tên Khách Sạn": "Hôtel de la Coupole MGallery", "Địa điểm": "Sapa", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 4900000},
        {"Mã HS": "H012", "Tên Khách Sạn": "Silk Path Grand Resort Sapa", "Địa điểm": "Sapa", "Hạng": "5 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 2800000},
        {"Mã HS": "H013", "Tên Khách Sạn": "Sapa Horizon Hotel", "Địa điểm": "Sapa", "Hạng": "3 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 850000},

        # --- NHA TRANG ---
        {"Mã HS": "H015", "Tên Khách Sạn": "Vinpearl Resort Nha Trang", "Địa điểm": "Nha Trang", "Hạng": "5 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 2600000},
        {"Mã HS": "H016", "Tên Khách Sạn": "Amiana Resort Nha Trang", "Địa điểm": "Nha Trang", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 5200000},

        # --- ĐÀ LẠT ---
        {"Mã HS": "H019", "Tên Khách Sạn": "Dalat Palace Heritage Hotel", "Địa điểm": "Đà Lạt", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 4200000},
        {"Mã HS": "H021", "Tên Khách Sạn": "Terracotta Hotel & Resort", "Địa điểm": "Đà Lạt", "Hạng": "4 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 1500000},

        # --- HẠ LONG ---
        {"Mã HS": "H024", "Tên Khách Sạn": "Vinpearl Resort & Spa Hạ Long", "Địa điểm": "Hạ Long", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 4500000},
        {"Mã HS": "H025", "Tên Khách Sạn": "FLC Grand Hotel Hạ Long", "Địa điểm": "Hạ Long", "Hạng": "5 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 2200000},

        # --- HÀ NỘI ---
        {"Mã HS": "H028", "Tên Khách Sạn": "InterContinental Westlake", "Địa điểm": "Hà Nội", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 5500000},

        # --- QUY NHƠN ---
        {"Mã HS": "H031", "Tên Khách Sạn": "Anantara Quy Nhon Villas", "Địa điểm": "Quy Nhơn", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 9800000},

        # --- TP. HỒ CHÍ MINH ---
        {"Mã HS": "H034", "Tên Khách Sạn": "The Reverie Saigon", "Địa điểm": "TP. Hồ Chí Minh", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 7500000}
    ]

# Dữ liệu lịch trình mẫu cho Chatbot tư vấn
ITINERARY_DATABASE = {
    "sapa": """
🗓️ **Lịch trình gợi ý Sapa (3 Ngày 2 Đêm):**
- **Ngày 1:** Đến Sapa -> Check-in khách sạn -> Tham quan Bản Cát Cát, tìm hiểu văn hóa H'Mông -> Tối dạo Chợ đêm, thưởng thức đồ nướng.
- **Ngày 2:** Chinh phục Đỉnh Fansipan bằng cáp treo -> Chiều check-in Moana Sapa / Cầu kính Rồng Mây -> Tối tắm lá thuốc người Dao đỏ.
- **Ngày 3:** Thăm Thung lũng Mường Hoa / Đèo Ô Quy Hồ -> Mua đặc sản (thịt trâu gác bếp, hạt dổi) -> Khởi hành về.
    """,
    "phú quốc": """
🗓️ **Lịch trình gợi ý Phú Quốc (4 Ngày 3 Đêm):**
- **Ngày 1:** Đón sân bay -> Check-in resort -> Chiều ngắm hoàng hôn tại Sunset Sanato / Grand World -> Tối khám phá Chợ đêm Phú Quốc.
- **Ngày 2:** Tour 4 Đảo (Hòn Mây Rút, Hòn Móng Tay...) -> Lặn ngắm san hô -> Trải nghiệm Cáp treo Hòn Thơm dài nhất thế giới.
- **Ngày 3:** Khám phá VinWonders & Vinpearl Safari -> Tối xem show diễn triệu đô Grand World (Sắc Màu Venices).
- **Ngày 4:** Mua sắm đặc sản (Hạt tiêu, Rượu sim, Nước mắm) -> Tự do tắm biển -> Ra sân bay.
    """,
    "đà nẵng": """
🗓️ **Lịch trình gợi ý Đà Nẵng - Hội An (3 Ngày 2 Đêm):**
- **Ngày 1:** Đón khách Đà Nẵng -> Bán đảo Sơn Trà (Chùa Linh Ứng) -> Chiều di chuyển Phố cổ Hội An, thả hoa đăng -> Tối về Đà Nẵng.
- **Ngày 2:** Vui chơi trọn ngày tại Sun World Bà Nà Hills (Check-in Cầu Vàng, Làng Pháp) -> Tối ngắm Cầu Rồng phun lửa/nước.
- **Ngày 3:** Tham quan Danh thắng Ngũ Hành Sơn -> Mua sắm Chợ Hàn -> Tiễn sân bay.
    """,
    "đà lạt": """
🗓️ **Lịch trình gợi ý Đà Lạt (3 Ngày 2 Đêm):**
- **Ngày 1:** Check-in Quảng trường Lâm Viên, Hồ Xuân Hương -> Tham quan Dinh I / Dinh III -> Tối dạo Chợ Âm Phủ thưởng thức bánh tráng nướng.
- **Ngày 2:** Săn mây đồi Cầu Đất -> Tham quan Chùa Ve Chai (Linh Phước) -> Chiều check-in Thung lũng Tình Yêu / Mongo Land -> Tối nghe nhạc acoustic.
- **Ngày 3:** Langbiang -> Thác Datanla (chơi xe trượt) -> Mua mứt đặc sản Đà Lạt -> Về lại.
    """,
    "hạ long": """
🗓️ **Lịch trình gợi ý Hạ Long (2 Ngày 1 Đêm):**
- **Ngày 1:** Lên du thuyền thăm Vịnh Hạ Long (Động Thiên Cung, Hang Đầu Gỗ, Hòn Gà Chọi) -> Ăn trưa hải sản trên tàu -> Check-in khách sạn -> Tối quẩy tại Sun World Park.
- **Ngày 2:** Tắm biển Bãi Cháy -> Mua chả mực Hạ Long -> Trả phòng về.
    """,
    "nha trang": """
🗓️ **Lịch trình gợi ý Nha Trang (3 Ngày 2 Đêm):**
- **Ngày 1:** Đón khách -> Tháp Bà Ponagar -> Chùa Long Sơn -> Chiều tắm biển Trần Phú -> Tối ăn hải sản.
- **Ngày 2:** Vui chơi trọn gói tại VinWonders Hòn Tre (Cáp treo vượt biển, công viên nước, show Tata) -> Tối dạo chợ đêm.
- **Ngày 3:** Tour lặn biển Hòn Mun / Đảo Yến -> Mua yến sào, nem nướng -> Tiễn khách.
    """
}

# Đơn giá tham chiếu vận chuyển
TRANSPORT_RATES = {
    "Phú Quốc": 1200000, "Đà Nẵng": 1000000, "Hà Nội": 900000, "Sapa": 1500000,
    "Nha Trang": 1100000, "Đà Lạt": 1300000, "Hạ Long": 1200000, "Quy Nhơn": 1200000, "TP. Hồ Chí Minh": 1000000
}
GUIDE_RATE = 800000  # HDV/ngày
MEAL_RATES = {"3 Sao": 150000, "4 Sao": 250000, "5 Sao": 450000}  # Tiền ăn/người/bữa

# Khởi tạo session states
if 'df_hotels' not in st.session_state:
    st.session_state.df_hotels = pd.DataFrame(get_initial_hotels())

if 'df_bookings' not in st.session_state:
    st.session_state.df_bookings = pd.DataFrame([
        {"Mã Đơn": "BK-1001", "Tên Khách": "Anh Minh", "SĐT": "0901234567", "Điểm đến": "Phú Quốc", "Số Khách": 5, "Ngày/Đêm": "4N3Đ", "Khách sạn": "Vinpearl Discovery VIP (5 Sao VIP)", "Tổng Tiền": 52500000, "Trạng thái": "Chờ Giám đốc duyệt", "Ngày đặt": "2026-09-28"},
        {"Mã Đơn": "BK-1002", "Tên Khách": "Chị Hoa (Tập đoàn FPT)", "SĐT": "0912345678", "Điểm đến": "Sapa", "Số Khách": 12, "Ngày/Đêm": "3N2Đ", "Khách sạn": "Hôtel de la Coupole (5 Sao VIP)", "Tổng Tiền": 118000000, "Trạng thái": "Đã chốt & Cọc", "Ngày đặt": "2026-09-27"}
    ])

if 'df_tours' not in st.session_state:
    st.session_state.df_tours = pd.DataFrame([
        {"ID": "T001", "Tên Tour": "Hà Nội - Sapa - Fansipan 3N2Đ", "Loại": "Nội địa", "Khởi hành": "2026-10-05", "Trạng thái": "Đã đủ chỗ", "Số chỗ": 25, "Đã đặt": 25, "Doanh thu": 105000000, "Chi phí": 78000000},
        {"ID": "T002", "Tên Tour": "Đà Nẵng - Hội An - Bà Nà 4N3Đ", "Loại": "Nội địa", "Khởi hành": "2026-10-10", "Trạng thái": "Mở bán", "Số chỗ": 30, "Đã đặt": 18, "Doanh thu": 104400000, "Chi phí": 72000000}
    ])

# Khởi tạo dữ liệu Quản lý Nhân sự & HDV
if 'df_staff' not in st.session_state:
    st.session_state.df_staff = pd.DataFrame([
        {"Mã NV": "HDV-01", "Họ và Tên": "Nguyễn Văn Tuấn", "Chức danh": "HDV Quốc tế", "SĐT": "0908112233", "Thẻ HDV": "Nội địa & Quốc tế", "Tuyến đường chính": "Sapa, Hà Nội, Hạ Long", "Ngoại ngữ": "Tiếng Anh, Tiếng Trung", "Trạng thái": "Sẵn sàng nhận tour"},
        {"Mã NV": "HDV-02", "Họ và Tên": "Lê Thị Mai", "Chức danh": "HDV Nội địa", "SĐT": "0918334455", "Thẻ HDV": "Nội địa", "Tuyến đường chính": "Đà Nẵng, Hội An, Huế", "Ngoại ngữ": "Tiếng Anh", "Trạng thái": "Đang đi tour (T001)"},
        {"Mã NV": "HDV-03", "Họ và Tên": "Trần Hoàng Nam", "Chức danh": "HDV Quốc tế", "SĐT": "0938556677", "Thẻ HDV": "Nội địa & Quốc tế", "Tuyến đường chính": "Phú Quốc, Nha Trang, Đà Lạt", "Ngoại ngữ": "Tiếng Anh, Tiếng Hàn", "Trạng thái": "Sẵn sàng nhận tour"},
        {"Mã NV": "DH-01", "Họ và Tên": "Phạm Quốc Bảo", "Chức danh": "Chuyên viên Điều hành Tour", "SĐT": "0977889900", "Thẻ HDV": "Không", "Tuyến đường chính": "Toàn quốc", "Ngoại ngữ": "Tiếng Anh", "Trạng thái": "Đang làm việc"}
    ])

# Khởi tạo lịch sử Chatbot
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Xin chào! Tôi là Trợ lý ảo tư vấn tour Viet Travel 🤖.\n\nBạn muốn tìm hiểu lịch trình du lịch ở đâu (Sapa, Phú Quốc, Đà Nẵng, Đà Lạt, Hạ Long, Nha Trang...) hoặc có thắc mắc gì về dịch vụ không ạ?"}
    ]

# ==========================================
# 3. THANH ĐIỀU HƯỚNG CHÍNH (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=65)
    st.title("VIET TRAVEL ENTERPRISE")

    app_mode = st.radio(
        "🔀 CHỌN CHẾ ĐỘ SỬ DỤNG:",
        ["🌟 CỔNG ĐẶT TOUR (Dành cho Khách)", "💬 CHATBOT TƯ VẤN LỊCH TRÌNH", "👔 HỆ THỐNG QUẢN TRỊ (Dành cho CEO)"],
        index=0
    )

    st.divider()

    if "CEO" in app_mode:
        ceo_menu = st.selectbox(
            "DANH MỤC QUẢN TRỊ:",
            [
                "📊 Dashboard Điều hành CEO",
                "📥 Tiếp nhận & Duyệt Đơn đặt",
                "👨‍💼 Quản lý Nhân sự & HDV",
                "🏨 Quản lý Khách sạn Partner",
                "🗺️ Quản lý Tour & Vận hành",
                "💰 Báo cáo Tài chính"
            ]
        )

# ==========================================
# 4. KHU VỰC HIỂN THỊ NỘI DUNG CHÍNH
# ==========================================

# ------------------------------------------
# CHẾ ĐỘ 1: CỔNG ĐẶT TOUR
# ------------------------------------------
if "CỔNG ĐẶT TOUR" in app_mode:
    st.markdown('<div class="main-title">🏖️ ĐẶT TOUR DU LỊCH THIẾT KẾ THEO YÊU CẦU CỦA BẠN</div>', unsafe_allow_html=True)
    st.caption("Hãy tự do thiết kế chuyến đi hoàn hảo của bạn. Hệ thống sẽ tự động tính toán chi phí minh bạch tức thì!")

    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        st.subheader("1. Thông tin Chuyến đi & Nhu cầu")

        available_locations = sorted(list(st.session_state.df_hotels["Địa điểm"].unique()))

        col_a, col_b = st.columns(2)
        with col_a:
            destination = st.selectbox("📍 Điểm đến bạn muốn đi", available_locations)
            pax = st.number_input("👥 Số lượng khách (Người)", min_value=1, value=4, step=1)
            days = st.number_input("☀️ Số ngày đi", min_value=1, value=3, step=1)
            nights = st.number_input("🌙 Số đêm ở", min_value=0, value=2, step=1)

        with col_b:
            star_rating = st.selectbox("⭐ Hạng Khách sạn mong muốn", ["5 Sao", "4 Sao", "3 Sao"])
            room_type = st.selectbox("🛏️ Loại phòng", ["Standard", "VIP / Suite"])

            hotels_df = st.session_state.df_hotels
            matched_hotels = hotels_df[
                (hotels_df["Địa điểm"] == destination) & 
                (hotels_df["Hạng"] == star_rating) & 
                (hotels_df["Loại phòng"] == room_type)
            ]

            if not matched_hotels.empty:
                selected_hotel_name = st.selectbox("🏨 Khách sạn gợi ý phù hợp nhất", matched_hotels["Tên Khách Sạn"].unique())
                hotel_price_per_night = matched_hotels[matched_hotels["Tên Khách Sạn"] == selected_hotel_name]["Giá/Phòng/Đêm"].values[0]
            else:
                selected_hotel_name = f"Khách sạn Tiêu chuẩn {star_rating} (Tham chiếu)"
                hotel_price_per_night = 4500000 if star_rating == "5 Sao" else (2000000 if star_rating == "4 Sao" else 900000)
                st.info(f"💡 Chưa có Partner cụ thể cho tùy chọn này. Sử dụng đơn giá tham chiếu {star_rating}.")

        st.subheader("2. Dịch vụ đi kèm chọn thêm")
        ca, cb, cc = st.columns(3)
        with ca:
            inc_car = st.checkbox("Xe riêng đưa đón suốt tuyến", value=True)
        with cb:
            inc_guide = st.checkbox("Hướng dẫn viên chuyên nghiệp", value=True)
        with cc:
            inc_meal = st.checkbox("Bao gồm ăn uống (3 bữa/ngày)", value=True)

    with c_right:
        st.subheader("3. Báo Giá Chuyến Đi Chi Tiết")

        rooms_needed = math.ceil(pax / 2)
        cost_hotel = rooms_needed * hotel_price_per_night * nights
        cost_car = (TRANSPORT_RATES.get(destination, 1100000) * days) if inc_car else 0
        cost_guide = (GUIDE_RATE * days) if inc_guide else 0
        cost_meal = (pax * MEAL_RATES.get(star_rating, 200000) * 2 * days) if inc_meal else 0

        total_cost_net = cost_hotel + cost_car + cost_guide + cost_meal
        selling_price = total_cost_net / 0.8
        price_per_pax = selling_price / pax

        st.markdown(f"""
        <div class="booking-card">
            <h3 style="color: #15803D; margin:0;">TỔNG CHI PHÍ TRỌN GÓI</h3>
            <h1 style="color: #16A34A; margin: 10px 0;">{selling_price:,.0f} VNĐ</h1>
            <p style="font-size: 18px; color: #1E3A8A; margin:0;"><b>Đơn giá/Khách:</b> <span style="color: #B91C1C;">{price_per_pax:,.0f} VNĐ</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("**Bóc tách hạng mục chi phí đã bao gồm:**")
        st.write(f"- 🛏️ **Khách sạn:** {rooms_needed} phòng {room_type} ({selected_hotel_name}) x {nights} đêm.")
        st.write(f"- 🚗 **Di chuyển:** Xe đưa đón riêng tại {destination} ({days} ngày).")
        st.write(f"- 👨‍💼 **Phục vụ:** Hướng dẫn viên suốt tuyến ({days} ngày).")
        st.write(f"- 🍽️ **Ẩm thực:** {days*2} bữa ăn chính theo tiêu chuẩn {star_rating}.")

        st.divider()
        st.subheader("📝 Xác Nhận Đặt Tour")
        with st.form("customer_booking_form"):
            cust_name = st.text_input("Họ và Tên người đặt*", placeholder="Nhập họ tên...")
            cust_phone = st.text_input("Số điện thoại liên hệ*", placeholder="Nhập SĐT...")
            cust_note = st.text_area("Ghi chú thêm (Nếu có)", placeholder="Ví dụ: Yêu cầu phòng tầng cao, hướng biển...")

            btn_submit = st.form_submit_button("🚀 ĐẶT TOUR NGAY")
            if btn_submit:
                if not cust_name or not cust_phone:
                    st.error("Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")
                else:
                    new_booking = {
                        "Mã Đơn": f"BK-{1001 + len(st.session_state.df_bookings)}",
                        "Tên Khách": cust_name,
                        "SĐT": cust_phone,
                        "Điểm đến": destination,
                        "Số Khách": pax,
                        "Ngày/Đêm": f"{days}N{nights}Đ",
                        "Khách sạn": f"{selected_hotel_name} ({star_rating} {room_type})",
                        "Tổng Tiền": selling_price,
                        "Trạng thái": "Chờ Giám đốc duyệt",
                        "Ngày đặt": str(date.today())
                    }
                    st.session_state.df_bookings = pd.concat([st.session_state.df_bookings, pd.DataFrame([new_booking])], ignore_index=True)
                    st.balloons()
                    st.success("🎉 Đặt tour thành công! Đội ngũ Điều hành sẽ liên hệ xác nhận trong vòng 15 phút.")

# ------------------------------------------
# CHẾ ĐỘ 2: CHATBOT TƯ VẤN LỊCH TRÌNH
# ------------------------------------------
elif "CHATBOT" in app_mode:
    st.markdown('<div class="main-title">💬 CHATBOT HỎI ĐÁP & TƯ VẤN LỊCH TRÌNH DU LỊCH</div>', unsafe_allow_html=True)
    st.caption("Trợ lý AI sẵn sàng giải đáp thắc mắc về địa điểm, lịch trình chi tiết và chi phí dự kiến 24/7.")

    st.write("💡 **Gợi ý câu hỏi nhanh:**")
    quick_cols = st.columns(4)
    quick_q = None
    if quick_cols[0].button("📍 Lịch trình Sapa"):
        quick_q = "Gợi ý lịch trình tour Sapa"
    if quick_cols[1].button("🏖️ Lịch trình Phú Quốc"):
        quick_q = "Cho tôi lịch trình đi Phú Quốc"
    if quick_cols[2].button("🌉 Lịch trình Đà Nẵng"):
        quick_q = "Tư vấn tour Đà Nẵng"
    if quick_cols[3].button("🌲 Lịch trình Đà Lạt"):
        quick_q = "Lịch trình đi Đà Lạt thế nào?"

    st.divider()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Nhập thắc mắc của bạn về lịch trình tour tại đây...")
    prompt = user_input or quick_q

    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        prompt_lower = prompt.lower()
        response = ""

        found_destination = False
        for loc_key, itinerary in ITINERARY_DATABASE.items():
            if loc_key in prompt_lower:
                response = f"Dưới đây là gợi ý lịch trình chi tiết cho chuyến đi **{loc_key.upper()}** của bạn:\n" + itinerary
                response += "\n\n👉 Bạn có thể chuyển sang tab **'CỔNG ĐẶT TOUR'** ở thanh bên trái để tự chọn số người, số ngày và nhận báo giá trọn gói tự động nhé!"
                found_destination = True
                break

        if not found_destination:
            if "giá" in prompt_lower or "chi phí" in prompt_lower or "tiền" in prompt_lower:
                response = """
💰 **Thông tin chi phí Tour:**
- Giá tour được tự động tính toán dựa trên: **Số lượng người**, **Số ngày đêm**, **Hạng khách sạn (3-5 sao)** và **Các dịch vụ chọn thêm** (Xe đưa đón, HDV, Ăn uống).
- Báo giá minh bạch bao gồm chi phí Net và ưu đãi định mức.
- Bạn vui lòng vào tab **'CỔNG ĐẶT TOUR'** chọn các tùy chọn để xem bảng giá chính xác nhất!
                """
            elif "khách sạn" in prompt_lower or "phòng" in prompt_lower:
                response = "🏨 Viet Travel hợp tác với hơn 30+ hệ thống khách sạn/resort hàng đầu Việt Nam như Vinpearl, InterContinental, Novotel, Silk Path, FLC... từ 3 sao đến 5 sao VIP."
            elif "xin chào" in prompt_lower or "chào" in prompt_lower or "hi" in prompt_lower:
                response = "Xin chào bạn! Tôi có thể giúp gì cho chuyến du lịch sắp tới của bạn? Bạn muốn tham khảo lịch trình Sapa, Phú Quốc, Đà Nẵng, Đà Lạt hay địa điểm nào khác?"
            else:
                response = f"""
Cảm ơn bạn đã đặt câu hỏi: *"{prompt}"*.

Dưới đây là một số địa điểm nổi tiếng Viet Travel có sẵn lịch trình chi tiết:
- 🏔️ **Sapa** (3N2Đ - Cáp treo Fansipan, Bản Cát Cát)
- 🏖️ **Phú Quốc** (4N3Đ - Tour 4 Đảo, VinWonders, Safari)
- 🌉 **Đà Nẵng** (3N2Đ - Bà Nà Hills, Hội An)
- 🌲 **Đà Lạt** (3N2Đ - Quảng trường Lâm Viên, Langbiang)
- 🚢 **Hạ Long** (2N1Đ - Du thuyền Vịnh Hạ Long)
- 🏖️ **Nha Trang** (3N2Đ - VinWonders, Tour Đảo)

Bạn hãy nhập tên địa điểm muốn đi để tôi gửi lịch trình gợi ý nhé!
                """

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# ------------------------------------------
# CHẾ ĐỘ 3: QUẢN TRỊ CEO
# ------------------------------------------
else:
    if ceo_menu == "📊 Dashboard Điều hành CEO":
        st.markdown('<div class="main-title">👔 EXECUTIVE DASHBOARD - BÁO CÁO BÀN GIÁO QUẢN TRỊ</div>', unsafe_allow_html=True)

        df_b = st.session_state.df_bookings
        df_t = st.session_state.df_tours

        total_custom_rev = df_b[df_b["Trạng thái"] != "Hủy đơn"]["Tổng Tiền"].sum()
        total_tour_rev = df_t["Doanh thu"].sum()
        grand_total_rev = total_custom_rev + total_tour_rev
        pending_orders = len(df_b[df_b["Trạng thái"] == "Chờ Giám đốc duyệt"])

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("TỔNG DOANH THU TOÀN CÔNG TY", f"{grand_total_rev:,.0f} VNĐ", delta="+22.4% Tăng trưởng")
        k2.metric("Doanh thu Tour Khách Tự Thiết Kế", f"{total_custom_rev:,.0f} VNĐ", delta=f"{len(df_b)} Đơn hàng")
        k3.metric("Doanh thu Tour Ghép Định Kỳ", f"{total_tour_rev:,.0f} VNĐ", delta=f"{len(df_t)} Tour đang chạy")
        k4.metric("ĐƠN ĐẶT TOUR CHỜ DUYỆT", f"{pending_orders} Đơn", delta="Cần xử lý ngay" if pending_orders > 0 else "Đã xong", delta_color="inverse")

        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📈 Doanh thu theo Điểm đến (Tour Thiết Kế)")
            chart_data_dest = df_b.groupby("Điểm đến")["Tổng Tiền"].sum()
            st.bar_chart(chart_data_dest)

        with c2:
            st.subheader("📊 So sánh Doanh thu vs Chi phí các Tour")
            chart_data_tour = df_t.set_index("ID")[["Doanh thu", "Chi phí"]]
            st.bar_chart(chart_data_tour)

    elif ceo_menu == "📥 Tiếp nhận & Duyệt Đơn đặt":
        st.markdown('<div class="main-title">📥 QUẢN LÝ & DUYỆT YÊU CẦU ĐẶT TOUR TỪ KHÁCH HÀNG</div>', unsafe_allow_html=True)
        df_b = st.session_state.df_bookings

        for idx, row in df_b.iterrows():
            with st.expander(f"📌 Mã đơn: **{row['Mã Đơn']}** | Khách: **{row['Tên Khách']}** ({row['SĐT']}) - **{row['Điểm đến']}** ({row['Ngày/Đêm']}) - **{row['Trạng thái']}**"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"- **Điểm đến:** {row['Điểm đến']}")
                    st.write(f"- **Số lượng khách:** {row['Số Khách']} người")
                    st.write(f"- **Thời gian:** {row['Ngày/Đêm']}")
                    st.write(f"- **Khách sạn yêu cầu:** {row['Khách sạn']}")
                with col2:
                    st.write(f"- **Tổng giá trị đơn:** {row['Tổng Tiền']:,.0f} VNĐ")
                    st.write(f"- **Ngày đặt:** {row['Ngày đặt']}")

                    new_status = st.selectbox(
                        "Cập nhật Trạng thái đơn:",
                        ["Chờ Giám đốc duyệt", "Đã chốt & Cọc", "Đã hoàn thành", "Hủy đơn"],
                        key=f"status_{idx}",
                        index=["Chờ Giám đốc duyệt", "Đã chốt & Cọc", "Đã hoàn thành", "Hủy đơn"].index(row["Trạng thái"])
                    )
                    if new_status != row["Trạng thái"]:
                        st.session_state.df_bookings.at[idx, "Trạng thái"] = new_status
                        st.success(f"Đã cập nhật trạng thái đơn {row['Mã Đơn']} thành '{new_status}'!")
                        st.rerun()

    elif ceo_menu == "👨‍💼 Quản lý Nhân sự & HDV":
        st.markdown('<div class="main-title">👨‍💼 QUẢN LÝ DANH SÁCH NHÂN SỰ & HƯỚNG DẪN VIÊN</div>', unsafe_allow_html=True)

        # Thống kê nhanh
        df_s = st.session_state.df_staff
        c_hdv1, c_hdv2, c_hdv3 = st.columns(3)
        c_hdv1.metric("TỔNG NHÂN SỰ/HDV", f"{len(df_s)} Người")
        c_hdv2.metric("HDV Sẵn Sàng Đi Tour", f"{len(df_s[df_s['Trạng thái'] == 'Sẵn sàng nhận tour'])} HDV")
        c_hdv3.metric("HDV Đang Bận Tour", f"{len(df_s[df_s['Trạng thái'].str.contains('Đang đi tour')])} HDV")

        st.divider()

        # Bộ lọc nhân sự
        flt_col1, flt_col2 = st.columns(2)
        with flt_col1:
            role_filter = st.multiselect("Lọc theo Chức danh", options=df_s["Chức danh"].unique(), default=df_s["Chức danh"].unique())
        with flt_col2:
            status_filter = st.multiselect("Lọc theo Trạng thái", options=df_s["Trạng thái"].unique(), default=df_s["Trạng thái"].unique())

        filtered_staff = df_s[(df_s["Chức danh"].isin(role_filter)) & (df_s["Trạng thái"].isin(status_filter))]

        st.dataframe(filtered_staff, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("➕ Thêm Nhân Sự / Hướng Dẫn Viên Mới")
        with st.form("add_staff_form"):
            s1, s2, s3 = st.columns(3)
            with s1:
                st_name = st.text_input("Họ và Tên*")
                st_phone = st.text_input("Số điện thoại*")
                st_role = st.selectbox("Chức danh*", ["HDV Quốc tế", "HDV Nội địa", "Chuyên viên Điều hành Tour", "NV Kinh doanh"])
            with s2:
                st_card = st.selectbox("Thẻ HDV", ["Nội địa & Quốc tế", "Nội địa", "Không"])
                st_routes = st.text_input("Tuyến đường chính / Khu vực", placeholder="Ví dụ: Phú Quốc, Nha Trang")
            with s3:
                st_lang = st.text_input("Ngoại ngữ", value="Tiếng Anh")
                st_status = st.selectbox("Trạng thái", ["Sẵn sàng nhận tour", "Đang đi tour", "Đang làm việc", "Nghỉ phép"])

            btn_add_staff = st.form_submit_button("💾 Lưu Nhân Sự Mới")
            if btn_add_staff:
                if not st_name or not st_phone:
                    st.error("Vui lòng điền đầy đủ Họ tên và Số điện thoại!")
                else:
                    new_staff = {
                        "Mã NV": f"NV-0{len(st.session_state.df_staff)+1}",
                        "Họ và Tên": st_name,
                        "Chức danh": st_role,
                        "SĐT": st_phone,
                        "Thẻ HDV": st_card,
                        "Tuyến đường chính": st_routes if st_routes else "Chưa phân công",
                        "Ngoại ngữ": st_lang,
                        "Trạng thái": st_status
                    }
                    st.session_state.df_staff = pd.concat([st.session_state.df_staff, pd.DataFrame([new_staff])], ignore_index=True)
                    st.success(f"🎉 Đã thêm nhân sự {st_name} vào hệ thống quản lý thành công!")
                    st.rerun()

    elif ceo_menu == "🏨 Quản lý Khách sạn Partner":
        st.markdown('<div class="main-title">🏨 QUẢN LÝ DANH MỤC KHÁCH SẠN PARTNER</div>', unsafe_allow_html=True)

        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            loc_filter = st.multiselect("Lọc theo Địa điểm", options=st.session_state.df_hotels["Địa điểm"].unique(), default=st.session_state.df_hotels["Địa điểm"].unique())
        with col_filter2:
            star_filter = st.multiselect("Lọc theo Hạng sao", options=["5 Sao", "4 Sao", "3 Sao"], default=["5 Sao", "4 Sao", "3 Sao"])

        filtered_df = st.session_state.df_hotels[
            (st.session_state.df_hotels["Địa điểm"].isin(loc_filter)) &
            (st.session_state.df_hotels["Hạng"].isin(star_filter))
        ]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        st.subheader("➕ Thêm Khách sạn Partner Mới")
        with st.form("add_hotel_form"):
            h1, h2, h3 = st.columns(3)
            with h1:
                h_name = st.text_input("Tên Khách Sạn")
                h_location = st.text_input("Địa điểm (Tỉnh/Thành phố)", value="Phú Quốc")
            with h2:
                h_star = st.selectbox("Hạng Sao", ["5 Sao", "4 Sao", "3 Sao"])
                h_room = st.selectbox("Loại Phòng", ["Standard", "VIP / Suite"])
            with h3:
                h_price = st.number_input("Giá/Phòng/Đêm (VNĐ)", step=100000, value=2000000)

            btn_add = st.form_submit_button("Lưu Khách Sạn Mới")
            if btn_add:
                if h_name:
                    new_h = {
                        "Mã HS": f"H00{len(st.session_state.df_hotels)+1}",
                        "Tên Khách Sạn": h_name,
                        "Địa điểm": h_location,
                        "Hạng": h_star,
                        "Loại phòng": h_room,
                        "Giá/Phòng/Đêm": h_price
                    }
                    st.session_state.df_hotels = pd.concat([st.session_state.df_hotels, pd.DataFrame([new_h])], ignore_index=True)
                    st.success(f"Đã thêm khách sạn {h_name} vào hệ thống thành công!")
                    st.rerun()

    elif ceo_menu == "🗺️ Quản lý Tour & Vận hành":
        st.markdown('<div class="main-title">🗺️ QUẢN LÝ VẬN HÀNH TOUR GHÉP ĐỊNH KỲ</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.df_tours, use_container_width=True, hide_index=True)

    elif ceo_menu == "💰 Báo cáo Tài chính":
        st.markdown('<div class="main-title">💰 BÁO CÁO TÀI CHÍNH & LỢI NHUẬN RÒNG</div>', unsafe_allow_html=True)
        st.info("Hệ thống tự động đồng bộ doanh thu từ Đơn đặt của Khách và Tour ghép để tính lợi nhuận ròng.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Viet Travel Enterprise Management Platform")
