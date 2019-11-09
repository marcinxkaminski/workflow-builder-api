from ml.components.WorkflowElement import WorkflowElement

from os.path import isfile
from re import match
from termcolor import colored

FILE = 'End.py'
OPTIONAL = True
NAME = 'END'
DESCRIPTION = 'Validates filepaths and prints end message'
MATERIAL_ICON = 'stop'
REQUIREMENTS = ['termcolor==1.1.0']

_MESSAGE = 'FINITO! \n Your results are in: {} \n'


class End(WorkflowElement):
    def __init__(self):
        super().__init__(
            name=NAME,
            description=DESCRIPTION,
            materialIcon=MATERIAL_ICON,
            optional=OPTIONAL,
            requirements=REQUIREMENTS,
            config={
                'data': {
                    'output': 'your_results_output',
                }
            }
        )

    def _is_filepath_valid(self, filepath: str) -> bool:
        return match('^((\w:/)|//|/|./|\.\./)?(\w+/)*(\w+\.\w+)$', filepath) and filepath

    def _is_filepath_valid_and_exists(self, filepath: str) -> bool:
        return self._is_filepath_valid(filepath=filepath) and isfile(filepath)

    def _create_message(self, output: str) -> str:
        return _MESSAGE.format(output)

    def _print_message(self, message: str):
        color = 'yellow'
        separator = colored('================================================\n', color)
        final_message = colored(message, color)
        print(separator, final_message, separator)

    def main(self, input=None, output=None, delimiter=',', **kwargs):
        """
        Validates output filepath and prints end message.
        **input**: filepath to the input (unuseful here)
        **output**: filepath to the output
        **kwargs**: any other useful params
        """
        if not (self._is_filepath_valid_and_exists(filepath=output)):
            raise FileExistsError

        self._print_message(message=self._create_message(output=output))

    def quick_main(self, data: dict) -> dict:
        """
        Validates output filepath and returns exemplary end message.
        **data**: data for fast processing, defined in the config of the workflow element
        **returns**: dict with result in it
        """
        result = {'data': ''}

        out_fp = data.get('output', '')

        if not (self._is_filepath_valid(filepath=out_fp)):
            result['data'] = 'Files paths\' must be valid'
        else:
            result['data'] = self._create_message(output=out_fp)

        return result
