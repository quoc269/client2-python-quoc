from flask import Flask, request, abort
from flask.globals import session
from XL_3L_Quan_ly_Chi_nhanh import*
#--THẦY ƠI, DO DUNG LƯỢNG TẬP TIN VƯỢT QUÁ 10M, EM BỎ FOLDER ENVIROMENT FLASK,
#  KHI CHẠY THẦY CÀI LẠI GIÚP EM. CẢM ƠN THẦY!

DichVu = Flask(__name__, static_url_path="/Media_QLCN", static_folder="Media_QLCN")
DichVu.secret_key = "QuocNguyenViet" 

#--biến dùng chung

#--Xử lý biến cố khơi động
@DichVu.route("/", methods =["GET"])
def XL_KhoiDong():  
    khungHTML = docKhungHTML() 
    chuoiHTML = Tao_Chuoi_HTML_Dang_nhap()
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)    
    return chuoiHTML

#--Xử lý biến cố đăng nhập
@DichVu.route("/QLCN/kiem-tra-dang-nhap", methods =["POST"])
def XL_DangNhapNhanVien():
    khungHTML = docKhungHTML()
    Danh_sach_Quan_ly_Chi_nhanh = Doc_Cong_ty()["Danh_sach_Quan_ly_Chi_nhanh"]
    tenDangNhap = request.form["txtTenDangNhap"]
    matKhau = request.form["txtMatKhau"]
    chuoiHTML =''
  
    Hop_le = any([QLCN for QLCN in Danh_sach_Quan_ly_Chi_nhanh
                    if QLCN['Ten_Dang_nhap']== tenDangNhap and QLCN['Mat_khau']==matKhau ])
    if Hop_le:
        QLCN = [QLCN for QLCN in Danh_sach_Quan_ly_Chi_nhanh
                          if QLCN['Ten_Dang_nhap']== tenDangNhap and QLCN['Mat_khau']==matKhau][0]       
        Danh_sach_Nhan_vien_Chi_nhanh = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)        
        Danh_sach_Don_xin_nghi_QLCN = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_Chi_nhanh)
        session["Nguoi_dung"] = QLCN   
        chuoiHTML =Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Don_xin_nghi_QLCN) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_Chi_nhanh) + Tao_Chuoi_HTML_Xem_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Nhan_vien_Chi_nhanh)
    else:
        chuoiHTML = Tao_Chuoi_HTML_Dang_nhap("","","Đăng nhập không hợp lệ")   
      
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
    return chuoiHTML

 #Xử lý biến cố /QLDV/tra-cuu-nhan-vien
@DichVu.route("/QLCN/tra-cuu-nhan-vien", methods=["POST"])
def XL_Tra_cuu_Nhan_vien ():
    khungHTML = docKhungHTML()
    tuKhoa = request.form["txtTuKhoa"]     
    QLCN = session["Nguoi_dung"]
    print(QLCN)
    Danh_sach_Nhan_vien_Chi_Nhanh = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_Chi_Nhanh)  
    Danh_sach_Tim_kiem = Tra_cuu_Quan_ly_Chi_nhanh(QLCN, tuKhoa)
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Don_xin_nghi_Nhan_vien) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Tim_kiem, tuKhoa) + Tao_Chuoi_HTML_Xem_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Tim_kiem)
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#--Xử lý chức năng \Nhan_vien\chuc-nang-cap-nhat
@DichVu.route("/QLCN/chuc-nang-cap-nhat", methods=["POST"])
def XL_ChucNangCapNhat_Nhan_vien():
    QLCN = session["Nguoi_dung"]          
    khungHTML = docKhungHTML() 
    Danh_sach_Nhan_vien_QLCN = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_QLCN)
    Ma_Xu_ly = request.form["Ma_Xu_ly"]    
    if Ma_Xu_ly == "Chuyen_Don_vi":
        Ma_so_Nhan_vien = request.form["txtMa_so_Nhan_vien"]  
        Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien_QLCN if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
        Ma_Don_vi_Moi = request.form["txtMaDonVi"]
        Ten_Don_vi_moi = request.form["txtTenDonVi"]      
        Nhan_vien["Don_vi"]["Ma_so"] = Ma_Don_vi_Moi
        Nhan_vien["Don_vi"]["Ten"] = Ten_Don_vi_moi
        Ghi_Nhan_vien(Nhan_vien)
    session["Nguoi_dung"] = QLCN
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN,Danh_sach_Don_xin_nghi_Nhan_vien) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_QLCN) + Tao_Chuoi_HTML_Xem_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Nhan_vien_QLCN)
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý biến cố /QLDV/quan-ly-nhan-vien
@DichVu.route("/QLCN/quan-ly-nhan-vien", methods=["POST"])
def XL_Quan_ly_Nhan_vien():
    khungHTML = docKhungHTML()
    QLCN ={}   
    if "Nguoi_dung" in session:
        QLCN = session['Nguoi_dung']
    Danh_sach_Nhan_vien_QLCN = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_QLCN)
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Don_xin_nghi_Nhan_vien) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_QLCN) + Tao_Chuoi_HTML_Xem_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Nhan_vien_QLCN)
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý duyệt danh sách đơn xin nghỉ /QLDV/duyet-danh-sach-don-xin-nghi
@DichVu.route("/QLCN/duyet-danh-sach-don-xin-nghi", methods=["POST"])
def XL_Duyet_Danh_sach_Don_xin_nghi():
    khungHTML = docKhungHTML()
    QLCN ={}   
    if "Nguoi_dung" in session:
        QLCN = session['Nguoi_dung']
    Danh_sach_Nhan_vien_QLCN = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_QLCN)   
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Don_xin_nghi_Nhan_vien) + Tao_Chuoi_HTML_Danh_sach_Don_Xin_nghi(Danh_sach_Don_xin_nghi_Nhan_vien) 
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

@DichVu.route("/QLCN/duyet-don-xin-nghi", methods=["POST"])
def XL_Duyet_Don_xin_nghi():
    khungHTML = docKhungHTML()   
    QLCN ={}   
    if "Nguoi_dung" in session:
        QLCN = session['Nguoi_dung'] 
    Danh_sach_Nhan_vien_QLCN = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_QLCN)  
    Ma_so_Nhan_vien = request.form["txtMa_so_Nhan_vien"]
    Ngay_Nop_don = request.form["txtNgayNop"]  
    Dong_y = request.form["rdbYKien"] 
    Y_kien = False
    Cho_nghi = ""
    Noi_dung = request.form["txtNoiDung"] 
    if Dong_y !="":
        Y_kien = True
    if Dong_y == "Dong_y":
        Cho_nghi = "Đồng ý. "
    else:
        Cho_nghi = "Không Đồng ý. "
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien_QLCN if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    for dxn in Nhan_vien["Danh_sach_Don_xin_nghi"]:
        if dxn["Ngay_Nop_don"] == Ngay_Nop_don:
            dxn["Y_kien_Quan_ly_Chi_nhanh"]["Da_co_Y_kien"] = Y_kien
            dxn["Y_kien_Quan_ly_Chi_nhanh"]["Noi_dung"] = Cho_nghi + Noi_dung
    Ghi_Nhan_vien(Nhan_vien)
    session["Nguoi_dung"] = QLCN  
    Danh_sach_Don_xin_nghi_Nhan_vien_moi = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_QLCN) 
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Don_xin_nghi_Nhan_vien_moi) + Tao_Chuoi_HTML_Danh_sach_Don_Xin_nghi(Danh_sach_Don_xin_nghi_Nhan_vien_moi) 
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML
#Xư lý báo cáo ngoại ngữ
@DichVu.route("/QLCN/bao-cao-ngoai-ngu", methods=["POST"])
def XL_Bao_cao_Ngoai_ngu():
    QLCN = session["Nguoi_dung"]
    khungHTML = docKhungHTML()
    Danh_sach_Nhan_vien_Chi_nhanh = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_Chi_nhanh)
    chuoiHTML =Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN,Danh_sach_Don_xin_nghi_Nhan_vien) +Tao_Chuoi_HTML_Bao_cao_Ngoai_ngu(Danh_sach_Nhan_vien_Chi_nhanh)
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xư lý báo cáo Đơn vị
@DichVu.route("/QLCN/bao-cao-don-vi", methods=["POST"])
def XL_Bao_cao_Don_vi():
    QLCN = session["Nguoi_dung"]
    khungHTML = docKhungHTML()
    Danh_sach_Nhan_vien_Chi_nhanh = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien_Chi_nhanh)
    chuoiHTML =Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN,Danh_sach_Don_xin_nghi_Nhan_vien) +Tao_Chuoi_HTML_Bao_cao_Don_vi(Danh_sach_Nhan_vien_Chi_nhanh, QLCN)
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý biến cố thoát đăng nhập
@DichVu.route("/Nhan_vien/thoat-dang-nhap", methods=["POST"])
def XL_ThoatDangNhap():
    khungHTML = docKhungHTML()
    chuoiHTML = ""
    if "Nguoi_dung" in session:
        session.pop("Nguoi_dung", None)    
        chuoiHTML = Tao_Chuoi_HTML_Dang_nhap()
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)    
    return chuoiHTML
#--Xóa cache browser
@DichVu.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

#--Run chuong trinh
if __name__ == '__main__':
   DichVu.run()
