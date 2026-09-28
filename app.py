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

# Custom CSS cho giao diện doanh nghiệp & cổng đặt tour
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
# 2. KHỞI TẠO DỮ LIỆU DÙNG CHUNG (SESSION STATE)
# ==========================================
@st.cache_data
def get_initial_hotels():
    return [
        {"Mã HS": "H001", "Tên Khách Sạn": "Vinpearl Resort & Spa", "Địa điểm": "Phú Quốc", "Hạng": "5 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 2500000},
        {"Mã HS": "H002", "Tên Khách Sạn": "Vinpearl Discovery VIP", "Địa điểm": "Phú Quốc", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 4800000},
        {"Mã HS": "H003", "Tên Khách Sạn": "Sun World Hotel", "Địa điểm": "Đà Nẵng", "Hạng": "4 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 1200000},
        {"Mã HS": "H004", "Tên Khách Sạn": "Novotel Han River VIP", "Địa điểm": "Đà Nẵng", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 3800000},
        {"Mã HS": "H005", "Tên Khách Sạn": "InterContinental Westlake", "Địa điểm": "Hà Nội", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 5500000},
        {"Mã HS": "H006", "Tên Khách Sạn": "Hôtel de la Coupole MGallery", "Địa điểm": "Sapa", "Hạng": "5 Sao", "Loại phòng": "VIP / Suite", "Giá/Phòng/Đêm": 4900000},
        {"Mã HS": "H007", "Tên Khách Sạn": "Sapa Horizon Hotel", "Địa điểm": "Sapa", "Hạng": "3 Sao", "Loại phòng": "Standard", "Giá/Phòng/Đêm": 850000}
    ]

# Đơn giá tham chiếu tính toán hệ thống (Net cost)
TRANSPORT_RATES = {"Phú Quốc": 1200000, "Đà Nẵng": 1000000, "Hà Nội": 900000, "Sapa": 1500000} # Xe/ngày
GUIDE_RATE = 800000 # HDV/ngày
MEAL_RATES = {"3 Sao": 150000, "4 Sao": 250000, "5 Sao": 450000} # Tiền ăn/người/bữa

if 'df_hotels' not in st.session_state:
    st.session_state.df_hotels = pd.DataFrame(get_initial_hotels())

if 'df_bookings' not in st.session_state:
    # Dữ liệu yêu cầu đặt tour từ khách hàng
    st.session_state.df_bookings = pd.DataFrame([
        {"Mã Đơn": "BK-1001", "Tên Khách": "Anh Minh", "SĐT": "0901234567", "Điểm đến": "Phú Quốc", "Số Khách": 5, "Ngày/Đêm": "4N3Đ", "Khách sạn": "Vinpearl Discovery VIP (5 Sao VIP)", "Tổng Tiền": 52500000, "Trạng thái": "Chờ Giám đốc duyệt", "Ngày đặt": "2026-09-28"},
        {"Mã Đơn": "BK-1002", "Tên Khách": "Chị Hoa (Tập đoàn FPT)", "SĐT": "0912345678", "Điểm đến": "Sapa", "Số Khách": 12, "Ngày/Đêm": "3N2Đ", "Khách sạn": "Hôtel de la Coupole (5 Sao VIP)", "Tổng Tiền": 118000000, "Trạng thái": "Đã chốt & Cọc", "Ngày đặt": "2026-09-27"}
    ])

if 'df_tours' not in st.session_state:
    # Dữ liệu các Tour ghép định kỳ
    st.session_state.df_tours = pd.DataFrame([
        {"ID": "T001", "Tên Tour": "Hà Nội - Sapa - Fanxipan 3N2Đ", "Loại": "Nội địa", "Khởi hành": "2026-10-05", "Trạng thái": "Đã đủ chỗ", "Số chỗ": 25, "Đã đặt": 25, "Doanh thu": 105000000, "Chi phí": 78000000},
        {"ID": "T002", "Tên Tour": "Đà Nẵng - Hội An - Bà Nà 4N3Đ", "Loại": "Nội địa", "Khởi hành": "2026-10-10", "Trạng thái": "Mở bán", "Số chỗ": 30, "Đã đặt": 18, "Doanh thu": 104400000, "Chi phí": 72000000},
        {"ID": "T003", "Tên Tour": "Bangkok - Pattaya (Thái Lan) 5N4Đ", "Loại": "Outbound", "Khởi hành": "2026-10-12", "Trạng thái": "Mở bán", "Số chỗ": 20, "Đã đặt": 15, "Doanh thu": 133500000, "Chi phí": 95000000}
    ])

# ==========================================
# 3. THANH ĐIỀU HƯỚNG CHÍNH (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=65)
    st.title("VIET TRAVEL ENTERPRISE")
    
    # CHUYỂN ĐỔI CHẾ ĐỘ SỬ DỤNG
    app_mode = st.radio(
        "🔀 CHỌN CHẾ ĐỘ SỬ DỤNG:",
        ["🌟 CỔNG ĐẶT TOUR (Dành cho Khách)", "👔 HỆ THỐNG QUẢN TRỊ (Dành cho CEO)"],
        index=0
    )
    
    st.divider()

    if "CEO" in app_mode:
        ceo_menu = st.selectbox(
            "DANH MỤC QUẢN TRỊ:",
            [
                "📊 Dashboard Điều hành CEO",
                "📥 Tiếp nhận & Duyệt Đơn đặt",
                "🏨 Quản lý Khách sạn Partner",
                "🗺️ Quản lý Tour & Vận hành",
                "💰 Báo cáo Tài chính"
            ]
        )

# ==========================================
# 4. KHU VỰC HIỂN THỊ NỘI DUNG CHÍNH
# ==========================================

# ------------------------------------------
# CHẾ ĐỘ 1: CỔNG ĐẶT TOUR CHO KHÁCH HÀNG
# ------------------------------------------
if "Khách" in app_mode:
    st.markdown('<div class="main-title">🏖️ ĐẶT TOUR DU LỊCH THIẾT KẾ THEO YÊU CẦU CỦA BẠN</div>', unsafe_allow_html=True)
    st.caption("Hãy tự do thiết kế chuyến đi hoàn hảo của bạn. Hệ thống sẽ tự động tính toán chi phí minh bạch tức thì!")

    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        st.subheader("1. Thông tin Chuyến đi & Nhu cầu")
        
        col_a, col_b = st.columns(2)
        with col_a:
            destination = st.selectbox("📍 Điểm đến bạn muốn đi", ["Phú Quốc", "Đà Nẵng", "Sapa", "Hà Nội"])
            pax = st.number_input("👥 Số lượng khách (Người)", min_value=1, value=5, step=1)
            days = st.number_input("☀️ Số ngày đi", min_value=1, value=4, step=1)
            nights = st.number_input("🌙 Số đêm ở", min_value=0, value=3, step=1)

        with col_b:
            star_rating = st.selectbox("⭐ Hạng Khách sạn mong muốn", ["5 Sao", "4 Sao", "3 Sao"])
            room_type = st.selectbox("🛏️ Loại phòng", ["VIP / Suite", "Standard"])

            # Lọc khách sạn theo nhu cầu
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
                selected_hotel_name = f"Khách sạn Tiêu chuẩn {star_rating} (Chưa chỉ định)"
                hotel_price_per_night = 4500000 if star_rating == "5 Sao" else (2000000 if star_rating == "4 Sao" else 900000)
                st.info(f"💡 Sử dụng đơn giá tham chiếu {star_rating} cho lựa chọn này.")

        st.subheader("2. Dịch vụ đi kèm chọn thêm")
        ca, cb, cc = st.columns(3)
        with ca:
            inc_car = st.checkbox("Xe riêng đưa đón suốt tuyến", value=True)
        with cb:
            inc_guide = st.checkbox("Hướng dẫn viên chuyên nghiệp", value=True)
        with cc:
            inc_meal = st.checkbox("Bao gồm ăn uống (3 bữa/ngày)", value=True)

    # THUẬT TOÁN TÍNH GIÁ TỰ ĐỘNG
    with c_right:
        st.subheader("3. Báo Giá Chuyến Đi Chi Tiết")
        
        rooms_needed = math.ceil(pax / 2) # 2 người/phòng
        cost_hotel = rooms_needed * hotel_price_per_night * nights
        cost_car = (TRANSPORT_RATES.get(destination, 1000000) * days) if inc_car else 0
        cost_guide = (GUIDE_RATE * days) if inc_guide else 0
        cost_meal = (pax * MEAL_RATES.get(star_rating, 200000) * 2 * days) if inc_meal else 0

        total_cost_net = cost_hotel + cost_car + cost_guide + cost_meal
        # Biên lợi nhuận định mức 20% mặc định cho hệ thống bán lẻ
        selling_price = total_cost_net / 0.8
        price_per_pax = selling_price / pax

        # Hiển thị thẻ Báo Giá
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
            cust_note = st.text_area("Ghi chú thêm (Nếu có)", placeholder="Ví dụ: Yêu cầu ăn chay, có trẻ em...")
            
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
# CHẾ ĐỘ 2: QUẢN TRỊ DÀNH CHO GIÁM ĐỐC
# ------------------------------------------
else:
    if ceo_menu == "📊 Dashboard Điều hành CEO":
        st.markdown('<div class="main-title">👔 EXECUTIVE DASHBOARD - BÁO CÁO BÀN GIÁO QUẢN TRỊ</div>', unsafe_allow_html=True)
        
        df_b = st.session_state.df_bookings
        df_t = st.session_state.df_tours

        # Tổng hợp chỉ số KPI
        total_custom_rev = df_b[df_b["Trạng thái"] != "Hủy đơn"]["Tổng Tiền"].sum()
        total_tour_rev = df_t["Doanh thu"].sum()
        grand_total_rev = total_custom_rev + total_tour_rev
        pending_orders = len(df_b[df_b["Trạng thái"] == "Chờ Giám đốc duyệt"])

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("TỔNG DOANH THU TOÀN CÔNG TY", f"{grand_total_rev:,.0f} VNĐ", delta="+18.5% Tăng trưởng")
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
        st.caption("Danh sách khách hàng đã tự thiết kế tour và ấn nút Đặt Tour trên App.")

        df_b = st.session_state.df_bookings

        # Hiển thị danh sách Đơn đặt
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
                    
                    # Nút duyệt đơn dành cho CEO
                    new_status = st.selectbox("Cập nhật Trạng thái đơn:", ["Chờ Giám đốc duyệt", "Đã chốt & Cọc", "Đã hoàn thành", "Hủy đơn"], key=f"status_{idx}", index=["Chờ Giám đốc duyệt", "Đã chốt & Cọc", "Đã hoàn thành", "Hủy đơn"].index(row["Trạng thái"]))
                    if new_status != row["Trạng thái"]:
                        st.session_state.df_bookings.at[idx, "Trạng thái"] = new_status
                        st.success(f"Đã cập nhật trạng thái đơn {row['Mã Đơn']} thành '{new_status}'!")
                        st.rerun()

    elif ceo_menu == "🏨 Quản lý Khách sạn Partner":
        st.markdown('<div class="main-title">🏨 QUẢN LÝ DANH MỤC KHÁCH SẠN PARTNER</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.df_hotels, use_container_width=True, hide_index=True)
        
        st.subheader("➕ Thêm Khách sạn Partner Mới")
        with st.form("add_hotel_form"):
            h1, h2, h3 = st.columns(3)
            with h1:
                h_name = st.text_input("Tên Khách Sạn")
                h_location = st.selectbox("Địa điểm", ["Phú Quốc", "Đà Nẵng", "Sapa", "Hà Nội", "Nha Trang"])
            with h2:
                h_star = st.selectbox("Hạng Sao", ["5 Sao", "4 Sao", "3 Sao"])
                h_room = st.selectbox("Loại Phòng", ["VIP / Suite", "Standard"])
            with h3:
                h_price = st.number_input("Giá/Phòng/Đêm (VNĐ)", step=100000, value=2000000)
                
            btn_add = st.form_submit_button("Lưu Khách Sạn Mới")
            if btn_add:
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
