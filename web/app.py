from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from web.customers import hello, Customer, Detail, Del
from custome_daidien import NDD, NDD_moi, Del_NDD

app = Flask(__name__)
api = Api(app)


api.add_resource(Customer, '/khach-hang')
api.add_resource(Detail, '/khach-hang/chi-tiet/<id>')
api.add_resource(Del, '/khach-hang/xoa/<id>')
api.add_resource(NDD, '/khach-hang/dai-dien/<id>')
api.add_resource(Del_NDD, '/khach-hang/dai-dien/xoa/<id>')
api.add_resource(NDD_moi, '/khach-hang/dai-dien-moi/<id>')
api.add_resource(hello, '/')
# api.add_resource(License.post, '/ban-quyen/them-moi')
# api.add_resource(Register, '/register')
# api.add_resource(Retrieve, '/retrieve')
# api.add_resource(Save, '/save')

CORS(app)
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

# client = MongoClient("mongodb://localhost:27017")
# db = client.ByteSave_Licenses
# users = db["Users"]
# license = db["Licenses"]
#
# """
# HELPER FUNCTIONS
# """
# def userExist(username):
#     if users.find({"Username": username}).count() == 0:
#         return False
#     else:
#         return True
# def verifyUser(username, password):
#     if not userExist(username):
#         return False
#
#     user_hashed_pw = users.find({
#         "Username": username
#     })[0]["Password"]
#
#     if bcrypt.checkpw(password.encode('utf8'), user_hashed_pw):
#         return True
#     else:
#         return False
#
#
# def getUserMessages(username):
#     # get the messages
#     return users.find({
#         "Username": username,
#     })[0]["Messages"]
#
#
# """
# RESOURCES
# """
#
# @api.representation('application/json')
# class License(Resource):
#     def get(self):
#         data = []
#         i = 0
#         try:
#             for item in license.find({'IS_XOA': {'$ne': 1}}):
#                 i = i + 1
#                 data.append({'STT': i,
#                              'id': item['id'],
#                              'MA_LICENSE': item['MA_LICENSE'],
#                              'TIME_TAO_AT': item['TIME_TAO_AT'],
#                              'TIME_UPDATE_AT': item['TIME_UPDATE_AT'],
#                              'TIME_HET_HAN': '',
#                              'ID_KH': item['ID_KH'],
#                              'THANG_NAM': item['THANG_NAM'],
#                              'SO_THANG_NAM': item['SO_THANG_NAM'],
#                              'TRANG_THAI': item['TRANG_THAI'],
#                              'SO_LUONG_MAY_SU_DUNG': item['SO_LUONG_MAY_SU_DUNG'],
#                              })
#         except Exception as e:
#             return jsonify({'data': [], 'string_error': str(e)})
#         return jsonify({'data': data})
#     def post(self):
#         if request.method == 'POST':
#             form = request.form
#             idd = form.get('idlicense', '')
#             if idd != '' and idd != None:
#                 try:
#                     license.update_one(
#                         {"id": idd},
#                         {"$set": {"ID_KH": form.get('ID_KH', ''),
#                                   "MA_LICENSE": form.get('MA_LICENSE', ''),
#                                   "TIME_HET_HAN": form.get('TIME_HET_HAN', ''),
#                                   "SO_THANG_NAM": form.get('SO_THANG_NAM', ''),
#                                   "THANG_NAM": form.get('THANG_NAM', ''),
#                                   "SO_LUONG_MAY_SU_DUNG": form.get('SO_LUONG_MAY_SU_DUNG', ''),
#                                   "SO_LUONG_MAY_SU_DUNG": form.get('SO_LUONG_MAY_SU_DUNG', ''),
#                                   }})
#                 except Exception as e:
#                     return jsonify(
#                         {'status': 'NOK', 'msg': 'Chỉnh sửa không thành công mã bản quyền', 'string_error': str(e)})
#                 return jsonify({'status': 'OK', 'msg': 'Chỉnh sửa thành công mã bản quyền'})
#             try:
#                 idmax = license.find().sort([("id", -1)])[0]['id'] if license.find().count() > 0 else 0
#                 license.insert({
#                     'id': idmax + 1,
#                     'ID_KH': int(form.get('ID_KH')),
#                     'MA_LICENSE': form.get('MA_LICENSE'),
#                     # 'TIME_HET_HAN': form.get('TIME_HET_HAN'),
#                     'SO_THANG_NAM': int(form.get('TIME_HET_HAN')),
#                     'THANG_NAM': int(form.get('Choisenamthang')),
#                     'SO_LUONG_MAY_SU_DUNG': int(form.get('SO_LUONG_MAY_SU_DUNG')),
#                     'TIME_TAO_AT': Timer.get_timestamp_now(),
#                     'TIME_UPDATE_AT': Timer.get_timestamp_now(),
#                     'TRANG_THAI': 0,
#                 })
#             except Exception as e:
#                 return jsonify(
#                     {'status': 'NOK', 'msg': 'Thêm mới không thành công mã bản quyền', 'string_error': str(e)})
#         return jsonify({'status': 'OK', 'msg': 'Thêm mới thành công mã bản quyền'})
#
#
#
# @api.representation('application/json')
# class Register(Resource):
#     def post(self):
#         # Get posted data from request
#         data = request.get_json()
#         username = data["username"]
#         password = data["password"]
#
#         # check if user exists
#         if userExist(username):
#             retJson = {
#                 "status": 301,
#                 "msg": "Invalid Username"
#             }
#             return jsonify(retJson)
#
#         # encrypt password
#         hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
#
#         # Insert record
#         users.insert({
#             "Username": username,
#             "Password": hashed_pw,
#             "Messages": []
#         })
#
#         # Return successful result
#         retJosn = {
#             "status": 200,
#             "msg": "Registration successful"
#         }
#         return jsonify(retJosn)
#
# @api.representation('application/json')
# class Retrieve(Resource):
#     def post(self):
#          # Get posted data from request
#         data = request.get_json()
#
#         # get data
#         username = data["username"]
#         password = data["password"]
#
#         # check if user exists
#         if not userExist(username):
#             retJson = {
#                 "status": 301,
#                 "msg": "Invalid Username"
#             }
#             return jsonify(retJson)
#
#         # check password
#         correct_pw = verifyUser(username, password)
#         if not correct_pw:
#             retJson = {
#                 "status": 302,
#                 "msg": "Invalid password"
#             }
#             return jsonify(retJson)
#
#         # get the messages
#         messages = getUserMessages(username)
#
#         # Build successful response
#         retJson = {
#             "status": 200,
#             "obj": messages
#         }
#
#         return jsonify(retJson)
#
# @api.representation('application/json')
# class Save(Resource):
#     def post(self):
#
#          # Get posted data from request
#         data = request.get_json()
#
#         # get data
#         username = data["username"]
#         password = data["password"]
#         message = data["message"]
#
#         # check if user exists
#         if not userExist(username):
#             retJson = {
#                 "status": 301,
#                 "msg": "Invalid Username"
#             }
#             return jsonify(retJson)
#
#         # check password
#         correct_pw = verifyUser(username, password)
#         if not correct_pw:
#             retJson = {
#                 "status": 302,
#                 "msg": "Invalid password"
#             }
#             return jsonify(retJson)
#
#         if not message:
#             retJson = {
#                 "status": 303,
#                 "msg": "Please supply a valid message"
#             }
#             return jsonify(retJson)
#
#         # get the messages
#         messages = getUserMessages(username)
#
#         # add new message
#         messages.append(message)
#
#         # save the new user message
#         users.update({
#             "Username": username
#         }, {
#             "$set": {
#                 "Messages": messages
#             }
#         })
#
#         retJson = {
#             "status": 200,
#             "msg": "Message has been saved successfully"
#         }
#         return jsonify(retJson)


