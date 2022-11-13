import tensorflow as tf
import numpy as np
import utils
from model import dronet


def getModel(img_width, img_height, img_channels, output_dim):
    m = dronet(img_width, img_height, img_channels, output_dim)
    return m


def train(train_data, val_data, model, initial_epoch):
    # Initialize loss weights
    model.alpha = tf.Variable(1, trainable=False, name="alpha", dtype=tf.float32)
    model.beta = tf.Variable(0, trainable=False, name="beta", dtype=tf.float32)

    # Initialize number of samples for hard-mining
    model.k_mse = tf.Variable(32, trainable=False, name="k_mse", dtype=tf.int32)
    model.k_entropy = tf.Variable(32, trainable=False, name="k_entropy", dtype=tf.int32)

    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=1e-2, decay_steps=10000, decay_rate=1e-5
    )

    optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
    # Configure training process
    # TODD("Add training process config")
    model.compile(
        optimizer=optimizer,
        loss=[
            utils.hard_mining_mse(model.k_mse),
            utils.hard_mining_entropy(model.k_entropy),
        ],
        loss_weights=[model.alpha, model.beta],
    )
    # Train model
    steps_per_epoch = int(np.ceil(train_data.samples / 32))
    val_steps = int(np.ceil(val_data.samples / 32))

    model.fit_generator(
        train_data,
        epochs=1,
        steps_per_epoch=steps_per_epoch,
        validation_data=val_data,
        validation_steps=val_steps,
        initial_epoch=initial_epoch,
    )

    # Save the model in tflite format
    # Convert the model.
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the model.
    with open("model.tflite", "wb") as f:
        f.write(tflite_model)


def main():
    output_dim = 1
    img_mode = "grayscale"
    img_width = 320
    img_height = 240

    # Generate training data with real-time augmentation
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=0.2,
        rescale=1.0 / 255,
        width_shift_range=0.2,
        height_shift_range=0.2,
    )

    train_generator = train_datagen.flow_from_directory(
        "../training",
        shuffle=True,
        color_mode=img_mode,
        target_size=(img_width, img_height),
        batch_size=32,
    )

    val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

    val_generator = val_datagen.flow_from_directory(
        "../validation",
        shuffle=True,
        color_mode=img_mode,
        target_size=(img_width, img_height),
        batch_size=32,
    )

    model = getModel(img_width, img_height, 1, output_dim)

    train(train_generator, val_generator, model, 0)


if __name__ == "__main__":
    main()
