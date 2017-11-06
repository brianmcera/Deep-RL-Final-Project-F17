# To get started, copy over hyperparams from another experiment.
# Visit rll.berkeley.edu/gps/hyperparams.html for documentation.

""" Hyperparameters for Laika Reinforcement Learning experiment. """
from __future__ import division

from datetime import datetime
import os.path

import numpy as np

from gps import __file__ as gps_filepath
from gps.agent.ros.agent_ros import AgentROS
from gps.algorithm.algorithm_traj_opt import AlgorithmTrajOpt
from gps.algorithm.cost.cost_fk import CostFK
from gps.algorithm.cost.cost_action import CostAction
from gps.algorithm.cost.cost_sum import CostSum
from gps.algorithm.cost.cost_state import CostState
from gps.algorithm.dynamics.dynamics_lr import DynamicsLR
from gps.algorithm.traj_opt.traj_opt_lqr_python import TrajOptLQRPython
from gps.algorithm.policy_opt.policy_opt_tf import PolicyOptTf
from gps.algorithm.traj_opt.traj_opt_lqr_python import TrajOptLQRPython
from gps.algorithm.policy.lin_gauss_init import init_lqr
from gps.algorithm.policy.policy_prior_gmm import PolicyPriorGMM
from gps.gui.target_setup_gui import load_pose_from_npz
from gps.gui.config import generate_experiment_info
from gps.algorithm.policy_opt.tf_model_example import tf_network

SENSOR_DIMS = {
    'POSITIONS': 9*3,
    'VELOCITIES': 9*3,
    'ORIENTATIONS': 9*3,
    'ANGULAR ACCELERATIONS': 9*3,
    'ACTION': 32 + 4, #32 CABLES AND 4 MOTORS ON THE LEGS
}

BASE_DIR = '/'.join(str.split(gps_filepath, '/')[:-2])
EXP_DIR = BASE_DIR + '/../experiments/Laika_Test/'

common = {
    'experiment_name': 'my_experiment' + '_' + \
            datetime.strftime(datetime.now(), '%m-%d-%y_%H-%M'),
    'experiment_dir': EXP_DIR,
    'data_files_dir': EXP_DIR + 'data_files/',
    'target_filename': EXP_DIR + 'target.npz',
    'log_filename': EXP_DIR + 'log.txt',
    'conditions': 1,
}

if not os.path.exists(common['data_files_dir']):
    os.makedirs(common['data_files_dir'])
   
x0s = []
#ee_tgts = []
high_number = 1e3
state_tgts = [];
for i in range(9):
    state_tgts = np.append(state_tgts,[high_number]) #positive X direction
    state_tgts = np.append(state_tgts,[np.zeros((1,11))]) #don't care about other states
reset_conditions = []

agent = {
    'type': AgentROS,
    'dt': 0.05,
    'conditions': common['conditions'],
    'T': 100,
    'x0': x0s,
    'ee_points_tgt': ee_tgts,
    'reset_conditions': reset_conditions,
    'sensor_dims': SENSOR_DIMS,
    'state_include': [JOINT_ANGLES, JOINT_VELOCITIES, END_EFFECTOR_POINTS,
                      END_EFFECTOR_POINT_VELOCITIES],
    'end_effector_points': EE_POINTS,
    'obs_include': [],
}

algorithm = {
    'type': AlgorithmTrajOpt,
    'conditions': common['conditions'],
    'iterations': 10,
}

algorithm['init_traj_distr'] = {
    'type': init_lqr,
    'init_gains':  1.0 / PR2_GAINS,
    'init_acc': np.zeros(SENSOR_DIMS[ACTION]),
    'init_var': 1.0,
    'stiffness': 0.5,
    'stiffness_vel': 0.25,
    'final_weight': 50,
    'dt': agent['dt'],
    'T': agent['T'],
}

torque_cost = {
    'type': CostAction,
    'wu': 5e-3 / PR2_GAINS,
}

algorithm['cost'] = {
    'type': CostSum,
    'costs': [torque_cost, fk_cost1, fk_cost2],
    'weights': [1.0, 1.0, 1.0],
}

algorithm['dynamics'] = {
    'type': DynamicsLRPrior,
    'regularization': 1e-6,
    'prior': {
        'type': DynamicsPriorGMM,
        'max_clusters': 20,
        'min_samples_per_cluster': 40,
        'max_samples': 20,
    },
}

algorithm['traj_opt'] = {
    'type': TrajOptLQRPython,
}

algorithm['policy_opt'] = {}

config = {
    'iterations': algorithm['iterations'],
    'common': common,
    'verbose_trials': 0,
    'agent': agent,
    'gui_on': True,
    'algorithm': algorithm,
    'num_samples': 5,
}

common['info'] = generate_experiment_info(config)
