import numpy as np
from cost_functions import trajectory_cost_fn
import time

class Controller():
	def __init__(self):
		pass

	# Get the appropriate action(s) for this state(s)
	def get_action(self, state):
		pass


class RandomController(Controller):
	def __init__(self):
		print('Initializing random controller...')
		rl_high = 12 #kept for now, but useless since the checks will happen on NTRT side
		rl_low = 5
		torque_high = 5
		torque_low = -5
		n_cables = 32
		n_legs = 4
		self.action_high = np.concatenate((rl_high*np.ones(n_cables),torque_high*np.ones(n_legs)))
		self.action_low = np.concatenate((rl_low*np.ones(n_cables),torque_low*np.ones(n_legs)))
		self.ac_dim = 36
                self.cable_motor_vel = 0.15 
                self.dt = 0.002
                self.num_cables = n_cables

	def get_action(self, state):
		#action = self.action_low+np.random.uniform(size=self.ac_dim)*(self.action_high-self.action_low)
                print((np.random.randint(-1,2,self.num_cables)))
                print((self.action_low[self.num_cables:]+np.random.uniform(size=self.ac_dim-self.num_cables)*(self.action_high-self.action_low)[self.num_cables:]))
                print(type(self.ac_dim-self.num_cables))
                action = np.concatenate((np.random.randint(-1,2,self.num_cables),self.action_low[self.num_cables:]+np.random.uniform(size=(self.ac_dim-self.num_cables))*(self.action_high-self.action_low)[self.num_cables:]))
		return action

class MPCcontroller(Controller):
	""" Controller built using the MPC method outlined in https://arxiv.org/abs/1708.02596 """
	def __init__(self,
				 dyn_model,
				 horizon=5,
				 cost_fn=None,
				 num_simulated_paths=10,
				 ):
		print('Initializing MPC controller...')
		self.dyn_model = dyn_model
		self.horizon = horizon
		self.cost_fn = cost_fn
		self.num_simulated_paths = num_simulated_paths
		self.ac_dim = 36
		self.obs_dim = 108

		rl_high = 12
		rl_low = 5
		torque_high = 5
		torque_low = -5
		n_cables = 32
		n_legs = 4
		self.action_high = np.concatenate((rl_high*np.ones(n_cables),torque_high*np.ones(n_legs)))
		self.action_low = np.concatenate((rl_low*np.ones(n_cables),torque_low*np.ones(n_legs)))
                self.cable_motor_vel = 0.15 #m/s
                self.num_cables = n_cables
                
	def get_action(self, state):
		# Broadcast state for batch calculations
		batch_state = np.tile(state,(self.num_simulated_paths,1))
		best_traj = None
		state_traj = batch_state[np.newaxis,:]

		for i in range(self.horizon):
			# Sample actions
			#batch_action = self.action_low+np.random.uniform(size=(self.num_simulated_paths,self.ac_dim))*(self.action_high-self.action_low)
                        batch_action = np.concatenate((np.random.randint(-1,2,(self.num_simulated_paths,self.num_cables)),self.action_low[self.num_cables:]+np.random.uniform(size=(self.num_simulated_paths,self.ac_dim-self.num_cables))*(self.action_high-self.action_low)[self.num_cables:]),axis=1)
			# Simulate dynamics from NN model
			batch_state = self.dyn_model.predict(batch_state,batch_action)
			# Add next state batch to trajectory
			state_traj = np.vstack((state_traj,batch_state[np.newaxis,:]))
			# Add actions to sequence
			if i == 0:
				action_seq = batch_action[np.newaxis,:]
			else:
				action_seq = np.vstack((action_seq,batch_action[np.newaxis,:]))

		s_t_traj = state_traj[0:self.horizon,:,:]
		s_tp1_traj = state_traj[1:self.horizon+1,:,:]
		traj_cost = trajectory_cost_fn(self.cost_fn,s_t_traj,action_seq,s_tp1_traj)
		best_traj = np.argmin(traj_cost)

		# Get best action
		best_action = action_seq[0,best_traj,:].reshape((self.ac_dim))
		return best_action
		""" Note: be careful to batch your simulations through the model for speed """
