import razorpay
from flask import Flask, request, render_template
from werkzeug.exceptions import BadRequest

app = Flask(__name__, static_folder="static", static_url_path='', template_folder='templates')


@app.route('/order', methods=['GET'])
def create_order():
    params = request.args
    key_id = params.get('key_id')

    if key_id == None:
        return BadRequest()

    key_secret = params.get('key_secret')

    if key_secret == None:
        return BadRequest()

    razorpay_client = razorpay.Client(auth=(key_id, key_secret))
    DATA = {
        "amount": 500000,
        "currency": "INR"
    }
    response = razorpay_client.order.create(data=DATA)
    order_id = response.get('id')
    currency = response.get('currency')
    amount = response.get('amount')
    return render_template('app.html', key=key_id, secret=key_secret, amount=amount, currency=currency, order_id=order_id)


@app.route('/charge', methods=['POST'])
def app_charge():
    key_id = request.form['key_id']
    key_secret = request.form['key_secret']
    razorpay_client = razorpay.Client(auth=(key_id, key_secret))
    payment_id = request.form['razorpay_payment_id']
    order_id = request.form['razorpay_order_id']
    signature = request.form['razorpay_signature']
    parameters = {
        "razorpay_order_id": order_id,
        "razorpay_payment_id": payment_id,
        "razorpay_signature": signature
    }
    verified_signature = razorpay_client.utility.verify_payment_signature(parameters) # if verified_signature is None, the result is True
    if verified_signature == None:
        return render_template('thankyou.html')


if __name__ == '__main__':
    app.run()