# To get started, copy over hyperparams from another experiment.
# Visit rll.berkeley.edu/gps/hyperparams.html for documentation.

""" Hyperparameters for Laika Reinforcement Learning experiment. """
from __future__ import division

from datetime import datetime
import os.path

import numpy as np

from gps import __file__ as gps_filepath
from gps.agent.ros.agent_laika_ros import AgentLaikaROS
from gps.algorithm.algorithm_traj_opt import AlgorithmTrajOpt
from gps.algorithm.algorithm_mdgps import AlgorithmMDGPS
from gps.algorithm.cost.cost_state import CostState
from gps.algorithm.dynamics.dynamics_prior_gmm import DynamicsPriorGMM
from gps.algorithm.dynamics.dynamics_lr_prior import DynamicsLRPrior
from gps.algorithm.traj_opt.traj_opt_lqr_python import TrajOptLQRPython
from gps.algorithm.policy_opt.policy_opt_tf import PolicyOptTf
from gps.algorithm.policy.lin_gauss_init import init_lqr
from gps.algorithm.policy.policy_prior_gmm import PolicyPriorGMM
from gps.gui.target_setup_gui import load_pose_from_npz
from gps.gui.config import generate_experiment_info
from gps.proto.gps_pb2 import BODY_STATES, CABLE_RL, ACTION
from gps.algorithm.policy_opt.tf_model_example import tf_network
#WHERE IS THE TF POLICY IMPORTED?

SENSOR_DIMS = {
    BODY_STATES: 108,
    CABLE_RL: 32,
    ACTION: 36, #32 CABLES AND 4 MOTORS ON THE LEGS
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
    'iterations':1,
}

if not os.path.exists(common['data_files_dir']):
    os.makedirs(common['data_files_dir'])

agent = {
    'type': AgentLaikaROS,
    'dt': 0.002,
    'conditions': common['conditions'],
    'T': 100,
    'substeps': 1,
    'state_size' : 140,
    'x0': [np.zeros(140)], #debug: change later
    'sensor_dims': SENSOR_DIMS,
    'state_include': [BODY_STATES,CABLE_RL],
    'obs_include': [BODY_STATES,CABLE_RL],
}

algorithm = {
    'type': AlgorithmMDGPS,
    'conditions': common['conditions'],
    'iterations': 12,
    'kl_step': 1.0,
    'min_step_mult': 0.5,
    'max_step_mult': 3.0,
    'policy_sample_mode': 'replace',
}

algorithm['init_traj_distr'] = {
    'type': init_lqr,
    'init_gains':  np.ones(SENSOR_DIMS[ACTION]),
    'init_acc': np.zeros(SENSOR_DIMS[ACTION]),
    'init_var': 1.0,
    'stiffness': 0.5,
    'stiffness_vel': 0.25,
    'final_weight': 50,
    'dt': agent['dt'],
    'T': agent['T'],
}


algorithm['cost'] = {
    'type': CostState,
    'data_types' : {
        BODY_STATES: {
            'wp': np.ones(108),
            'target_state': np.ones(108)*100,
        },
        CABLE_RL: {
            'wp': np.ones(32),
            'target_state': np.ones(32)*100,
        },
    },
    'alpha': 1e-2,
    'l1':0,
    'l2':1.0,
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

algorithm['policy_opt'] = {
    'type': PolicyOptTf,
    'network_params': {
        'obs_include': [BODY_STATES, CABLE_RL],
        'obs_vector_data': [BODY_STATES, CABLE_RL],
        'sensor_dims': SENSOR_DIMS,
        'n_layers': 2,
        'dim_hidden': [100, 100],
    },
    'network_model': tf_network,
    'iterations': 1000,
    'weights_file_prefix': EXP_DIR + 'policy',
}

algorithm['policy_prior'] = {
    'type': PolicyPriorGMM,
    'max_clusters': 20,
    'min_samples_per_cluster': 40,
    'max_samples': 40,
}

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
