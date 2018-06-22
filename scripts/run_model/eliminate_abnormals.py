import os
import csv
import math
from subprocess import call
from shutil import copyfile
from scripts.run_model.run_siamese import construct_paths
from scripts.data.split_file import split_dataset

validation_proportion = 0.3
test_proportion = 0

config_file_path = '../../config/01_bcb_clone_and_fp_balanced_all.yml'
data_file_dir_template = '../../data/processed/bcb/clone_and_false_positives/balanced/all-balanced/{run_id}/'
model_name = 'eliminate_abnormal'

main_filename = 'main.csv'
train_filename = 'train.csv'
val_filename = 'val.csv'
test_filename = main_filename
better_main_filename = 'better.' + main_filename


def main(threshold=0.5):
    """This script train the model and check the prediction against the testing set.
    It removes the training data that is too different than the prediction.
    """

    init_data_file_dir = data_file_dir_template.format(run_id='00')
    abnormal_file_path = os.path.join(init_data_file_dir, 'abnormals.csv')

    previous_better_main_file_path = None
    step = 0
    with open(abnormal_file_path, 'w+') as afile:
        awriter = csv.writer(afile)

        while step < 100:
            run_id = str(step).zfill(2)

            print("Running run_id: {}".format(run_id))

            # Make new dir for this run if needed
            data_file_dir = data_file_dir_template.format(run_id=run_id)
            os.makedirs(data_file_dir, exist_ok=True)

            # Construct the paths for all kinds of files
            paths = construct_paths(model_name, run_id, data_file_dir, test_filename=test_filename)
            predictions_file_path = paths['predictions_file_path']

            current_main_file_path = os.path.join(data_file_dir, main_filename)
            is_current_main_file_exist = os.path.exists(current_main_file_path)
            # Copy main.csv file from the previous run
            if previous_better_main_file_path and not is_current_main_file_exist:
                print("Copying main file from previous run...")
                copyfile(previous_better_main_file_path, current_main_file_path)

            is_val_file_exist = os.path.exists(paths['val_file_path'])
            # print("Does validation file exist?: {}".format(is_val_file_exist))
            #  Split main.csv into (train, val).csv
            if not is_val_file_exist:
                print("Splitting main file...")
                split_dataset(current_main_file_path, data_file_dir, test_proportion, validation_proportion)

            is_model_trained = os.path.exists(paths['data_manager_pickle_file_path'])
            # print("data manager pickle file path: {}".format(paths['data_manager_pickle_file_path']))
            # print("is trained: {}".format(is_model_trained))

            # If the model is not trained yet.
            if not is_model_trained:
                # Train the model
                print("Start training...")
                run_script("train", run_id, data_file_dir, test_filename)

            is_predicted = os.path.exists(predictions_file_path)
            # print("prediction file path: {}".format(predictions_file_path))
            # print("is predicted: {}".format(is_predicted))

            # If the prediction file not generated yet
            if not is_predicted:
                # Predict with the trained models
                print("Start predicting...")
                run_script("predict", run_id, data_file_dir, test_filename)

            # Compare the test data with the predict data
            #  and remove those with large differences from the training set

            test_file_path = paths['test_file_path']
            better_main_file_path = os.path.join(data_file_dir, better_main_filename)

            print("Removing abnormal files...")
            with open(test_file_path) as tfile:
                treader = csv.reader(tfile)
                with open(predictions_file_path) as pfile:
                    preader = csv.reader(pfile)
                    with open(better_main_file_path, 'w') as bfile:
                        bwriter = csv.writer(bfile)
                        for row_orig, row_pred in zip(treader, preader):
                            ground_truth = float(row_orig[2])
                            predicted = float(row_pred[0])
                            new_row = row_orig + [predicted]
                            if math.fabs(ground_truth - predicted) > threshold:
                                # abnormal case
                                awriter.writerow(new_row)
                            else:
                                # better train file
                                bwriter.writerow(new_row)

            previous_better_main_file_path = better_main_file_path

            step += 1

            # Test with only N times of traverse
            if step >= 50:
                break


def run_script(mode, run_id, data_file_dir, test_filename):
    call(['python', 'run_siamese.py',
          mode,
          '--config_file={}'.format(config_file_path),
          '--model_name={}'.format(model_name),
          '--run_id={}'.format(run_id),
          '--data_file_dir={}'.format(data_file_dir),
          '--test_filename={}'.format(test_filename),
          ])


if __name__ == '__main__':
    main()
