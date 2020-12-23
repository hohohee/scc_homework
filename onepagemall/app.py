from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def write_orders():
    color_receive = request.form['color_give']
    name_receive = request.form['name_give']
    number_receive = request.form['number_give']
    email_receive = request.form['email_give']

    # 2. DB에 정보 삽입하기
    order = {
        'color': color_receive,
        'name': name_receive,
        'number': number_receive,
        'email': email_receive
    }

    db.orders.insert_one(order)
    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '주문이 완료되었습니다.'})


@app.route('/order', methods=['GET'])
def read_orders():
    orders = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
