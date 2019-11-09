from ml.components.WorkflowElement import WorkflowElement
import csv

FILE = 'Normalize.py'
OPTIONAL = True
NAME = 'NORMALIZE'
DESCRIPTION = 'Normalizes data'
MATERIAL_ICON = 'equalizer'
REQUIREMENTS = []


class Normalize(WorkflowElement):
    def __init__(self):
        super().__init__(
            name=NAME,
            description=DESCRIPTION,
            materialIcon=MATERIAL_ICON,
            optional=OPTIONAL,
            requirements=REQUIREMENTS,
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
                    if cols[idx]:
                        cols[idx].append(col)
                    else:
                        cols[idx] = col
        return cols

    def _normalize_columns(self, cols: dict) -> dict:
        normalized_cols = {}

        for idx, col in cols.items():
            normalized_cols[idx] = self._normalize(col)

        return normalized_cols

    def _save_cols_to_file(self, output: str, cols: dict):
        writer = csv.writer(open(output, 'w'))
        cols_keys = cols.keys()
        cols_val_count = len(cols[cols_keys[0]])

        for idx in cols_val_count:
            row = []
            for key in cols_keys:
                row.append(cols[key][idx])
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
            )
        )

    def quick_main(self, data: dict) -> dict:
        """
        Normalizes data from input arra/list and returns it
        **data**: data for fast processing, defined in the config of the workflow element
        **returns**: dict with result in it
        """
        result = {'data': ''}
        arr = data.get('values', '')

        result['data'] = self._normalize(arr)

        return result
