import datetime
from pathlib import Path
import json
import requests, base64
#--XỬ LÝ LƯU TRỮ
# CAC HAM XU LY LUU TRU MOI THEO CACH CUA THAY
Dia_chi_Dich_vu = 'https://data-service-quoc.herokuapp.com/'
Dia_chi_Media = f'''{Dia_chi_Dich_vu}/Media'''
Loai_Nguoi_dung ="Nhan_vien"
# CAC HAM XU LY LUU TRU 
#-----Doc khung html
def docKhungHTML():
    Chuoi_HTML = ""  
    Doi_tuong_A ={"quoc":"ok"}
    Ma_so_Xu_ly = "Doc_Khung_HTML" 
    Doi_tuong_B ={}
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B['Kq'] == 'OK':
        Chuoi_HTML = Doi_tuong_B['Chuoi_HTML']      
    return Chuoi_HTML
#-----Doc Cong ty
def Doc_Cong_ty():
    Cong_ty = {}
    Doi_tuong_A ={"quoc":"ok"}
    Ma_so_Xu_ly = "/Doc_Cong_ty" 
    Doi_tuong_B ={}
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B['Kq'] == 'OK':
        Cong_ty = Doi_tuong_B['Cong_ty']    
    return Cong_ty
#----Doc Danh sach nhan vien 
def Doc_Danh_sach_Nhan_vien():
    Danh_sach_Nhan_vien = []
    Doi_tuong_A ={"quoc":"ok"}
    Ma_so_Xu_ly = "Doc_Danh_sach_Nhan_vien" 
    Doi_tuong_B ={}
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B['Kq'] == 'OK':
        Danh_sach_Nhan_vien= Doi_tuong_B['Danh_sach_Nhan_vien'] 
    return Danh_sach_Nhan_vien

#---Ghi thong tin cap nhat
def Ghi_Nhan_vien(Nhan_vien):     
    Doi_tuong_A ={"quoc":"ok", "Nhan_vien": Nhan_vien}
    Ma_so_Xu_ly = "Ghi_Nhan_vien"     
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    return Doi_tuong_B
#---Ghi Hình Nhân viên
def Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh):       
    Ma_so_Xu_ly = "Ghi_Hinh_Nhan_vien"     
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''
    Chuoi_Hinh =  base64.b64encode(Hinh.read())
    Chuoi_Hinh = Chuoi_Hinh.decode('utf-8')    
    Doi_tuong_A ={"Nhan_vien": Nhan_vien, "Hinh": Chuoi_Hinh}
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A)
    Doi_tuong_B = json.loads(res.text)
    return Doi_tuong_B

#XU LY NGHIEP VU
#--Doc_Danh_sach_Nhan_vien_QLCN
def Doc_Danh_sach_Nhan_vien_QLCN(QLCN):
  Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien()
  Danh_sach_Nhan_vien_QLCN = []
  for nv in Danh_sach_Nhan_vien:
    if(nv["Don_vi"]["Chi_nhanh"]["Ma_so"] == QLCN["Chi_nhanh"]["Ma_so"]):
      Danh_sach_Nhan_vien_QLCN.append(nv)
  return Danh_sach_Nhan_vien_QLCN

#--Tra_cuu_Quan_ly_Don_vi
def Tra_cuu_Quan_ly_Chi_nhanh(QLCN, tuKhoa):
    dstk = []
    Danh_sach_Nhan_vien_Theo_QLCN = Doc_Danh_sach_Nhan_vien_QLCN(QLCN)
    tuKhoa = tuKhoa.lower()
    for nv in Danh_sach_Nhan_vien_Theo_QLCN:
        if(tuKhoa in nv["Ho_ten"].lower()
        or tuKhoa in nv["Gioi_tinh"].lower()
        or tuKhoa in nv["Don_vi"]["Ten"].lower()
         or tuKhoa in nv["Don_vi"]["Chi_nhanh"]["Ten"].lower()
         or tuKhoa in nv["CMND"].lower()
         or tuKhoa in nv["Dia_chi"].lower()
        ):
            dstk.append(nv)
    return dstk
#--Doc_Danh_sach_Don_xin_Nghi_QLDV
def Doc_Danh_sach_Don_xin_Nghi_QLCN(Danh_sach_Nhan_vien):
  Danh_sach_Nhan_vien_Don_Xin_nghi = []
  for nv in Danh_sach_Nhan_vien:
    for dxn in nv["Danh_sach_Don_xin_nghi"]:
      if(dxn["Y_kien_Quan_ly_Chi_nhanh"]["Da_co_Y_kien"] == False and dxn["Y_kien_Quan_ly_Don_vi"]["Da_co_Y_kien"]==True):
        Danh_sach_Nhan_vien_Don_Xin_nghi.append(nv)
        break
  return Danh_sach_Nhan_vien_Don_Xin_nghi

##--Tạo chuỗi tiền tệ
def Tao_chuoi_Tien_te(n):
  Chuoi = '${:,}'.format(n)
  Chuoi = Chuoi.replace(",", ".")
  Chuoi = Chuoi.replace("$", "")
  return Chuoi

#--XU LY GIAO DIEN 
#------Xu ly giao dien dang nhap
def Tao_Chuoi_HTML_Dang_nhap(tenDangNhap="", matKhau="", thongBaoDangNhap=""):
    Cong_ty = Doc_Cong_ty()    
    chuoiHTML = f'''<div class= "container px-3"> <h1 class="text-danger"> {thongBaoDangNhap} </h1> </div> '''
    chuoiHTML += f'''<div class= "container px-3"> <h1 class="text-primary">Tên Công ty:  {Cong_ty["Ten"]} </h1> </div>'''
    chuoiHTML += f""" <div class= "container px-3">
        <form action="/QLCN/kiem-tra-dang-nhap" method="POST">            
            <div class="form-group">
              <label class="text-primary" for="name">Tên Đăng nhập</label>
              <input type="text" class="form-control" name="txtTenDangNhap" id="name" placeholder="Nhập tên đăng nhập: QLCN_1, QLCN_2,..." >
            </div>
            <div class="form-group">
              <label class="text-primary" for="pass">Mật khẩu</label>
              <input type="password" class="form-control" name="txtMatKhau" id="pass" placeholder="Nhập mật khẩu:  QLCN_1, QLCN_2,...">
            </div>
            <button type="submit" class="btn btn-primary">Đăng nhập</button>
        </form>
      </div> """
    return chuoiHTML

#--Tao_Chuoi_HTML_Tra_cuu
def Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien, tuKhoa=""):
  chuoiHTML = f''' 
      <div class="container bg-primary py-3 my-3">
          <form action="/QLCN/tra-cuu-nhan-vien" method="POST">
          <input type="text" name="txtTuKhoa" value="{tuKhoa}"/> 
          <input type="submit" value="Tra cứu" class="btn btn-success"/> 
          <span class="badge badge-danger">Kết quả: {len(Danh_sach_Nhan_vien)}</span>
          </form>
      </div>
   '''
  return chuoiHTML
#--Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi
def Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Don_xin_nghi):
  So_don = 0
  if len(Danh_sach_Don_xin_nghi) > 0:  
    for nv in Danh_sach_Don_xin_nghi:
      for dxn in nv["Danh_sach_Don_xin_nghi"]:               
        if dxn["Y_kien_Quan_ly_Don_vi"]["Da_co_Y_kien"] == True and dxn["Y_kien_Quan_ly_Chi_nhanh"]["Da_co_Y_kien"] == False  :
          So_don += 1   
  chuoiHTML = f''' 
    <div class="container-fluid p-2 my-2 justify-content-end "> 
      <div>
          <h5 class="text-danger">Đang đăng nhập: {QLCN["Ten_Dang_nhap"]} </h5>        
      </div>
      <div class="container-fluid">
          <form action="/Nhan_vien/thoat-dang-nhap" method="POST">               
              <button type="submit" class="btn btn-primary">Thoát Đăng nhập</button>
          </form>
        </div>
    </div>
       <div class="container bg-success py-3 my-3 ">
          <div class="row">
              <div class="col">
                <form action="/QLCN/quan-ly-nhan-vien" method="POST">               
                   <input type="submit" value="Quản lý Nhân viên" class="btn btn-warning" />
                </form>
               
              </div>
              <div class="col">
                <form action="/QLCN/bao-cao-don-vi" method="POST">               
                   <input type="submit" value="Báo cáo Đơn vị" class="btn btn-warning" />
                </form>               
              </div>
               <div class="col">
                <form action="/QLCN/bao-cao-ngoai-ngu" method="POST">               
                   <input type="submit" value="Báo cáo Ngoại ngữ" class="btn btn-warning" />
                </form>               
              </div>
              <div class="col">
              <form action="/QLCN/duyet-danh-sach-don-xin-nghi" method="POST">               
                    <input type="submit" value="Duyệt Đơn xin nghỉ" class="btn btn-warning" /> <span class="badge badge-danger">Số đơn: {So_don} </span>
                </form>
               
              </div>
          </div>
      </div>
  '''
  return chuoiHTML
#--Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi
def Tao_Chuoi_HTML_Xem_Quan_ly_Chi_nhanh(QLCN, Danh_sach_Nhan_vien):
  chuoiHTML =f''' ''' 
  Cong_ty = Doc_Cong_ty() 
  for Nhan_vien in Danh_sach_Nhan_vien:
    Chuoi_Ngoai_Ngu = ""
    Chuoi_HTML_Don_vi_Bo_sung = ""
    Danh_sach_Don_vi_Bo_sung = Cong_ty["Danh_sach_Don_vi"]
    for nn in Nhan_vien["Danh_sach_Ngoai_ngu"]:
      Chuoi_Ngoai_Ngu += f'''<span class="badge badge-primary mx-3"> {nn["Ten"]}</span> '''
    Danh_sach_Don_vi_Bo_sung = [Danh_sach_Don_vi_Bo_sung for Danh_sach_Don_vi_Bo_sung in Danh_sach_Don_vi_Bo_sung if Danh_sach_Don_vi_Bo_sung["Chi_nhanh"]["Ma_so"] == QLCN["Chi_nhanh"]["Ma_so"] and Danh_sach_Don_vi_Bo_sung["Ma_so"] !=Nhan_vien["Don_vi"]["Ma_so"] ]
    for dvbs in Danh_sach_Don_vi_Bo_sung:
      Chuoi_HTML_Don_vi_Bo_sung += f'''

       <form action="/QLCN/chuc-nang-cap-nhat" method="post">
            <input type="hidden" name="txtMa_so_Nhan_vien" value="{Nhan_vien["Ma_so"]}" />
           <input type="hidden" name="Ma_Xu_ly" value="Chuyen_Don_vi" />
                          
               <div class="col">           
                  <input type="hidden" name="txtTenDonVi" value="{dvbs["Ten"]}" />
                  <input type="hidden" name="txtMaDonVi" value="{dvbs["Ma_so"]}" />               
                <button type="submit" class="btn btn-warning" name="btnDonVi"  >{dvbs["Ten"]}</button>  
                </div>
             
        </form>
    '''    
    
    chuoiHTML += f'''    
    <!--button chuc data-toggle cua nhan vien -->
    <div class="container bg-secondary py-3">
      <div class=" row py-3">
          
          <div class="col-3">
             <button class=" btn btn-danger" type="button" data-toggle="collapse" data-target="#ChuyenDonVi-{Nhan_vien["Ma_so"]}" aria-expanded="false" aria-controls="collapseExample">
                Chuyển Đơn vị
               </button>
          </div>    
         </div>
    </div>
  <!--/button chuc data-toggle cua nhan vien -->     
     <!--form cap nhat Ngoai ngu-->
     
    <div class="container collapse bg-secondary" id="ChuyenDonVi-{Nhan_vien["Ma_so"]}">
      <div class="container py-3">
        <h3 class="text-danger">CHUYỂN ĐƠN VỊ NHÂN VIÊN CÓ MÃ: {Nhan_vien["Ma_so"]} - TÊN: {Nhan_vien["Ho_ten"]}</h3>
        <div class="row">  
         {Chuoi_HTML_Don_vi_Bo_sung}
        </div>
      </div>
    </div>
     <!--/form cap nhat ngoai ngu-->  

    <div class="container">
    <div class="row">
        <div class="col-3">
         <img src="{Dia_chi_Media}/{Nhan_vien["Ma_so"]}.png" alt="{Nhan_vien["Ma_so"]}.png" class="img-thumbnail" style="height:250px; width:200px" >
        </div>
        <div class="col-9">
         <p>Họ tên: {Nhan_vien["Ho_ten"]} - Giới tính: {Nhan_vien["Gioi_tinh"]} </p>
         <p>CMND: {Nhan_vien["CMND"]} - Ngày sinh: {Nhan_vien["Ngay_sinh"]}- Mức lương:  {Tao_chuoi_Tien_te(Nhan_vien["Muc_luong"])} </p>
         <p>Điện thoại: {Nhan_vien["Dien_thoai"]} - Email: {Nhan_vien["Mail"]}     </p>
         <p>Địa chỉ:{Nhan_vien["Dia_chi"]} - Đơn vị:  <span class="badge badge-success mx-3"> {Nhan_vien["Don_vi"]["Ten"]}</span> </p>         
          <p>Danh sách ngoại ngữ: {Chuoi_Ngoai_Ngu}</p>               
          
                           
        </div>
    </div>
    </div> 

     '''
  return chuoiHTML
#--Tao_Chuoi_HTML_Danh_sach_Don_Xin_nghi
def Tao_Chuoi_HTML_Danh_sach_Don_Xin_nghi(Danh_sach_Don_xin_nghi_Nhan_vien):  
  chuoiHTML = ""
  if len(Danh_sach_Don_xin_nghi_Nhan_vien) >0:
    Chuoi_Don_xin_Nghi = ""
    stt = 0
    for nv in Danh_sach_Don_xin_nghi_Nhan_vien:     
      for dxn in nv["Danh_sach_Don_xin_nghi"]:
        if(dxn["Y_kien_Quan_ly_Chi_nhanh"]["Da_co_Y_kien"] == False and dxn["Y_kien_Quan_ly_Don_vi"]["Da_co_Y_kien"]== True):
          stt +=1
          Y_kien_Quan_ly_Don_vi = ""
          Y_kien_Quan_ly_Chi_nhanh = ""

          if dxn["Y_kien_Quan_ly_Don_vi"]["Da_co_Y_kien"] == True:
            Y_kien_Quan_ly_Don_vi = f'''{ dxn["Y_kien_Quan_ly_Don_vi"]["Noi_dung"]} '''
          else:
            Y_kien_Quan_ly_Don_vi = "Chưa có ý kiến"
          
          if dxn["Y_kien_Quan_ly_Chi_nhanh"]["Da_co_Y_kien"] == True:
            Y_kien_Quan_ly_Chi_nhanh = "Đã có ý kiến"
          else:
            Y_kien_Quan_ly_Chi_nhanh = "Chưa có ý kiến"

          Chuoi_Don_xin_Nghi += f''' 
          <tr>
                <td>{stt}</td>
                <td>{nv["Ho_ten"]}</>
                <td>{dxn["Ngay_Nop_don"]}</td>
                <td>{dxn["So_ngay"]}</td>
                <td>{dxn["Ly_do"]}</td>
                <td>{Y_kien_Quan_ly_Don_vi}</td>
                <td>{Y_kien_Quan_ly_Chi_nhanh}</td>
                <td>
                <div class="container">
                <button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#Don_xin_nghi-{stt}">Duyệt Đơn</button>

                <!-- Modal -->
                <div id="Don_xin_nghi-{stt}" class="modal fade" role="dialog">
                  <div class="modal-dialog">
                
                    <!-- Modal content-->
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close bg-danger" data-dismiss="modal">&times;</button>            
                      </div>
                      <div class="modal-body">
                      <!--form nop don xin nghi-->    
                      
                        <div class="container py-3">
                          <h3 class="text-danger text-center">DUYỆT ĐƠN XIN NGHỈ CỦA {nv["Ma_so"]} : {nv["Ho_ten"]}</h3>
                            <form action="/QLCN/duyet-don-xin-nghi" method="post">
                                <input type="hidden" name="Ma_Xu_ly" value="Nop_Don_xin_nghi" />
                                <div class="container py-3">
                                    <label for="">Họ tên :  {nv["Ho_ten"]} </label> <br>
                                    <label for=""> Đơn vị:  {nv["Don_vi"]["Ten"]}</label> <br>
                                    <label for="">CMND: {nv["CMND"]}</label> <br>
                                    <label for="">Ngày bắt đầu nghỉ: {dxn["Ngay_Bat_dau_nghi"]}</label> <br>
                                    <label for=""> Số ngày nghỉ: {dxn["So_ngay"]}</label> <br>
                                    <label for=""> Lý do: {dxn["Ly_do"]}</label> <br> 
                                    <div class="row">
                                      <div class="col radio">
                                          <label><input type="radio" name="rdbYKien" value="Dong_y" checked>Đồng ý cho nghỉ</label>
                                        </div>
                                        <div class="col radio">
                                          <label><input type="radio" name="rdbYKien" value="Khong_Dong_y">Không đồng ý cho nghỉ</label>
                                        </div>
                                    </div>
                                    <label>Nội dung: </label>
                                    <textarea name="txtNoiDung" id="" cols="30" rows="3" required></textarea>
                                    <input type="hidden" name="txtMa_so_Nhan_vien" value="{nv["Ma_so"]}" />
                                    <input type="hidden" name="txtNgayNop" value="{dxn["Ngay_Nop_don"]}" />
                                    <p class="text-center"><input type="submit" value="Duyệt đơn" class="btn btn-primary "></p>
                                </div>       

                            </form>
                        </div>
                    
                      <!--form nop don xin nghi-->

                      </div>
                      
                    </div>
                
                  </div>
                </div>

                </div>            
                </td>
                
          </tr> '''
    chuoiHTML += f'''
     <p class="py-2 bg-info">Số đơn xin nghỉ chưa được duyệt:<span class="badge badge-danger">Số đơn: {stt} </span> </p>               
          <table class="table table-striped">
            <thead>
              <tr>
                <th>STT</th>
                <th>Họ tên </th>
                <th>Ngày nộp</th>
                <th>Số ngày nghỉ</th>
                <th>Lý do</th>
                <th>Ý kiến của Quản lý Đơn vị - Nội dung</th>
                <th>Ý kiến của Quản lý Chi nhánh - Nội dung</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {Chuoi_Don_xin_Nghi}
            </tbody>
          </table>
   '''
  else: 
     chuoiHTML+=f'''<p class="container py-2 bg-info"> Không có đơn xin nghỉ nào  </p> '''
  return chuoiHTML

#--Tao_Chuoi_HTML_Bao_cao_Ngoai_ngu
def Tao_Chuoi_HTML_Bao_cao_Ngoai_ngu(Danh_sach_Nhan_vien_Chi_nhanh):
  Cong_ty = Doc_Cong_ty()
  Chuoi_Thong_ke = ""
  for nn in Cong_ty["Danh_sach_Ngoai_ngu"]:
    Tong_so_Nhan_vien_Ngoai_ngu = 0    
    for Nhan_vien in Danh_sach_Nhan_vien_Chi_nhanh:
      for Nhan_vien_Ngoai_ngu in Nhan_vien["Danh_sach_Ngoai_ngu"]:
        if(nn["Ma_so"] == Nhan_vien_Ngoai_ngu["Ma_so"]):
          Tong_so_Nhan_vien_Ngoai_ngu += 1
    Phan_tram_Nhan_vien_Ngoai_ngu = (Tong_so_Nhan_vien_Ngoai_ngu/len(Danh_sach_Nhan_vien_Chi_nhanh))*100
    Chuoi_Thong_ke += f''' 
    <tr>              
              <td>{nn["Ten"]}</td>
              <td>{Tong_so_Nhan_vien_Ngoai_ngu}</td>
              <td>{round(Phan_tram_Nhan_vien_Ngoai_ngu, 2)}</td>
            </tr>       
    '''   
  chuoiHTML = f'''
     <div class="container">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Ngoại ngữ</th>
              <th>Số nhân viên</th>
              <th>Tỷ lệ phần %</th>
            </tr>
          </thead>
          <tbody>
            {Chuoi_Thong_ke}        
          </tbody>
        </table>
      </div>
   '''
  return chuoiHTML

#--Tao_Chuoi_HTML_Bao_cao_Don_vi
def Tao_Chuoi_HTML_Bao_cao_Don_vi(Danh_sach_Nhan_vien_Chi_nhanh, QLCN):
  Chuoi_Thong_ke = ""
  Cong_ty = Doc_Cong_ty()
  Danh_sach_Don_vi_Chi_nhanh = [Danh_sach_Don_vi_Chi_nhanh for Danh_sach_Don_vi_Chi_nhanh in Cong_ty["Danh_sach_Don_vi"] if Danh_sach_Don_vi_Chi_nhanh["Chi_nhanh"]["Ma_so"] == QLCN["Chi_nhanh"]["Ma_so"]]
  for dv in Danh_sach_Don_vi_Chi_nhanh:
    Tong_so_Nhan_vien_Don_vi = 0
    for Nhan_vien in Danh_sach_Nhan_vien_Chi_nhanh:
      if(dv["Ma_so"]== Nhan_vien["Don_vi"]["Ma_so"]):
        Tong_so_Nhan_vien_Don_vi +=1
    Phan_tram_Nhan_vien_Don_vi = (Tong_so_Nhan_vien_Don_vi/len(Danh_sach_Nhan_vien_Chi_nhanh))*100
    Chuoi_Thong_ke += f'''
            <tr>
              <td>{dv["Ten"]}</td>
              <td>{Tong_so_Nhan_vien_Don_vi}</td>
              <td>{round(Phan_tram_Nhan_vien_Don_vi, 2)}</td>
            </tr>  
     '''
  chuoiHTML = f'''
     <div class="container">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Đơn vị</th>
              <th>Số nhân viên</th>
              <th>Tỷ lệ phần %</th>
            </tr>
          </thead>
          <tbody>
              {Chuoi_Thong_ke}
          </tbody>
        </table>
      </div>
   '''
  return chuoiHTML