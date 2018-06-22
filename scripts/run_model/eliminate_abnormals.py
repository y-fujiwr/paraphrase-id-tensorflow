import os
import csv
from subprocess import call
from scripts.run_model.run_siamese import construct_paths

config_file_path = '../../config/01_bcb_clone_and_fp_balanced_all.yml'
data_file_dir_template = '../../data/processed/bcb/clone_and_false_positives/balanced/all-balanced/{run_id}/'

main_file = 'main.csv'
test_file_path = main_file
better_main_file = 'better.' + main_file


def main(threshold=0.5):
    """This script train the model and check the prediction against the testing set.
    It removes the training data that is too different than the prediction.
    """

    init_data_file_dir = data_file_dir_template.format(run_id='00')
    abnormal_file_path = os.path.join(init_data_file_dir, 'abnormals.csv')
    test_file = test_file_path

    step = 0
    with open(abnormal_file_path, 'w+') as afile:
        awriter = csv.writer(afile)

        while step < 100:
            run_id = str(step).zfill(2)

            data_file_dir = data_file_dir_template.format(run_id=run_id)
            os.makedirs(data_file_dir, exist_ok=True)

            model_name = 'eliminate-abnormal'
            paths = construct_paths(model_name, run_id, data_file_dir, test_file=test_file)

            # Train the model
            run_script("train", run_id, data_file_dir, test_file)

            # Predict with the trained models
            run_script("predict", run_id, data_file_dir, test_file)

            # Compare the test data with the predict data
            #  and remove those with large differences from the training set

            output_predictions_path = paths['output_predictions_path']
            test_file = paths['test_file']
            better_main_file_path = os.path.join(data_file_dir, better_main_file)

            with open(test_file) as tfile:
                treader = csv.reader(tfile)
                with open(output_predictions_path) as pfile:
                    preader = csv.reader(pfile)
                    with open(better_main_file_path, 'w') as bfile:
                        bwriter = csv.writer(bfile)
                        for row_orig, row_pred in zip(treader, preader):
                            ground_truth = float(row_orig[2])
                            predicted = float(row_pred[0])
                            if ground_truth - predicted > threshold:
                                # abnormal case
                                awriter.writerow(row_orig.extend(row_pred))
                            else:
                                bwriter.writewor(row_orig)

            # Generate the new training set, split into (train, val).csv

            step += 1
            break


def run_script(mode, run_id, data_file_dir, test_file):
    call(['python', 'run_siamese.py',
          mode,
          '--config_file={}'.format(config_file_path),
          '--run_id={}'.format(run_id),
          '--data_file_dir={}'.format(data_file_dir),
          '--test_file={}'.format(test_file),
          ])


if __name__ == '__main__':
    main()
