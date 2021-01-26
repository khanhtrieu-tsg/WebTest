from flask import jsonify, request
from flask_restful import Resource
from pymongo import MongoClient

from app_common import Timer, client, link_api_agent, link_api_mac

database = client.ByteSave_Customers
db = database["Customers_DaiDien"]


class NDD(Resource):
    def get(self, id):
        try:
            dataNDD = []
            i = 0
            for item in db.find({'$and': [{'IS_XOA': {'$ne': 1}},{'ID_KH': int(id)}]}):
                i = i + 1
                dataNDD.append({
                    'stt': i,
                    'id': item['id'],
                    'DAI_DIEN_TEN': item['DAI_DIEN_TEN'],
                    'DAI_DIEN_SDT': item['DAI_DIEN_SDT'],
                    'DAI_DIEN_CHUC_VU': item['DAI_DIEN_CHUC_VU'],
                    'DAI_DIEN_EMAIL': item['DAI_DIEN_EMAIL'],
                    'DAI_DIEN_TRANG_THAI': item['DAI_DIEN_TRANG_THAI'],
                })
            return jsonify({'data': dataNDD})
        except Exception as e:
            return jsonify({'data': [], 'string_error': str(e)})

    def post(self, id):
        try:
            form = request.form
            id_ndd = form.get('idndd','')
            if id_ndd != '':
                db.update_one(
                    {"id": int(id_ndd)},
                    {"$set": {
                              'DAI_DIEN_TEN': form.get('NDD_TEN'),
                              'DAI_DIEN_SDT': form.get('NDD_SDT'),
                              'DAI_DIEN_CHUC_VU': form.get('NDD_CHUC_VU'),
                              'DAI_DIEN_EMAIL': form.get('NDD_EMAIL'),
                              'DAI_DIEN_TRANG_THAI': int(form.get('NDD_TRANGTHAI')),
                              }})
                return jsonify({'status': 'OK', 'msg': 'Chỉnh sửa thành công người liên hệ: ' + form.get('NDD_TEN')})
            idmax = db.find().sort([("id", -1)])[0]['id'] if db.find().count() > 0 else 0
            db.insert({
                'id': idmax + 1,
                'ID_KH': int(id),
                'DAI_DIEN_TEN': form.get('NDD_TEN'),
                'DAI_DIEN_SDT': form.get('NDD_SDT'),
                'DAI_DIEN_CHUC_VU': form.get('NDD_CHUC_VU'),
                'DAI_DIEN_EMAIL': form.get('NDD_EMAIL'),
                'DAI_DIEN_TRANG_THAI': int(form.get('NDD_TRANGTHAI')),
                'IS_XOA': 0,
            })
        except Exception as e:
            return jsonify({'status': 'OK', 'msg': 'Thêm mới không thành công người liên hệ!', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Thêm mới thành công người liên hệ: ' + form.get('NDD_TEN')})

class NDD_moi(Resource):
    def post(self,id):
        form = request.form
        for i in range(0, int(form.get('CountRowNDD')) + 1):
            try:
                if form.get('NguoiDD_TEN' + str(i)) != '' and form.get('NguoiDD_TEN' + str(i)) != None:
                    idmax = db.find().sort([("id", -1)])[0]['id'] if db.find().count() > 0 else 0
                    db.insert({
                        'id': idmax + 1,
                        'ID_KH': int(id),
                        'DAI_DIEN_TEN': form.get('NguoiDD_TEN' + str(i)),
                        'DAI_DIEN_SDT': form.get('NguoiDD_SDT' + str(i)),
                        'DAI_DIEN_CHUC_VU': form.get('NguoiDD_CHUC_VU' + str(i)),
                        'DAI_DIEN_EMAIL': form.get('NguoiDD_EMAIL' + str(i)),
                        'DAI_DIEN_TRANG_THAI': int(form.get('NguoiDD_TRANG_THAI' + str(i))),
                        'IS_XOA': 0,
                    })
            except Exception as e:
                continue
        return jsonify({'status': 'OK', 'msg': 'Chỉnh sửa thành công khách hàng: ' + str(form.get('KH_TEN', ''))})

class Del_NDD(Resource):
    def post(self,id):
        try:
            db.update_one(
                {"id": int(id)},
                {"$set": {
                    'IS_XOA': 1,
                }})
        except Exception as e:
            return jsonify(
                {'status': 'NOK', 'msg': 'Xóa người đại diện không thành công!'})
        return jsonify({'status': 'OK', 'msg': 'Xóa thành công người đại hiện!'})
