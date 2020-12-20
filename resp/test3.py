from flask import Flask,request
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

first_init = True
df = pd.DataFrame([])

#####

save_file_name = 'test_no1.csv'

####


def add_data(buy,sell,symbol,curr_time):
    global df
    index= len(df)
    for i,symbol_t in enumerate(symbol):
        df.at[index,'time_stamp'] = curr_time
        df.at[index,"%s_buy"%symbol_t] = buy[i]
        df.at[index,"%s_sell"%symbol_t] = sell[i]
        
    if len(df)%10==0:
        df.to_csv(save_file_name,index=False,sep='\t')

@app.route("/test/", methods = ['POST'])
def test():
    all_data = request.data
    #print("DATA", request.data)
    curr_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    buy,sell,symbol = all_data.decode("utf-8").split("],[")
    buy = [float(x) for x in list(buy[2:].split(","))]
    sell = [float(x) for x in list(sell.split(","))]
    symbol = [str(x[1:-1]) for x in list(symbol[:-2].split(","))]
    
    add_data(buy,sell,symbol,curr_time)
    
    return '', 200        
 

if __name__ == "__main__":
    app.run()
