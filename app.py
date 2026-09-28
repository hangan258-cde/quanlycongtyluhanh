import streamlit as st

# Config trang Streamlit
st.set_page_config(
    page_title="Quản lý Tour Lữ Hành", page_icon="✈️", layout="wide"
)


# -------------------------------------------------------------------
# 1. CÁC LỚP LOGIC NGHIỆP VỤ (CLASSES)
# -------------------------------------------------------------------
class DichVuBoSung:

    def __init__(self, ten_dich_vu: str, gia_goc: float):
        self.ten_dich_vu = ten_dich_vu
        self.gia_goc = gia_goc


class ThongTinThangBay:

    def __init__(self, hang_hang_khong: str, hang_ve: str, gia_ve: float):
        self.hang_hang_khong = hang_hang_khong
        self.hang_ve = hang_ve
        self.gia_ve = gia_ve


class KhachHangTour:

    def __init__(
        self,
        ho_ten: str,
        tuoi: int,
        thang_di: int,
        thong_tin_bay: ThongTinThangBay = None,
    ):
        self.ho_ten = ho_ten
        self.tuoi = tuoi
        self.thang_di = thang_di
        self.thong_tin_bay = thong_tin_bay
        self.dich_vu_them = []

    def them_dich_vu(self, dich_vu: DichVuBoSung):
        self.dich_vu_them.append(dich_vu)

    @property
    def la_mua_cao_diem(self) -> bool:
        # Mùa cao điểm: Tháng 1, 6, 7, 8, 12
        mua_cao_diem = [1, 6, 7, 8, 12]
        return self.thang_di in mua_cao_diem

    def tinh_gia_dich_vu_khach(self, gia_dich_vu_co_ban: float) -> dict:
        if self.tuoi < 5:
            he_so = 0.0
            ghi_chu = "Trẻ em dưới 5 tuổi: Miễn phí dịch vụ"
        elif 5 <= self.tuoi < 12:
            he_so = 0.5
            ghi_chu = "Trẻ em 5-11 tuổi: 50% giá dịch vụ (Không giường riêng)"
        else:
            he_so = 1.0
            ghi_chu = "Người lớn (Từ 12 tuổi trở lên): 100% giá dịch vụ"

        phi_dich_vu_tour = gia_dich_vu_co_ban * he_so
        return {"phi_tour": phi_dich_vu_tour, "ghi_chu": ghi_chu, "he_so": he_so}

    def tinh_gia_phong_khach_san(self, gia_phong_tieu_chuan: float) -> float:
        # Mùa cao điểm phụ thu 30%
        if self.la_mua_cao_diem:
            return gia_phong_tieu_chuan * 1.3
        return gia_phong_tieu_chuan


# -------------------------------------------------------------------
# 2. GIAO DIỆN STREAMLIT (UI)
# -------------------------------------------------------------------
st.title("✈️ Hệ Thống Quản Lý & Tính Giá Tour Du Lịch")
st.write(
    "Nhập thông tin khách hàng, chuyến bay và dịch vụ để tính tổng chi phí."
)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📋 Nhập thông tin Tour & Khách hàng")

    # Thông tin cơ bản khách hàng
    ho_ten = st.text_input("Họ và tên khách hàng", value="Nguyễn Văn A")
    tuoi = st.number_input(
        "Độ tuổi", min_value=0, max_value=120, value=25, step=1
    )
    thang_di = st.slider("Tháng khởi hành", min_value=1, max_value=12, value=7)

    # Thông tin giá tiêu chuẩn Tour
    st.subheader("💵 Đơn giá tiêu chuẩn")
    gia_tour_co_ban = st.number_input(
        "Giá tour cơ bản (VNĐ/người)",
        value=5000000,
        step=100000,
        format="%d",
    )
    gia_phong_tieu_chuan = st.number_input(
        "Giá phòng khách sạn cơ bản (VNĐ/đêm)",
        value=1500000,
        step=100000,
        format="%d",
    )

    # Thông tin chuyến bay
    st.subheader("🛫 Hãng & Hạng máy bay")
    hang_bay = st.selectbox(
        "Hãng hàng không",
        ["Vietnam Airlines", "Vietjet Air", "Bamboo Airways", "Vietravel Airlines"],
    )
    hang_ve = st.selectbox("Hạng vé", ["Phổ thông", "Thương gia", "Phổ thông đặc biệt"])
    gia_ve_bay = st.number_input(
        "Giá vé máy bay (VNĐ)", value=2500000, step=100000, format="%d"
    )

    # Dịch vụ bổ sung
    st.subheader("➕ Dịch vụ yêu cầu thêm")
    dv_dua_don = st.checkbox("Đưa đón tận nhà (+300.000 VNĐ)")
    dv_bao_hiem = st.checkbox("Bảo hiểm nâng cao (+200.000 VNĐ)")
    dv_an_rieng = st.checkbox("Chế độ ăn đặc biệt (+500.000 VNĐ)")

with col2:
    st.header("📊 Chi tiết tính giá & Chi phí")

    # Tạo đối tượng
    ve_bay = ThongTinThangBay(
        hang_hang_khong=hang_bay, hang_ve=hang_ve, gia_ve=gia_ve_bay
    )
    khach_hang = KhachHangTour(
        ho_ten=ho_ten, tuoi=tuoi, thang_di=thang_di, thong_tin_bay=ve_bay
    )

    # Thêm dịch vụ chọn thêm
    if dv_dua_don:
        khach_hang.them_dich_vu(DichVuBoSung("Đưa đón tận nhà", 300000))
    if dv_bao_hiem:
        khach_hang.them_dich_vu(DichVuBoSung("Bảo hiểm nâng cao", 200000))
    if dv_an_rieng:
        khach_hang.them_dich_vu(DichVuBoSung("Chế độ ăn đặc biệt", 500000))

    # Tính toán
    thong_tin_tuoi = khach_hang.tinh_gia_dich_vu_khach(gia_tour_co_ban)
    phi_tour_thuc_te = thong_tin_tuoi["phi_tour"]
    gia_phong_thuc_te = khach_hang.tinh_gia_phong_khach_san(gia_phong_tieu_chuan)
    tong_dv_them = sum(dv.gia_goc for dv in khach_hang.dich_vu_them)
    tong_tien = phi_tour_thuc_te + gia_phong_thuc_te + gia_ve_bay + tong_dv_them

    # Hiển thị thông báo mùa cao điểm
    if khach_hang.la_mua_cao_diem:
        st.warning(
            f"🔥 **Tháng {thang_di} là MÙA CAO ĐIỂM!** Giá phòng tăng 30% so với tiêu chuẩn."
        )
    else:
        st.success(
            f"🌿 **Tháng {thang_di} là MÙA THẤP ĐIỂM.** Giá phòng áp dụng mức bình thường."
        )

    # Hiển thị ghi chú độ tuổi
    st.info(f"👶 **Chính sách độ tuổi ({tuoi} tuổi):** {thong_tin_tuoi['ghi_chu']}")

    # Bảng phân tích chi phí
    st.write("### 🧾 Bảng kê chi phí chi tiết")
    st.table(
        [
            {
                "Khoản mục": "Phí dịch vụ Tour",
                "Chi tiết": f"{thong_tin_tuoi['ghi_chu']}",
                "Thành tiền (VNĐ)": f"{phi_tour_thuc_te:,.0f}",
            },
            {
                "Khoản mục": "Phòng khách sạn",
                "Chi tiết": f"Khách sạn tháng {thang_di} ({'Cao điểm +30%' if khach_hang.la_mua_cao_diem else 'Giá chuẩn'})",
                "Thành tiền (VNĐ)": f"{gia_phong_thuc_te:,.0f}",
            },
            {
                "Khoản mục": "Vé máy bay",
                "Chi tiết": f"{hang_bay} ({hang_ve})",
                "Thành tiền (VNĐ)": f"{gia_ve_bay:,.0f}",
            },
            {
                "Khoản mục": "Dịch vụ yêu cầu thêm",
                "Chi tiết": (
                    ", ".join([dv.ten_dich_vu for dv in khach_hang.dich_vu_them])
                    if khach_hang.dich_vu_them
                    else "Không chọn"
                ),
                "Thành tiền (VNĐ)": f"{tong_dv_them:,.0f}",
            },
        ]
    )

    st.markdown("---")
    st.metric(
        label="💰 TỔNG CHI PHÍ TOUR DỰ KIẾN", value=f"{tong_tien:,.0f} VNĐ"
    )
