import logging
import coloredlogs
import pandas
import numpy
import logging

from scipy import stats
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from multiprocessing import cpu_count
from joblib import Parallel, delayed
from argparse import ArgumentParser
from glob import glob

REQUIREMENTS = {
    'coloredlogs': None,
    'pandas': '0.24.2',
    'joblib': '',
    'scipy': '1.3.0',
    'scikit-learn': '0.21.1',
    'statsmodels': '0.9.0',
    'numpy': '1.16.3'
}


def dbscan(data, filepath):
    outlier_detection = DBSCAN(min_samples=1000, eps=50)
    clusters = outlier_detection.fit_predict(data)
    return bool(clusters)


def z_score(data, filepath):
    z = numpy.abs(stats.zscore(data))
    threshold = 3
    outliers = numpy.where(z > threshold)
    if (len(outliers) / len(data)) * 100 > 10:
        logging.warning(
            f"[over z-score threshold] {filepath} contained {len(outliers)} outliers, "
            f"above z-score threshold={threshold}"
        )


def irq(data, filepath):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    left = (data < (Q1 - 1.5 * IQR))
    right = (data > (Q3 + 1.5 * IQR))
    result = pandas.merge(left, right, on=['timestamp'])
    fauly_values = result[result.value_x | result.value_y]
    if (len(fauly_values) / len(data)) * 100 > 10:
        logging.warning(
            f"[over irq threshold] {filepath} contained {len(fauly_values)} values outside IRQ, "
            f"which is {round((len(fauly_values) / len(data)) * 100)}% of values"
        )
        return False
    return True


def same_values(data, filepath):
    counts = data['value'].value_counts()
    if numpy.any(counts > 0.5 * len(data['value'])):
        logging.warning(
            f"[over 50% same values] {filepath} contained {len(counts)} different values, "
            f"{round((counts.values[0] / len(data)) * 100, 2)}% of them was {counts.index[0]}"
        )
        return False
    return True


def two_sigma(data, filepath):
    mean = data.value.mean()
    std = data.value.std()
    left = (data.value < mean - 2 * std)
    right = (data.value > mean + 2 * std)
    result = pandas.merge(left, right, on=['timestamp'])
    fauly_values = result[result.value_x | result.value_y]
    if (len(fauly_values) / len(data)) * 100 > 10:
        logging.warning(
            f"[over two sigma threshold] {filepath} contained {len(fauly_values)} values outside two-sigma, "
            f"which is {round((len(fauly_values) / len(data)) * 100)}% of values"
        )
        return False
    return True


def isolation_forest(data, filepath):
    clf = IsolationForest(behaviour='new', max_samples=500, random_state=1, contamination='auto')
    preds = clf.fit_predict(data)
    outliers = numpy.unique(preds, return_counts=True)[1][0]
    if (outliers / len(data)) * 100 > 35:
        logging.warning(
            f"[isolation forest] {filepath} contained {outliers} values outside clusters in isolation forest, "
            f"which is {round((outliers / len(data)) * 100)}% of values"
        )


CHECKS = [
    same_values,
    z_score,
    irq,
    two_sigma,
    isolation_forest
]


# Main
def find_csvs(directory):
    return glob(directory, recursive=True)


def sanitize_input(dataframe):
    dataframe.set_index('timestamp', inplace=True)
    dataframe.rename(columns=lambda x: x.strip(), inplace=True)
    return dataframe


def check(i, file, files_to_process):
    logging.info("[%s/%s] processing %s", i, len(files_to_process), file)
    try:
        logging.debug("loading file contents")
        csv = sanitize_input(pandas.read_csv(file))

    except Exception as e:
        logging.warning("something is wrong with %s", file)
        logging.error(e)

    for check in CHECKS:
        check(csv, file)


def main(args):
    logging.basicConfig(filepath='faulty-records-search-'+args.output, level=logging.INFO)
    coloredlogs.install()
    files_to_process = find_csvs(args.directory)
    executor = Parallel(n_jobs=cpu_count(), backend='multiprocessing')
    tasks = [delayed(check)(i, file, files_to_process) for i, file in enumerate(files_to_process, 1)]
    executor(tasks)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-d', '--directory',
        help="Directory containing csv files with data",
        default="**/BITalino/*.csv"
    )

    parser.add_argument(
        '-o', '--output',
        help="Output file for results",
        default='faulty-records-search-report.txt'
    )

    args = parser.parse_args()
    main(args)
