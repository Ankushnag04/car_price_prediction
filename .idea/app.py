from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('price_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')
@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        km_driven=int(request.form['km_driven'])
        mileage=float(request.form['mileage'])
        engine=int(request.form['engine'])
        max_power=float(request.form['max_power'])
        years_driven =2021- float(request.form['years_driven'])


        fuel_Petrol=request.form['fuel_Petrol']
        if (fuel_Petrol=='Petrol'):
            fuel_Petrol=1
            fuel_Diesel=0
            fuel_LPG=0
        elif (fuel_Petrol=='Diesel'):
            fuel_Petrol = 0
            fuel_Diesel = 1
            fuel_LPG = 0
        else:
            fuel_Petrol = 0
            fuel_Diesel = 0
            fuel_LPG = 1

        seller_type_Individual=request.form['seller_type_Individual']
        if (seller_type_Individual=='Individual'):
            seller_type_Individual=1
            seller_type_Trustmark_Dealer=0
        else:
            seller_type_Individual = 0
            seller_type_Trustmark_Dealer = 1

        transmission_Manual=request.form['transmission_Manual']
        if transmission_Manual=='Mannual':
            transmission_Manual=1
        else:
            transmission_Manual=0

        owner_Second_Owner=request.form['owner_Second_Owner']
        if owner_Second_Owner=='Second_Owner':
            owner_Second_Owner=1
            owner_Fourth_and_Above_Owner=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
        elif owner_Second_Owner=='Fourth_&_Above_Owner':
            owner_Second_Owner = 0
            owner_Fourth_and_Above_Owner = 1
            owner_Test_Drive_Car = 0
            owner_Third_Owner = 0
        elif owner_Second_Owner=='Test_Drive_Car':
            owner_Second_Owner = 0
            owner_Fourth_and_Above_Owner = 0
            owner_Test_Drive_Car = 1
            owner_Third_Owner = 0
        else:
            owner_Second_Owner = 0
            owner_Fourth_and_Above_Owner = 0
            owner_Test_Drive_Car = 0
            owner_Third_Owner = 1
        prediction = model.predict([[km_driven, mileage, engine, max_power, years_driven,fuel_Diesel,fuel_LPG,fuel_Petrol,seller_type_Individual,
                                     seller_type_Trustmark_Dealer,transmission_Manual,owner_Fourth_and_Above_Owner,owner_Second_Owner,
                                     owner_Test_Drive_Car,owner_Third_Owner]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at 'INR {}'".format(output))

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)










