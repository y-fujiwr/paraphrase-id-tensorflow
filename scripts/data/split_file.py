import argparse
import logging
import os
import random


logger = logging.getLogger(__name__)


def main():
    argparser = argparse.ArgumentParser(
        description=("Split a file from the Kaggle Quora dataset "
                     "into train and validation files, given a validation "
                     "proportion"))
    argparser.add_argument("validation_proportion", type=float,
                           help=("Proportion of data in the input file "
                                 "to randomly split into a separate "
                                 "validation file. Value in [0, 1.0)"))
    argparser.add_argument("test_proportion", type=float,
                           help=("Proportion of data in the input file "
                                 "to randomly split into a separate "
                                 "test file. Value in [0, 1.0)"))
    argparser.add_argument("input_file_path", type=str,
                           help=("The path to the cleaned "
                                 "dataset file to split."))
    argparser.add_argument("output_dir_path", type=str,
                           help=("The *folder* to write the "
                                 "split files to"))
    config = argparser.parse_args()

    validation_proportion = config.validation_proportion
    test_proportion = config.test_proportion
    input_file_path = config.input_file_path
    output_dir_path = config.output_dir_path

    split_dataset(input_file_path, output_dir_path, test_proportion, validation_proportion)


def split_dataset(input_file_path, output_dir_path, test_proportion, validation_proportion, shuffle=False):
    if validation_proportion + test_proportion >= 1.0:
        logger.error("Validation + Test proportion should be less than 1.0")
        return
    # Get the data
    logger.info("Reading file from: {}".format(input_file_path))
    with open(input_file_path) as f:
        reader = f.readlines()
        input_rows = list(reader)

    if shuffle:
        logger.info("Shuffling input csv.")
        # For reproducibility
        random.seed(0)
        # Shuffle csv_rows deterministically in place
        random.shuffle(input_rows)

    total_length = len(input_rows)
    num_validation_lines = int(total_length * validation_proportion)
    num_test_lines = int(total_length * test_proportion)

    train_start = num_validation_lines + num_test_lines
    input_filename_full = os.path.basename(input_file_path)
    input_filename, input_ext = os.path.splitext(input_filename_full)
    train_out_path = os.path.join(output_dir_path,
                                  "train" + input_ext)
    val_out_path = os.path.join(output_dir_path,
                                "val" + input_ext)
    test_out_path = os.path.join(output_dir_path,
                                 "test" + input_ext)

    logger.info("Writing train split output to {}".format(train_out_path))
    with open(train_out_path, "w") as f:
        f.writelines(input_rows[train_start:])
    logger.info("Writing validation split output to {}".format(val_out_path))
    with open(val_out_path, "w") as f:
        f.writelines(input_rows[:num_validation_lines])
    logger.info("Writing test split output to {}".format(test_out_path))
    with open(test_out_path, "w") as f:
        f.writelines(input_rows[num_validation_lines:train_start])


if __name__ == "__main__":
    logging.basicConfig(format=("%(asctime)s - %(levelname)s - "
                                "%(name)s - %(message)s"),
                        level=logging.INFO)
    main()
