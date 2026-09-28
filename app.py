from datetime import datetime


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
    def la_mua_cao_diem(self) -> bool:  # <--- Đã sửa tại đây (thay 0 thành self)
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
            ghi_chu = "Người lớn (Từ 12 tuổi): 100% giá dịch vụ"

        phi_dich_vu_tour = gia_dich_vu_co_ban * he_so
        return {"phi_tour": phi_dich_vu_tour, "ghi_chu": ghi_chu}

    def tinh_gia_phong_khach_san(self, gia_phong_tieu_chuan: float) -> float:
        if self.la_mua_cao_diem:
            return gia_phong_tieu_chuan * 1.3
        return gia_phong_tieu_chuan

    def tinh_tong_chi_phi(
        self, gia_dich_vu_co_ban: float, gia_phong_tieu_chuan: float
    ) -> float:
        phi_tour = self.tinh_gia_dich_vu_khach(gia_dich_vu_co_ban)["phi_tour"]
        gia_phong = self.tinh_gia_phong_khach_san(gia_phong_tieu_chuan)
        gia_ve_bay = self.thong_tin_bay.gia_ve if self.thong_tin_bay else 0.0
        tong_dich_vu_them = sum(dv.gia_goc for dv in self.dich_vu_them)

        return phi_tour + gia_phong + gia_ve_bay + tong_dich_vu_them
