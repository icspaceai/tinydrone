import tensorflow as tf
from keras import backend as K


def hard_mining_mse(k):
    """
    Compute MSE for steering evaluation and hard-mining for the current batch.
    # Arguments
        k: number of samples for hard-mining.
    # Returns
        custom_mse: average MSE for the current batch.
    """

    def custom_mse(y_true, y_pred):
        # Parameter t indicates the type of experiment
        t = y_true[:,0]

        # Number of steering samples
        samples_steer = tf.cast(tf.equal(t,1), tf.int32)
        n_samples_steer = tf.reduce_sum(samples_steer)

        if n_samples_steer == 0:
            return 0.0
        else:
            # Predicted and real steerings
            pred_steer = tf.squeeze(y_pred, axis=-1)
            true_steer = y_true[:,1]

            # Steering loss
            l_steer = tf.multiply(t, K.square(pred_steer - true_steer))

            # Hard mining
            k_min = tf.minimum(k, n_samples_steer)
            _, indices = tf.nn.top_k(l_steer, k=k_min)
            max_l_steer = tf.gather(l_steer, indices)
            hard_l_steer = tf.divide(tf.reduce_sum(max_l_steer), tf.cast(k,tf.float32))

            return hard_l_steer

    return custom_mse



def hard_mining_entropy(k):
    """
    Compute binary cross-entropy for collision evaluation and hard-mining.
    # Arguments
        k: Number of samples for hard-mining.
    # Returns
        custom_bin_crossentropy: average binary cross-entropy for the current batch.
    """

    def custom_bin_crossentropy(y_true, y_pred):
        # Parameter t indicates the type of experiment
        t = y_true[:,0]

        # Number of collision samples
        samples_coll = tf.cast(tf.equal(t,0), tf.int32)
        n_samples_coll = tf.reduce_sum(samples_coll)

        if n_samples_coll == 0:
            return 0.0
        else:
            # Predicted and real labels
            pred_coll = tf.squeeze(y_pred, axis=-1)
            true_coll = y_true[:,1]

            # Collision loss
            l_coll = tf.multiply((1-t), K.binary_crossentropy(true_coll, pred_coll))

            # Hard mining
            k_min = tf.minimum(k, n_samples_coll)
            _, indices = tf.nn.top_k(l_coll, k=k_min)
            max_l_coll = tf.gather(l_coll, indices)
            hard_l_coll = tf.divide(tf.reduce_sum(max_l_coll), tf.cast(k, tf.float32))

            return hard_l_coll

    return custom_bin_crossentropy
