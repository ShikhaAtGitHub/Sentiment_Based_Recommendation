from flask import Flask, request, render_template, jsonify, json

import numpy as np
import pandas as pd
import pickle

user_final_rating = pd.read_pickle("models/user_final_rating.pkl")
df = pd.read_csv("models/df.csv")
word_vectorizer = pickle.load(
    open('models/word_vectorizer.pkl', 'rb'))
logit = pickle.load(
    open('models/logit_model.pkl', 'rb'))
# Few valid users: samantha, joshua, rebecca, 02dakota, 
def recommend(user_input):
    d = user_final_rating.loc[user_input].sort_values(ascending=False)[0:20]
    i= 0
    a = {}
    for prod_name in d.index.tolist():
        product_name = prod_name
        product_name_review_list =df[df['prod_name']== product_name]['Review'].tolist()
        features= word_vectorizer.transform(product_name_review_list)
        logit.predict(features)
        a[product_name] = logit.predict(features).mean()*100
    
    b= pd.Series(a).sort_values(ascending = False).head(5).index.tolist()
    return b

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        username = str(request.form.get('reviews_username'))
        if (user_final_rating.index == username).any():
            prediction = recommend(username)
            print("Output :", prediction)
            return render_template('index.html', data=prediction)
        else:
            return render_template('index.html', data2='Please enter valid user')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    print("Server Started")
    app.run(host="0.0.0.0", port=5001)
    # app.run(debug = True)