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
		self.action_high = np.concatenate((12*np.ones(32),10*np.ones(4)))
		self.action_low = np.concatenate((5*np.ones(32),-10*np.ones(4)))
		self.ac_dim = 36

	def get_action(self, state):
		action = self.action_low+np.random.uniform(size=self.ac_dim)*(self.action_high-self.action_low)
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
		self.action_high = np.concatenate((12*np.ones(32),10*np.ones(4)))
		self.action_low = np.concatenate((5*np.ones(32),-10*np.ones(4)))

	def get_action(self, state):
		# Broadcast state for batch calculations
		batch_state = np.tile(state,(self.num_simulated_paths,1))
		best_traj = None
		state_traj = batch_state[np.newaxis,:]

		for i in range(self.horizon):
			# Sample actions
			batch_action = self.action_low+np.random.uniform(size=(self.num_simulated_paths,self.ac_dim))*(self.action_high-self.action_low)
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
