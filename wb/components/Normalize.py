try:
    from WorkflowElement import WorkflowElement
except ModuleNotFoundError:
    from components.WorkflowElement import WorkflowElement

import csv

FILES = ['Normalize.py']
CLASSNAME = 'Normalize'
OPTIONAL = True
NAME = 'NORMALIZE'
DESCRIPTION = 'Normalizes data'
MATERIAL_ICON = 'equalizer'
INDEPENDENT = False
REQUIREMENTS = []


class Normalize(WorkflowElement):
    def __init__(self):
        super().__init__(
            name=NAME,
            description=DESCRIPTION,
            materialIcon=MATERIAL_ICON,
            optional=OPTIONAL,
            requirements=REQUIREMENTS,
            filenames=FILES,
            classname=CLASSNAME,
            independent=INDEPENDENT,
            config={
                'data': {
                    'values': [],
                }
            }
        )

    def _normalize(self, arr: list) -> list:
        return [(float(i)-min(arr))/(max(arr)-min(arr)) for i in arr]

    def _get_columns_from_file(self, input: str, delimiter: str) -> list:
        cols = {}
        with open(input) as csvfile:
            for row in csv.reader(csvfile, delimiter=delimiter):
                for idx, col in enumerate(row):
                    if cols.get(idx):
                        cols[idx].append(int(col))
                    else:
                        cols[idx] = [int(col)]
        return cols

    def _normalize_columns(self, cols: dict) -> dict:
        normalized_cols = {}

        for idx, col in cols.items():
            normalized_cols[idx] = self._normalize(col)

        return normalized_cols

    def _save_cols_to_file(self, output: str, cols: dict, delimiter: str = ','):
        writer = csv.writer(open(output, 'w'), delimiter=delimiter)
        cols_keys = list(cols)
        cols_val_count = len(cols.get(cols_keys[0]))

        for idx in range(cols_val_count):
            row = []
            for key in cols_keys:
                row.append(cols.get(key)[idx])
            writer.writerow(row)

    def main(self, input=None, output=None, delimiter=',', **kwargs):
        """
        Normalizes data from input file and saves it to output file
        **input**: filepath to the input
        **output**: filepath to the output
        **kwargs**: any other useful params
        """
        self._save_cols_to_file(
            output=output,
            cols=self._normalize_columns(
                cols=self._get_columns_from_file(
                    input=input,
                    delimiter=delimiter)
            ),
            delimiter=delimiter
        )

    def quick_main(self, data: dict) -> list:
        """
        Normalizes data from input arra/list and returns it
        **data**: data for fast processing, defined in the config of the workflow element
        **returns**: dict with result in it
        """
        arr = data.get('values', '')

        return self._normalize(arr)
