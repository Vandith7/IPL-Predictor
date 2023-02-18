import uvicorn
from fastapi import FastAPI
from IPLScore import IPL_Match
from IPL import IPL_match
import numpy as np
import pandas as pd
import pickle

app=FastAPI()

pickle_in=open("score.pkl","rb")
classifier=pickle.load(pickle_in)

pickle_inn=open("pipe.pkl","rb")
classifier_w=pickle.load(pickle_inn)

@app.get('/')
def index():
    return{'message':'This is IPL Score Predictor'}

@app.post('/predict_score')
def predict_score(data:IPL_Match):
    data=data.dict()
    temp_array = list()
    batting_team = data['batting_team']
    if batting_team == 'Chennai Super Kings':
        temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
    elif batting_team == 'Delhi Capitals':
        temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
    elif batting_team == 'Kings XI Punjab':
        temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
    elif batting_team == 'Kolkata Knight Riders':
        temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
    elif batting_team == 'Mumbai Indians':
        temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
    elif batting_team == 'Rajasthan Royals':
        temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
    elif batting_team == 'Royal Challengers Bangalore':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
    elif batting_team == 'Sunrisers Hyderabad':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]

    bowling_team = data['bowling_team']
    if bowling_team == 'Chennai Super Kings':
        temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
    elif bowling_team == 'Delhi Capitals':
        temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
    elif bowling_team == 'Kings XI Punjab':
        temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
    elif bowling_team == 'Kolkata Knight Riders':
        temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
    elif bowling_team == 'Mumbai Indians':
        temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
    elif bowling_team == 'Rajasthan Royals':
        temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
    elif bowling_team == 'Royal Challengers Bangalore':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
    elif bowling_team == 'Sunrisers Hyderabad':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]
    overs=data['overs']
    runs=data['runs']
    wickets=data['wickets']
    runs_in_prev_5=data['runs_in_prev_5']
    wickets_in_prev_5=data['wickets_in_prev_5']
    temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
    prediction_data = np.array([temp_array])
    my_prediction=int(classifier.predict(prediction_data)[0])
    lower_limit=my_prediction-10
    upper_limit=my_prediction+5
    result=[lower_limit,upper_limit]
    return {
        'lower_limit':lower_limit,
        'upper_limit':upper_limit
    }


@app.post('/predict')
def predict_win(data1:IPL_match):
    data1=data1.dict()
    temp_array = list()
    batting_team = data1['batting_team']

    bowling_team = data1['bowling_team']

    total_runs_x=data1['total_runs_x']
    score=data1['score']
    wickets=data1['wickets']
    overs=data1['overs']
    runs_left=total_runs_x-score
    balls_left=120-(overs*6)
    wickets=10-wickets
    crr=score/overs
    rrr=(runs_left*6)/balls_left
    input_df=pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[total_runs_x],'crr':[crr],'rrr':[rrr]})
    result=classifier_w.predict_proba(input_df)
    loss=result[0][0]
    win=result[0][1]
    return {
        'win':round(win*100),
        'loss':round(loss*100)
    }
if __name__=='__main__':
    uvicorn.run(app)