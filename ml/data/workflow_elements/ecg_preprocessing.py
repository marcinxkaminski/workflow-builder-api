import main as mp
import csv
import datetime
import errno
import os
from glob import glob

import heartpy as hp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

REQUIREMENTS = {
    'numpy': '1.16.3',
    'heartpy': '1.2.4',
    'matplotlib': '3.1.1',
}


def get_signal_from_file_and_normalize(file_path, bits):
    csv_file = open(file_path, "r")
    values = []
    next(csv_file)
    startTimestamp = None
    for line in csv_file:
        if startTimestamp is None:
            startTimestamp = line.split(", ")[0]
        val = line.split(", ")[1]
        values.append(val)
    csv_file.close()
    values = list(map((lambda x: normalize_value(np.float64(x), bits)), values))
    return np.asarray(values, dtype=np.float64), startTimestamp


def normalize_value(adc, bits):
    vcc = 3.3
    gECG = 1100
    return 1000*(((adc/2**bits)-0.5)*vcc)/gECG


def get_BPM_and_HRV_save(path, raw_signal, sampling_rate, segment_width, output_path):
    working_data, measures = hp.process_segmentwise(raw_signal,
                                                    sample_rate=sampling_rate, segment_width=segment_width,
                                                    segment_overlap=0, segment_min_size=20)
    BPM = measures['bpm']
    HRV = measures['rmssd']

    new_file_bpm = "BPM_FROM_ECG.csv"
    new_file_hrv = "HRV_FROM_ECG.csv"
    new_column_name_bpm = 'BPM_in_given_time_interval'
    new_column_name_hrv = 'HRV_in_given_time_interval'

    write_to_file(new_file_bpm, new_column_name_bpm, path=path, values=BPM, output_path=output_path)
    write_to_file(new_file_hrv, new_column_name_hrv, path=path, values=HRV, output_path=output_path)

    return BPM, HRV


def count_lines(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i


def write_to_file(filename, new_column_name, path, values=None, output_path=None):
    new_path = output_path+filename
    num_of_records = count_lines(path)
    interval_length = int(num_of_records / len(values))
    interval_id = 0
    ctr = 0

    # file reading/writing
    f = open(new_path, "w+")
    f.write("timestamp, {}\n".format(new_column_name))
    raw_data_file = open(path, "r")
    reader = csv.reader(raw_data_file)
    next(reader)
    for i in range(num_of_records):
        if ctr == interval_length:
            interval_id += 1
            ctr = 0
        else:
            ctr += 1
        new_line = "{0}, {1}\n".format(next(reader)[0], values[interval_id])
        f.write(new_line)
    f.close()
    raw_data_file.close()


def printSummaryAndReport(BPM, HRV, start_timestamp, segment_width, input_path, output_path):
    f = openReportFile(output_path)

    bpm_data = {}
    hrv_data = {}
    current_timestamp = int(start_timestamp)
    for i in range(len(BPM)):
        bpm_data[current_timestamp] = BPM[i]
        hrv_data[current_timestamp] = HRV[i]
        current_timestamp = current_timestamp + segment_width * 1000

    f.write("Input file: {}\n".format(input_path))
    f.write("BPM \n\ntimestamp,humanReadableTime,bpm\n")
    for key in bpm_data:
        new_line = "{0},{1},{2}\n".format(key,
                                          datetime.datetime.utcfromtimestamp(key / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                                          bpm_data[key])
        f.write(new_line)

    f.write("\n\n\n\nHRV \n\ntimestamp,humanReadableTime,hrv\n")
    for key in hrv_data:
        new_line = "{0},{1},{2}\n".format(key,
                                          datetime.datetime.utcfromtimestamp(key / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                                          hrv_data[key])
        f.write(new_line)

    dates = matplotlib.dates.date2num(
        list(map(lambda x: (datetime.datetime.utcfromtimestamp(x / 1000)), list(bpm_data.keys()))))

    plt.subplot(2, 1, 1)
    plt.plot_date(dates, list(bpm_data.values()), 'o-')
    plt.title('BPM and HRV for inputFile {}'.format(input_path))
    plt.ylabel('BPM')

    plt.subplot(2, 1, 2)
    plt.plot_date(dates, list(hrv_data.values()), '.-')
    plt.xlabel('time')
    plt.ylabel('HRV')

    plt.savefig(output_path + 'chart.png')


def openReportFile(output_path):
    filename = output_path
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    f = open(filename, "w+")
    return f


def preprocess_ECG_signal_and_normalize(file_path, sampling_rate, segment_width, bits, output_path):
    raw, startTimestamp = get_signal_from_file_and_normalize(file_path, bits)
    BPM, HRV = get_BPM_and_HRV_save(file_path, raw, sampling_rate, segment_width, output_path)

    printSummaryAndReport(BPM, HRV, startTimestamp, segment_width, file_path, output_path)

    filtered = hp.filtersignal(raw, cutoff=[0.5, 20], sample_rate=sampling_rate, order=2, filtertype='bandpass')


def main(args):
    files_to_process = glob(args.directory, recursive=True)
    for i, file in enumerate(files_to_process, 1):
        preprocess_ECG_signal_and_normalize(
            file_path=args.input,
            sampling_rate=args.samplingRate,
            segment_width=args.segmentWidth,
            bits=args.bits,
            output_path=f'{i}ecg-preprocessing-{args.output}'
        )

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-d', '--directory',
        help="Directory containing csv files with data",
        type=str,
        default="**/BITalino/*.csv"
    )

    parser.add_argument(
        '-o', '--output',
        help="Output file for results",
        type=str,
        default='ecg-preprocessing.txt'
    )

    parser.add_argument(
        '-s', '--samplingRate',
        help='sampling rate in seconds',
        type=float,
        default=1000.0
        )

    parser.add_argument(
        '-w', '--segmentWidth',
        help='segment width in seconds',
        type=int,
        default=120
        )

    parser.add_argument(
        '-b', '--bits',
        help='the number of bits for each channel',
        type=int,
        default=6
        )

    args = parser.parse_args()
    main(args)
