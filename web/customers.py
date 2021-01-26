from flask import jsonify, request
from flask_restful import Resource
from pymongo import MongoClient

from app_common import Timer,client, link_api_agent, link_api_mac

database = client.ByteSave_Customers
db = database["Customers"]

class hello(Resource):
    def get(self):
        return '<h1>Hello World</h1>'

class Customer(Resource):
    def get(self):
        data = []
        i = 0
        try:
            for item in db.find({'IS_XOA': {'$ne': 1}}):
                i = i + 1
                data.append({'STT': i,
                             'id': item['id'],
                             'KH_TEN': item['KH_TEN'],
                             'KH_EMAIL': item['KH_EMAIL'],
                             'KH_LOAI': item['KH_LOAI'],
                             'TIME_TAO_AT': item['TIME_TAO_AT'],
                             'KH_SDT': item['KH_SDT'],
                             'DIA_CHI': item['DIA_CHI'],
                             'MST': item['MST'],
                             'WEBSITE': item['WEBSITE'],
                             'FAX': item['FAX'],
                             'DAI_DIEN': [],
                             'DAI_DIEN_PHAT_LUAT': item['DAI_DIEN_PHAT_LUAT'],
                             })
        except Exception as e:
            return jsonify({'data': [], 'status': 'NOK', 'string_error': str(e)})
        return jsonify({'data': data, 'status': 'OK'})

    def post(self):
        if request.method == 'POST':
            form = request.form
            try:
                if db.find({'MST': form.get('MST')}).count() > 0:
                    return jsonify({'status': 'NOK', 'msg': 'Mã số thuế đã tồn tại!'})
                IS_NANG_CAP = 0
                if form.get('IS_NANG_CAP', 'off') == '1':
                    IS_NANG_CAP = 1
                idmax = db.find().sort([("id", -1)])[0]['id'] if db.find().count() > 0 else 0
                db.insert({
                    'id': idmax + 1,
                    'KH_TEN': form.get('KH_TEN'),
                    'KH_EMAIL': form.get('KH_EMAIL'),
                    'KH_LOAI': int(form.get('LOAI_KH')),
                    'KH_SDT': form.get('KH_SDT'),
                    'DIA_CHI': form.get('DIA_CHI'),
                    'THANH_PHO': int(form.get('THANH_PHO')),
                    'MST': form.get('MST'),
                    'WEBSITE': form.get('WEBSITE'),
                    'FAX': form.get('FAX'),
                    'STK_NGAN_HANG': form.get('STK_NGAN_HANG'),
                    'TEN_CHU_TK_NGAN_HANG': form.get('TEN_CHU_TK_NGAN_HANG'),
                    'TEN_NGAN_HANG': form.get('TEN_NGAN_HANG'),
                    'DAI_DIEN_PHAT_LUAT': form.get('DAI_DIEN_PHAT_LUAT'),
                    'QUY_MO': int(form.get('QUY_MO')),
                    'LINH_VUC': int(form.get('LINH_VUC')),
                    'IS_NANG_CAP': IS_NANG_CAP,
                    'TIME_TAO_AT': Timer.get_timestamp_now(),
                    'IS_XOA': 0,
                })
            except Exception as e:
                return jsonify(
                    {'status': 'NOK', 'msg': 'Thêm mới không thành công!', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Thêm mới thành công khách hàng' + str(form.get('KH_TEN')),'idkh':idmax + 1})


class Detail(Resource):
    def get(self, id):
        item = db.find({'id': int(id)})[0]
        data = []
        data.append({'id': item['id'],
                     'KH_TEN': item['KH_TEN'],
                     'KH_EMAIL': item['KH_EMAIL'],
                     'KH_LOAI': item['KH_LOAI'],
                     'TIME_TAO_AT': item['TIME_TAO_AT'],
                     'KH_SDT': item['KH_SDT'],
                     'DIA_CHI': item['DIA_CHI'],
                     'THANH_PHO': item['THANH_PHO'],
                     'MST': item['MST'],
                     'WEBSITE': item['WEBSITE'],
                     'FAX': item['FAX'],
                     'DAI_DIEN': [],
                     'DAI_DIEN_PHAT_LUAT': item['DAI_DIEN_PHAT_LUAT'],
                     'LINH_VUC': item['LINH_VUC'],
                     'QUY_MO': item['QUY_MO'],
                     'IS_NANG_CAP': item['IS_NANG_CAP'],
                     'IS_XOA': item['IS_XOA'],
                     })
        return jsonify({'status': 'OK', 'data': data})

    def post(self, id):
        try:
            form = request.form
            IS_NANG_CAP = 0
            if form.get('IS_NANG_CAP', 'off') == '1':
                IS_NANG_CAP = 1
            db.update_one(
                {"id": int(id)},
                {"$set": {'KH_TEN': form.get('KH_TEN'),
                          'KH_EMAIL': form.get('KH_EMAIL'),
                          'KH_LOAI': int(form.get('LOAI_KH')),
                          'KH_SDT': form.get('KH_SDT'),
                          'DIA_CHI': form.get('DIA_CHI'),
                          'THANH_PHO': int(form.get('THANH_PHO')),
                          'MST': form.get('MST'),
                          'WEBSITE': form.get('WEBSITE'),
                          'FAX': form.get('FAX'),
                          'STK_NGAN_HANG': form.get('STK_NGAN_HANG'),
                          'TEN_CHU_TK_NGAN_HANG': form.get('TEN_CHU_TK_NGAN_HANG'),
                          'TEN_NGAN_HANG': form.get('TEN_NGAN_HANG'),
                          'DAI_DIEN_PHAT_LUAT': form.get('DAI_DIEN_PHAT_LUAT'),
                          'QUY_MO': int(form.get('QUY_MO')),
                          'LINH_VUC': int(form.get('LINH_VUC')),
                          'IS_NANG_CAP': IS_NANG_CAP,
                          }})
        except Exception as e:
            return jsonify(
                {'status': 'NOK', 'msg': 'Chỉnh sửa không thành công khách hàng: ', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Chỉnh sửa thành công khách hàng: ' + str(form.get('KH_TEN', ''))})
class Del(Resource):
    def post(self,id):
        try:
            if id != '':
                db.update_one(
                    {"id": int(id)},
                    {"$set": {"IS_XOA": 1,
                              'TIME_UPDATE_AT': Timer.get_timestamp_now(),
                              }})
        except Exception as e:
            return jsonify({'status': 'NOK', 'msg': 'Xóa không thành công!', 'string_error': str(e)})
        return jsonify({'status': 'OK', 'msg': 'Xóa thành công!'})


