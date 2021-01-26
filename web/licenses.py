from flask import jsonify, request
from flask_restful import Resource
from pymongo import MongoClient

from app_common import Timer, link_api_agent, link_api_mac

client = MongoClient("mongodb://0.0.0.0:27017")
database = client.ByteSave_Licenses
users = database["Users"]
db = database["Licenses"]


class hello(Resource):
    def get(self):
        return 'hello khánh'

class License(Resource):
    def get(self):
        data = []
        i = 0
        try:
            for item in db.find({'IS_XOA': {'$ne': 1}}):
                i = i + 1
                data.append({'STT': i,
                             'id': item['id'],
                             'MA_LICENSE': item['MA_LICENSE'],
                             'TIME_TAO_AT': item['TIME_TAO_AT'],
                             'TIME_UPDATE_AT': item['TIME_UPDATE_AT'],
                             'TIME_HET_HAN': '',
                             'ID_KH': item['ID_KH'],
                             'THANG_NAM': item['THANG_NAM'],
                             'SO_THANG_NAM': item['SO_THANG_NAM'],
                             'TRANG_THAI': item['TRANG_THAI'],
                             'SO_LUONG_MAY_SU_DUNG': item['SO_LUONG_MAY_SU_DUNG'],
                             })
        except Exception as e:
            return jsonify({'data': [], 'string_error': str(e)})
        return jsonify({'data': data})

    def post(self):
        if request.method == 'POST':
            form = request.form
            idd = form.get('idlicense', '')
            if idd != '' and idd != None:
                try:
                    db.update_one(
                        {"id": idd},
                        {"$set": {"ID_KH": form.get('ID_KH', ''),
                                  "MA_LICENSE": form.get('MA_LICENSE', ''),
                                  "TIME_HET_HAN": form.get('TIME_HET_HAN', ''),
                                  "SO_THANG_NAM": form.get('SO_THANG_NAM', ''),
                                  "THANG_NAM": form.get('THANG_NAM', ''),
                                  "SO_LUONG_MAY_SU_DUNG": form.get('SO_LUONG_MAY_SU_DUNG', ''),
                                  "TIME_CAI_DAT_AT": '',
                                  }})
                except Exception as e:
                    return jsonify(
                        {'status': 'NOK', 'msg': 'Chỉnh sửa không thành công mã bản quyền', 'string_error': str(e)})
                return jsonify({'status': 'OK', 'msg': 'Chỉnh sửa thành công mã bản quyền'})
            try:
                idmax = db.find().sort([("id", -1)])[0]['id'] if db.find().count() > 0 else 0
                db.insert({
                    'id': idmax + 1,
                    'ID_KH': int(form.get('ID_KH')),
                    'MA_LICENSE': form.get('MA_LICENSE'),
                    # 'TIME_HET_HAN': form.get('TIME_HET_HAN'),
                    'SO_THANG_NAM': int(form.get('TIME_HET_HAN')),
                    'THANG_NAM': int(form.get('Choisenamthang')),
                    'SO_LUONG_MAY_SU_DUNG': int(form.get('SO_LUONG_MAY_SU_DUNG')),
                    'TIME_TAO_AT': Timer.get_timestamp_now(),
                    'TIME_UPDATE_AT': Timer.get_timestamp_now(),
                    'TRANG_THAI': 0,
                    "TIME_CAI_DAT_AT": '',
                })
            except Exception as e:
                return jsonify(
                    {'status': 'NOK', 'msg': 'Thêm mới không thành công mã bản quyền', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Thêm mới thành công mã bản quyền'})


class Del_License(Resource):
    def post(self):
        try:
            form = request.form
            if form.get('id') != '':
                db.update_one(
                    {"id": id},
                    {"$set": {"IS_XOA": 1,
                              'TIME_UPDATE_AT': Timer.get_timestamp_now(),
                              }})
        except Exception as e:
            return jsonify({'status': 'NOK', 'msg': 'Xóa không thành công mã bản quyền', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Xóa thành công mã bản quyền'})


class Change_Quantity(Resource):
    def post(self):
        try:
            form = request.form
            if form.get('idLicense') != '':
                db.update_one(
                    {"id": int(form.get('idLicense'))},
                    {"$set": {"SO_LUONG_MAY_SU_DUNG": int(form.get('SO_LUONG_MAY_SU_DUNG_EDIT')),
                              'TIME_UPDATE_AT': Timer.get_timestamp_now(),
                              }})
        except Exception as e:
            return jsonify({'status': 'NOK', 'msg': 'Thay đổi só lượng máy sử dụng bản quyền không thành công!',
                            'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Thay đổi só lượng máy sử dụng bản quyền thành công!'})


class GiaHan_License(Resource):
    def post(self,id):
        try:
            form = request.form
            if id != '':
                db.update_one(
                    {"id": int(id)},
                    {"$set": {
                        "SO_THANG_NAM": int(form.get('TIME_HET_HAN_EDIT')),
                        "THANG_NAM": int(form.get('Choisenamthang')),
                        'TIME_UPDATE_AT': Timer.get_timestamp_now(),
                    }})
        except Exception as e:
            return jsonify({'status': 'NOK', 'msg': 'Gia hạn không thành công!', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Gia hạn thành công!'})

class Stop_License(Resource):
    def post(self):
        try:
            form = request.form
            if form.get('idLicense') != '':
                db.update_one(
                    {"id": int(form.get('idLicense'))},
                    {"$set": {
                        "TRANG_THAI": 2,
                        'TIME_UPDATE_AT': Timer.get_timestamp_now(),
                    }})
        except Exception as e:
            return jsonify({'status': 'NOK', 'msg': 'Dừng hoạt động không thành công!', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Dừng hoạt động thành công!'})
class Check_License(Resource):
    def post(self,MA_BAN_QUYEN,DIA_CHI_MAC):
        try:
            if db.find({'MA_LICENSE': MA_BAN_QUYEN}):
                item_license = db.find({'MA_LICENSE': MA_BAN_QUYEN.trim()})[0]
                # lấy giá trị của agent
                item_agent = str(link_api_agent) + '/check/' + str(item_license['id'] + '/' + str(DIA_CHI_MAC.trim()))
                if item_agent['type'] == 0:
                    time_cai_dat = item_agent['data']['TIME_CAI_DAT_AT']

                return jsonify({'status': 'OK', 'msg': 'Mã bản quyền hợp lệ!', })
        except Exception as e:
            return jsonify({'status': 'NOK', 'msg': 'Mã bản quyền không hợp lệ!', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Mã bản quyền hợp lệ!'})

class Active_License(Resource):
    def post(self,MA_BAN_QUYEN,DIA_CHI_MAC,ID_PHIEN_BAN,IP_PRIVATE,IP_PUBLIC,OS):
        try:
            if db.find({'MA_LICENSE': MA_BAN_QUYEN}):
                item_license = db.find({'MA_LICENSE': MA_BAN_QUYEN.trim()})[0]
                # thêm mới agent
                item_agent = str(link_api_agent) + '/them-moi/' + str(ID_PHIEN_BAN.trim()) + '/' + str(
                    item_license['id'])

                if item_agent['ID_AGENT'] != 0:
                    item_mac_active = str(link_api_mac) + '/them-moi/' + str(item_agent['ID_AGENT']) + '/' + str(
                        DIA_CHI_MAC.trim()) \
                                      + '/' + str(IP_PRIVATE.trim()) + '/' + str(IP_PUBLIC.trim()) + '/' + str(
                        OS.trim())
                    return jsonify({'status': 'OK', 'msg': 'Kích hoạt bản quyền thành công!', })
                return jsonify({'status': 'NOK', 'msg': 'không thành công!', })
        except Exception as e:
            return jsonify({'status': 'NOK', 'msg': 'không thành công!', 'string_error': str(e)})


