import tensorflow as tf
import numpy as np

if __name__ == "__main__":
    with tf.Session() as sess:
        model_path = './models_builder'
        tf.saved_model.loader.load(sess,['fitted_dynamics'],model_path)

        graph = tf.get_default_graph()
        t = graph.get_tensor_by_name('dyn_model/layer_0/kernel:0')
        print(t.eval(session=sess)[0,0])
