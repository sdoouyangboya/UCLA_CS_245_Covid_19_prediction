from network import *
from build_data import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
import os
import csv
import json
import argparse

"""
# Train
model = Net(learning_rate=learning_rate)
for i in range(0, epochs):
    for j in range(0, Adj.shape[0], batch_size):
        metrics = model.train([Adj[j:j+batch_size], X[j:j+batch_size]], y[j:j+batch_size])
        print(metrics)
        os.system('clear')
        #print(scaler.inverse_transform(np.reshape(metrics["loss"], (1,-1))),
         #     scaler.inverse_transform(np.reshape(metrics["mse"], (1, -1))))
"""

def train_model(training_data, validation_data, hparams):
    """
    Function trains the model.
    args:
      training_data: List [Adj, X, y].
      validation_data: List [Adj, X, y]
      hparams: jsonfile
    """
    Adj, X, y = training_data
    batch_size = hparams["batch_size"]
    epochs = hparams["epoch"]
    learning_rate = hparams["learning_rate"]
    lossfile = hparams["lossfile"]
    checkpoint = hparams["checkpoint"]
    model = Net(learning_rate=learning_rate)
    if os.path.isfile(checkpoint):
        # Model exists
        model = load_model(Adj[0], X[0], learning_rate, checkpoint)
    else:
        model = Net(learning_rate=learning_rate)
    if os.path.isfile(lossfile):
        os.remove(lossfile)
    with open(lossfile, 'w', newline='') as csvfile:
        loss_writer = csv.writer(csvfile, delimiter=',')
        loss_writer.writerow(["Epoch", "MSE", "VMSE"])
        for i in range(0, epochs):
            epoch_mse = []
            for j in range(0, Adj.shape[0], batch_size):
                metrics = model.train([Adj[j:j+batch_size], X[j:j+batch_size]], y[j:j+batch_size])
                mse = metrics["mse"]
                epoch_mse.append(mse)
                print("epoch: {}, mse: {}".format(i, mse))
                loss_out = scaler.inverse_transform(np.reshape([mse], (-1, 1)))
                loss_out = [i, loss_out[0][0]]
                loss_writer.writerow(loss_out)
                # Validation ? 
            print("epoch: {}, Average_mse: {}, Validation_mse: ?".format(i, sum(epoch_mse)/len(epoch_mse)))
            loss_out = scaler.inverse_transform(
                np.reshape([sum(epoch_mse)/len(epoch_mse)], (-1, 1)))
            loss_out = [i, 0, loss_out[0][0]]
            loss_writer.writerow(loss_out)
    model.save_weights(checkpoint)
    return

def load_model(Adj, X, learning_rate, checkpoint):
    model = Net(learning_rate=learning_rate)
    _ = model([Adj, X])
    print(checkpoint)
    model.load_weights(checkpoint)
    return model

def predict(Adj, X, states, hparams, forecast_days=5):
    """
    Function makes forecasts
    args:
      Adj: Numpy matrix. [x, x]
      X: Numpy array, [x, y]
      forecast_days: int. Number of days to forecast
    returns:
      
    """
    checkpoint = hparams["checkpoint"]
    forecastfile = hparams["forecastfile"]
    learning_rate=1
    if os.path.isfile(checkpoint):
        # Model exists
        model = load_model(Adj[0], X[0], learning_rate, checkpoint)
    else:
        model = Net()
    # Assuming A doesnt change much
    Adj = Adj[-1]
    X = X[-1]
    print(Adj.shape)
    print(X.shape)
    forecast = []
    for i in range(0, forecast_days):
        y = model([Adj, X])
        X = np.concatenate((X[1:,:,:],
                            np.expand_dims(y,0)), axis=0)
        forecast.append(scaler.inverse_transform(y))
    if os.path.isfile(forecastfile):
        os.remove(forecastfile)
    with open(forecastfile, 'w', newline='') as csvfile:
        forecastWriter = csv.writer(csvfile, delimiter=',')
        forecastWriter.writerow(['Day']+states)
        for i in range(0,len(forecast)):
            forecastWriter.writerow(
                [1]+forecast[i].T.tolist()[0])
    return forecast



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train/Predict Neural Network")
    parser.add_argument("--Run", type=str,
                        help="""(Train|Forecast). Passing 'Train' will train the neural network. 
                        Passing 'Forecast' will make a forecast with existing neural network. 
                        Specify the model location in hparams.json""")
    args = parser.parse_args()


    scaler = MinMaxScaler()
    with open("hparams.json", "r") as f:
        hparams = json.load(f)
    feature_window = hparams["feature_window"]
    network_window = hparams["network_window"]

    # Load Data
    data = build_data(scaler, feature_window, network_window)
    print("ADJ: ", data[0].shape)
    print("X: ", data[1].shape)
    print("Y: ", data[2].shape)
    # Reform the data for 6 days
    Adj = data[0]
    X = data[1]
    y = data[2]
    states = data[3]
    print(Adj.shape)
    print(Adj[-1].shape)
    print(X[-1].shape)
    
    Adj, X, y = shuffle(Adj, X, y, random_state=0)
    if args.Run == "Train":
        train_model([Adj, X, y], [], hparams)
    elif args.Run == "Forecast":
        predict(Adj, X, states, hparams)
    else:
        print("Invalid Argument Passed")
