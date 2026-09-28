from datetime import datetime


class DichVuBoSung:

    def __init__(self, ten_dich_vu: str, gia_goc: float):
        self.ten_dich_vu = ten_dich_vu
        self.gia_goc = gia_goc


class ThongTinThangBay:

    def __init__(self, hang_hang_khong: str, hang_ve: str, gia_ve: float):
        self.hang_hang_khong = hang_hang_khong  # Ví dụ: 'Vietnam Airlines', 'Vietjet'
        self.hang_ve = hang_ve  # Ví dụ: 'Phổ thông', 'Thương gia'
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
        self.thang_di = thang_di  # 1 đến 12
        self.thong_tin_bay = thong_tin_bay
        self.dich_vu_them = []  # Danh sách các đối tượng DichVuBoSung

    def them_dich_vu(self, dich_vu: DichVuBoSung):
        self.dich_vu_them.append(dich_vu)

    @property
    def la_mua_cao_diem(0) -> bool:
        # Quy định mùa cao điểm: Tháng 6, 7, 8 (Du lịch hè) và Tháng 12, 1 (Lễ/Tết)
        mua_cao_diem = [1, 6, 7, 8, 12]
        return self.thang_di in mua_cao_diem

    def tinh_gia_dich_vu_khach(self, gia_dich_vu_co_ban: float) -> dict:
        """Tính phí dịch vụ tour dựa trên độ tuổi của khách hàng:

        - Dưới 5 tuổi: Miễn phí dịch vụ (0%)
        - Từ 5 đến dưới 12 tuổi: 50% giá dịch vụ (không có giường riêng)
        - Từ 12 tuổi trở lên: 100% giá người lớn
        """
        if self.tuoi < 5:
            he_so = 0.0
            ghi_chu = "Trẻ em dưới 5 tuổi: Miễn phí dịch vụ"
        elif 5 <= self.tuoi < 12:
            he_so = 0.5
            ghi_chu = "Trẻ em 5-11 tuổi: 50% giá dịch vụ (Không giường riêng)"
        else:
            he_so = 1.0
            ghi_chu = "Người lớn (Từ 12 tuổi): 100% giá dịch vụ"

        phi_dich_vu_tour = gia_dich_vu_co_ban * he_so
        return {"phi_tour": phi_dich_vu_tour, "ghi_chu": ghi_chu}

    def tinh_gia_phong_khach_san(self, gia_phong_tieu_chuan: float) -> float:
        """Giá phòng khách sạn thay đổi theo mùa cao điểm / thấp điểm:

        - Mùa cao điểm: Tăng 30% giá phòng
        - Mùa thấp điểm: Giữ nguyên giá tiêu chuẩn
        """
        if self.la_mua_cao_diem:
            return gia_phong_tieu_chuan * 1.3
        return gia_phong_tieu_chuan

    def tinh_tong_chi_phi(
        self, gia_dich_vu_co_ban: float, gia_phong_tieu_chuan: float
    ) -> float:
        # 1. Phí dịch vụ tour theo độ tuổi
        phi_tour = self.tinh_gia_dich_vu_khach(gia_dich_vu_co_ban)["phi_tour"]

        # 2. Giá phòng theo mùa (Khách từ 5 tuổi trở lên tính phòng/giường nếu áp dụng)
        gia_phong = self.tinh_gia_phong_khach_san(gia_phong_tieu_chuan)

        # 3. Giá vé máy bay
        gia_ve_bay = self.thong_tin_bay.gia_ve if self.thong_tin_bay else 0.0

        # 4. Các dịch vụ yêu cầu thêm
        tong_dich_vu_them = sum(dv.gia_goc for dv in self.dich_vu_them)

        # Tổng chi phí
        tong_tien = phi_tour + gia_phong + gia_ve_bay + tong_dich_vu_them
        return tong_tien


# ==========================================
# VÍ DỤ SỬ DỤNG CODE
# ==========================================
if __name__ == "__main__":
    # 1. Khai báo thông tin máy bay
    ve_vietnam_airlines = ThongTinThangBay(
        hang_hang_khong="Vietnam Airlines",
        hang_ve="Thương gia",
        gia_ve=3500000,
    )

    # 2. Tạo thông tin khách hàng đi vào tháng 7 (Mùa cao điểm)
    khach_hang_1 = KhachHangTour(
        ho_ten="Nguyễn Văn A",
        tuoi=8,  # Trẻ 8 tuổi -> 50% phí dịch vụ, không giường riêng
        thang_di=7,  # Tháng 7 -> Mùa cao điểm
        thong_tin_bay=ve_vietnam_airlines,
    )

    # 3. Thêm dịch vụ yêu cầu thêm
    khach_hang_1.them_dich_vu(
        DichVuBoSung(ten_dich_vu="Đưa đón tận nhà", gia_goc=300000)
    )
    khach_hang_1.them_dich_vu(
        DichVuBoSung(ten_dich_vu="Bảo hiểm du lịch nâng cao", gia_goc=150000)
    )

    # 4. Tính toán chi phí Tour
    GIA_TOUR_CO_BAN = 5000000
    GIA_PHONG_TIEU_CHUAN = 2000000

    thong_tin_tour = khach_hang_1.tinh_gia_dich_vu_khach(GIA_TOUR_CO_BAN)
    gia_phong_thuc_te = khach_hang_1.tinh_gia_phong_khach_san(
        GIA_PHONG_TIEU_CHUAN
    )
    tong_chi_phi = khach_hang_1.tinh_tong_chi_phi(
        GIA_TOUR_CO_BAN, GIA_PHONG_TIEU_CHUAN
    )

    # 5. In kết quả
    print(f"--- THÔNG TIN TOUR KHÁCH HÀNG: {khach_hang_1.ho_ten} ---")
    print(f"Tuổi: {khach_hang_1.tuoi} tuổi")
    print(
        f"Tháng đi: Tháng {khach_hang_1.thang_di} ({'Mùa cao điểm' if khach_hang_1.la_mua_cao_diem else 'Mùa thấp điểm'})"
    )
    print(
        f"Hãng máy bay: {khach_hang_1.thong_tin_bay.hang_hang_khong} - Hạng: {khach_hang_1.thong_tin_bay.hang_ve}"
    )
    print(f"Quy định tuổi: {thong_tin_tour['ghi_chu']}")
    print(f"Phí tour áp dụng: {thong_tin_tour['phi_tour']:,} VNĐ")
    print(f"Giá phòng khách sạn: {gia_phong_thuc_te:,} VNĐ")
    print(f"Giá vé máy bay: {khach_hang_1.thong_tin_bay.gia_ve:,} VNĐ")
    print(
        f"Tổng dịch vụ thêm: {sum(dv.gia_goc for dv in khach_hang_1.dich_vu_them):,} VNĐ"
    )
    print("-" * 40)
    print(f"TỔNG CHI PHÍ TOUR: {tong_chi_phi:,} VNĐ")
