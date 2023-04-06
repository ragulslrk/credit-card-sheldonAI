from flask import *
app=Flask(__name__,template_folder='template',static_url_path='/static')
import  pickle
import pandas as  pd 
import numpy  as np  
import jwt
# defining the  function to   predict from the  model using  pkl file 
def predict_model(form):
    LIMIT_BAL=float(form['balance_limit'])
    print(LIMIT_BAL)
    #ml  model loading
    f= open('models/credit_rf','rb') 
    model=pickle.load(f)
    #converting to  dataframe
    pre_data=pd.DataFrame([[LIMIT_BAL,int(form['PAY_1']),int(form['PAY_2']),int(form['PAY_3']),int(form['PAY_4']),int(form['PAY_5']),int(form['PAY_6']),float(form['BILL_AMT1']),float(form['BILL_AMT2']),float(form['BILL_AMT3']),float(form['BILL_AMT4']),float(form['BILL_AMT5']),float(form['BILL_AMT6'])]],columns=['LIMIT_BAL','PAY_1','PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2','BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6'])

    print(pre_data)
    #Predicting
    result=model.predict(pre_data)
    print('final result: ',result[0])
    return result[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=="GET":
        return render_template('predict.html')
    elif request.method=="POST":
        output=predict_model(request.form)
        encoded_jwt = jwt.encode({"result": str(output),"name":request.form['client_name']}, "credit_card_default", algorithm="HS256")
        return  redirect(url_for('result',token=encoded_jwt))


@app.route('/result/<token>')
def result(token):
     token=jwt.decode(token,"credit_card_default", algorithms=["HS256"])
     print(token)
     if token['result'] == "0":
        msg=token['name']+" has predicted as a Credit Default Payer For Next Month."
        flag=1
     else:
        msg=token['name']+" has predicted as Not a Credit Default Payer For Next Month."
        flag=0

     print(msg)
     return render_template('result.html',msg=msg,flag=flag)
if __name__ =="__main__":
    app.run(debug=True)