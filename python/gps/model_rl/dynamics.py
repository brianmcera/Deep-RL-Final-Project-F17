import tensorflow as tf
import numpy as np

# Predefined function to build a feedforward neural network
def build_mlp(input_placeholder,
              output_size,
              scope,
              n_layers=2,
              size=500,
              activation=tf.tanh,
              output_activation=None
              ):
    out = input_placeholder
    with tf.variable_scope(scope):
        for i in range(n_layers):
            out = tf.layers.dense(out, size, activation=activation, name='layer_'+str(i))
        out = tf.layers.dense(out, output_size, activation=output_activation, name='layer_out')
    return out

def shuffle(a, o):
    indicies = np.arange(o.shape[0])
    np.random.shuffle(indicies)

    a_shuf = a[indicies,:]
    o_shuf = o[indicies,:]

    return a_shuf, o_shuf

class NNDynamicsModel():
    def __init__(self,
                 n_layers,
                 size,
                 activation,
                 output_activation,
                 normalization,
                 batch_size,
                 iterations,
                 learning_rate,
                 sess
                 ):
        """ Note: Be careful about normalization """
        print('Initializing dynamics model...')
        obs_dim = 108
        ac_dim = 36

        self.normalization = normalization
        self.batch_size = batch_size
        self.iterations = iterations
        self.sess = sess

        # Create mlp, loss, and training op
        self.norm_obs_ac_ph = tf.placeholder(tf.float32,[None,obs_dim+ac_dim])
        self.norm_deltas_act = tf.placeholder(tf.float32,[None,obs_dim])
        self.norm_deltas_pred = build_mlp(self.norm_obs_ac_ph,obs_dim,'dyn_model',n_layers,size,activation,output_activation)
        self.loss = tf.losses.mean_squared_error(self.norm_deltas_pred,self.norm_deltas_act,scope='mse_loss')
        self.train_op = tf.train.AdamOptimizer(learning_rate).minimize(self.loss)

        # Define other parameters
        self.print_int = 100
        self.eps = 1e-6
        self.num_fit = 0

        self.model_dir = './models/'
        self.saver = tf.train.Saver()
        self.builder = tf.saved_model.builder.SavedModelBuilder('./models_builder')

    def fit(self, data):
        """
        Write a function to take in a dataset of (unnormalized)states, (unnormalized)actions, (unnormalized)next_states and fit the dynamics model going from normalized states, normalized actions to normalized state differences (s_t+1 - s_t)
        """
        # Extract data
        obs_t = data['obs_t']
        obs_tp1 = data['obs_tp1']
        acs_t = data['acs_t']
        deltas = obs_tp1-obs_t

        # Normalize data
        norm_obs_t = np.divide((obs_t-self.normalization['mean_obs']),(self.normalization['std_obs']+self.eps))
        norm_acs_t = np.divide((acs_t-self.normalization['mean_acs']),(self.normalization['std_acs']+self.eps))
        norm_deltas = np.divide((deltas-self.normalization['mean_deltas']),(self.normalization['std_deltas']+self.eps))

        # Create matricies for supervised learning_rate
        norm_obs_acs = np.concatenate((norm_obs_t,norm_acs_t),axis=1)

        # Shuffle data
        norm_obs_acs, norm_deltas = shuffle(norm_obs_acs,norm_deltas)

        batch_counter = 0
        n_data = norm_obs_acs.shape[0]
        n_batches = int(n_data/self.batch_size)

        self.sess.run(tf.global_variables_initializer())

        graph = tf.get_default_graph()
        t = graph.get_tensor_by_name('dyn_model/layer_0/kernel:0')
        print(t.eval(session=self.sess)[0,0])

        # Do learning, self.iterations is the number of epochs
        for i in range(self.iterations*(n_batches+1)):
            # Get batchs for inputs and labels
            start_pos = batch_counter*self.batch_size
            if batch_counter <= (n_batches-1):
                end_pos = (batch_counter+1)*self.batch_size
                batch_counter += 1
            else:
                end_pos = -1
                batch_counter = 0
            norm_obs_acs_batch = norm_obs_acs[start_pos:end_pos,:]
            norm_deltas_batch = norm_deltas[start_pos:end_pos,:]

            # Run training op
            self.sess.run(self.train_op,
                feed_dict={self.norm_obs_ac_ph:norm_obs_acs_batch,
                            self.norm_deltas_act:norm_deltas_batch})

            # Evaluate loss and print
            if i % self.print_int == 0 or i == self.iterations*(n_batches+1)-1:
                curr_loss = self.loss.eval(session=self.sess,
                    feed_dict={self.norm_obs_ac_ph:norm_obs_acs_batch,
                                self.norm_deltas_act:norm_deltas_batch})
                print('Iteration: %d, Loss: %g' % (i,curr_loss))

        model_name = self.model_dir + 'fitted_dynamics'
        save_path = self.saver.save(self.sess,model_name,global_step=self.num_fit)
        tf.train.write_graph(self.sess.graph,self.model_dir,'fitted_dynamics.pb',as_text=False)
        tf.train.write_graph(self.sess.graph,self.model_dir,'fitted_dynamics.pbtxt',as_text=True)

        # tf.add_to_collection('dyn_model',self.norm_deltas_pred)

        self.builder.add_meta_graph_and_variables(self.sess,['fitted_dynamics'])
        self.builder.save(as_text=False)
        self.builder.save(as_text=True)
        print('Saving dynamics NN parameters: ' + save_path)

        print(t.eval(session=self.sess)[0,0])

        self.num_fit += 1

        if self.num_fit == 1:
            exit()

    def predict(self, states, actions):
        """ Write a function to take in a batch of (unnormalized) states and (unnormalized) actions and return the (unnormalized) next states as predicted by using the model """
        # First normalize
        norm_states = np.divide((states-self.normalization['mean_obs']),(self.normalization['std_obs']+self.eps))
        norm_actions = np.divide((actions-self.normalization['mean_acs']),(self.normalization['std_acs']+self.eps))
        if len(states.shape) == 1:
            norm_obs_ac = np.append(norm_states,norm_actions).reshape((1,len(states)+len(actions)))
        else:
            norm_obs_ac = np.concatenate((norm_states,norm_actions),axis=1)

        # Use NN to predict normalized state change
        norm_deltas = self.sess.run(self.norm_deltas_pred,feed_dict={self.norm_obs_ac_ph:norm_obs_ac})

        # Denormalize and get state prediction
        deltas = self.normalization['mean_deltas']+np.multiply(self.normalization['std_deltas'],norm_deltas)
        next_states = states + deltas

        return next_states
