import numpy as np
from scipy import sparse
import tensorflow as tf
import spektral
from spektral.layers.ops import sp_matrix_to_sp_tensor


class Net(tf.keras.Model):
    def __init__(self,
                 window=6,
                 lstm_output=52,
                 dropout=.5,
                 batch_size=24,
                 learning_rate=1e-3, **kwargs):
        """
        Initializes a network
        args:
          Window: int. Window of days.
          lstm_output: int. Number of units to the LSTM layer. Output of lstm
          dropout: float. Probabiltiy of dropout.
          batch_size: int. Size of the batch for training
        Training: 500 epocs, batchsize 8, Adam optimizer, LR 10-3
        returns:
          None
        """
        super().__init__(**kwargs)
        self._nets = {}
        self._window = window
        self._batch_size = batch_size
        for i in range(1,window+1):
            self.build_MPNN_unit(dropout, str(i))
        self.LSTM1 = tf.keras.layers.LSTM(lstm_output, return_sequences=True)
        self.LSTM2 = tf.keras.layers.LSTM(lstm_output, return_state=True)
        self.Lin = tf.keras.layers.Dense(1, activation="relu")
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        #self.loss_tracker = tf.keras.metrics.Mean(name="loss") Don't need for batchsize 1
        self.mse_metric = tf.keras.metrics.MeanSquaredError(name="mse")

    def build_MPNN_unit(self, dropout, net_id=1):
        """
        Function builds an MPNN unit
        args:
          dropout: float. Probabiltiy of dropout.
          net_id: int. Id of the network.
        return:
          None
        """
        L1 = []
        L1.extend((
            spektral.layers.MessagePassing(aggregate='mean',
                                          activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(dropout)))
        L2 = []
        L2.extend((
            spektral.layers.MessagePassing(aggregate='sum',
                                           activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(dropout)))
        self._nets[net_id] = (L1, L2)


    def run_MPNN_unit(self, Adj, X, net_id=1):
        """
        Function calls layer given by id
        args:
          Adj: Tensor. [:, x, y]. Adjacency matrix of the graph
          X: Tensor. [:, x, z]. Node feature matrix.
        returns:
          Tensor. [x, z*2]. ouput of passig a message through the MPNN
        """
        L1, L2 = self._nets[net_id]
        Adj = sp_matrix_to_sp_tensor(Adj)
        y = None
        for i in range(0,len(L1)):
            if i == 0: # MessagePassing layer
                y = L1[i].propagate(X, Adj)
                continue
            y = L1[i](y)
        H1 = y
        for i in range(0, len(L2)):
            if i == 0: # MessagePassing Layer
                y = L2[i].propagate(y, Adj)
                continue
            y = L2[i](y)
        H2 = y
        return tf.concat((H1,H2), axis=1)

    def train(self, model_input, y):
        """
        Function Trains the network
        args:
          model_input: [Adj, X]
            Adj: Tensor. [:, x, x]. Adjacency matrix of the graph
            X: Tensor. [:, x, z]. Node feature matrix
          y: Tensor. [x, 1]
        returns:
        """
        Adj, X = model_input
        Adj = tf.squeeze(
            tf.convert_to_tensor(Adj, dtype=tf.float32))
        X = tf.convert_to_tensor(X[0], dtype=tf.float32)
        y = tf.convert_to_tensor(y[0], dtype=tf.float32)
        with tf.GradientTape() as tape:
            y_pred = self((Adj, X), training=True)
            loss = tf.keras.losses.mean_squared_error(y, y_pred)

        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # metrics
        # self.loss_tracker.update_state(loss)
        self.mse_metric.update_state(y, y_pred)
        # return {"loss": self.loss_tracker.result().numpy(),
        return {"mse": self.mse_metric.result().numpy()}
    
    def call(self, model_input, training=True):
        """
        Function calls the net
        args:
          Adj: Tensor. [:, x, y]. Adjacency matrix of the graph
          X: Tensor. [:, x, z]. Node feature matrix
        returns:
          x: Tensor. [x, 1]. Output of the neural net
        """
        Adj, X = model_input
        if not training:
            Adj = sp_matrix_to_sp_tensor(Adj)
        LSTM_input = []
        for i in range(0, self._window):
            LSTM_input.append(
                self.run_MPNN_unit(Adj[i,:,:],
                                   X[i,:,:], net_id=str(i+1)))
        x = tf.stack(LSTM_input, axis=1)
        x = self.LSTM1(x)
        output, final_memory_state, final_carry_state = self.LSTM2(x)
        #x = X+x
        #Lin?
        x = final_memory_state
        x = self.Lin(x)
        return x
