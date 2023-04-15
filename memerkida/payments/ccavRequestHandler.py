

from flask import request, redirect, Flask, render_template
from .ccavutil import encrypt,decrypt
from .ccavResponseHandler import res
from string import Template
app = Flask('ccavRequestHandler') 

'''
Please put in the 32 bit alphanumeric key and Access Code in quotes provided by CCAvenues.
'''

accessCode = 'AVCB26KC33AF31BCFA' 	
workingKey = '832F1AB2BBC5E2C88D38808D538FCE9E'

@app.route('/')
def webprint():
    return render_template('dataFrom.html')

@app.route('/ccavResponseHandler', methods=['GET', 'POST'])
def ccavResponseHandler():
    plainText = res(request.form['encResp'])
    return plainText

@app.route('/ccavRequestHandler', methods=['GET', 'POST'])
def login():
	p_merchant_id = request.form['merchant_id']
	p_order_id = request.form['order_id']
	p_currency = request.form['currency']
	p_amount = request.form['amount']
	p_redirect_url = request.form['redirect_url']
	p_cancel_url = request.form['cancel_url']
	p_language = request.form['language']
	p_billing_name = request.form['billing_name']
	p_billing_address = request.form['billing_address']
	p_billing_city = request.form['billing_city']
	p_billing_state = request.form['billing_state']
	p_billing_zip = request.form['billing_zip']
	p_billing_country = request.form['billing_country']
	p_billing_tel = request.form['billing_tel']
	p_billing_email = request.form['billing_email']
	p_delivery_name = request.form['delivery_name']
	p_delivery_address = request.form['delivery_address']
	p_delivery_city = request.form['delivery_city']
	p_delivery_state = request.form['delivery_state']
	p_delivery_zip = request.form['delivery_zip']
	p_delivery_country = request.form['delivery_country']
	p_delivery_tel = request.form['delivery_tel']
	p_merchant_param1 = request.form['merchant_param1']
	p_merchant_param2 = request.form['merchant_param2']
	p_merchant_param3 = request.form['merchant_param3']
	p_merchant_param4 = request.form['merchant_param4']
	p_merchant_param5 = request.form['merchant_param5']
	p_promo_code = request.form['promo_code']
	p_customer_identifier = request.form['customer_identifier']
	
	

	merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+p_delivery_name+'&'+'delivery_address='+p_delivery_address+'&'+'delivery_city='+p_delivery_city+'&'+'delivery_state='+p_delivery_state+'&'+'delivery_zip='+p_delivery_zip+'&'+'delivery_country='+p_delivery_country+'&'+'delivery_tel='+p_delivery_tel+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&'
		
	encryption = encrypt(merchant_data,workingKey)

	html = '''\
<html>
<head>
	<title>Sub-merchant checkout page</title>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
</head>
<body>
<form id="nonseamless" method="post" name="redirect" action="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" > 
		<input type="hidden" id="encRequest" name="encRequest" value=$encReq>
		<input type="hidden" name="access_code" id="access_code" value=$xscode>
		<script language='javascript'>document.redirect.submit();</script>
</form>    
</body>
</html>
'''
	fin = Template(html).safe_substitute(encReq=encryption,xscode=accessCode)
			
	return fin	

#Host Server and Port Number should be configured here.

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000)



