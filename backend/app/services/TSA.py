def closePriceHistory(df):
    import matplotlib.pyplot as plt
    plt.style.use("fivethirtyeight")
    
    #plt.figure(figsize=(16,8))
    plt.title("Close Price History")
    plt.plot(df["Close"])
    plt.xlabel("Date", fontsize=18)
    plt.ylabel("Close Price USD", fontsize=18)
    plt.savefig("output/PriceHistory.png", format="png")
    plt.close()
    
def ModelPricePred(df, ticker, data_source, start_date, predict_date):
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler
    from keras.models import Sequential
    from keras.layers import Dense, LSTM
    import math
    import matplotlib.pyplot as plt
    plt.style.use("fivethirtyeight")
    
    #Training Data
    data = df.filter(["Close"])
    dataset = data.values
    training_data_len = math.ceil(len(dataset) * 0.8)

    #Scaled Data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data[0:training_data_len , :]
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
        if i<= 61:
            print(x_train)
            print(y_train)
            print()

    #Convert to arrays
    x_train, y_train = np.array(x_train), np.array(y_train)

    #Reshape Data (3 Dim)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_train.shape

    #Build LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    #Compile model
    model1 = model.compile(optimizer="adam", loss="mean_squared_error")

    #Train model
    model.fit(x_train, y_train, batch_size=1, epochs=1)
    
    ####################################################################
    #Create test dataset
    
    #New array from containing scaled values from index 1543 to 2003
    test_data = scaled_data[training_data_len - 60: , :]
    #Create data sets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    #Convert data into numpy array
    x_test = np.array(x_test)

    #Reshape Data (3 Dim)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    x_test.shape

    #Get model predicted price values
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    #Get RMSE (root mean squared error)
    rmse = np.sqrt( np.mean( predictions - y_test )**2 )
    
    #Plot data
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid["Predictions"] = predictions

    #Visualize data
    plt.figure(figsize=(16,8))
    plt.title("Model")
    plt.xlabel("Date", fontsize=18)
    plt.xlabel("Close Price USD", fontsize=18)
    plt.plot(train["Close"])
    plt.plot(valid[["Close", "Predictions"]])
    plt.legend(["Train", "Validation", "Predictions"], loc="lower right")
    plt.savefig("output/ModelPrediction.png", format="png")
    plt.close()
    
    
    ###Predicted den Preis am Tag nach dem "predict_date" Datum### 
    import pandas_datareader as web
    #Get quote
    quote = web.DataReader(ticker, data_source=data_source, start=start_date, end=predict_date)
    #New dataframe
    new_df = quote.filter(["Close"])
    #Get the last 60 days closing prices and convert df to array
    last_60_days = new_df[-60:].values
    #Scale the data to be vals between 0 and 1
    last_60_days_scaled = scaler.transform(last_60_days)
    #Empty list
    X_test = []
    #Append
    X_test.append(last_60_days_scaled)
    #Convert X_test to numpy array
    X_test = np.array(X_test)
    #Reshape
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    #Get predicted scaled price
    pred_price = model.predict(X_test)
    #Undo scaling
    pred_price = scaler.inverse_transform(pred_price)
    return pred_price
    
def updatePNGsAndReturnPrediction(ticker = "GILD"):
    from datetime import datetime, timedelta
    currentTimeDate = datetime.now()
    valid_date = currentTimeDate.strftime('%Y-%m-%d') #today
    end_date = (currentTimeDate - timedelta(days=1)).strftime('%Y-%m-%d') #yesterday
    predict_date = (currentTimeDate + timedelta(days=1)).strftime('%Y-%m-%d') #tomorrow
    start_date = "2014-01-01"
    data_source = "yahoo"

    import pandas_datareader as web
    ###Korrekter Preis an dem Tag###
    df = web.DataReader(ticker, data_source=data_source, start=start_date, end=end_date)
    closePriceHistory(df)
    pred_price = ModelPricePred(df, ticker, data_source, start_date, predict_date)[0][0]
    valid_price = web.DataReader(ticker, data_source=data_source, start=valid_date, end=valid_date)["Close"][0]
    return [round(valid_price, 2), round(pred_price, 2)]


#return prediction value
#updates ModelPrediction.png, PriceHistory.png
    
#print(updatePNGsAndReturnPrediction())