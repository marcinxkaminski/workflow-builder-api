from ml.components.WorkflowElement import WorkflowElement

from os.path import isfile
from re import match
from termcolor import colored

FILE = 'Start.py'
OPTIONAL = True
NAME = 'START'
DESCRIPTION = 'Validates filepaths and prints start message'
MATERIAL_ICON = 'play_arrow'
REQUIREMENTS = ['termcolor==1.1.0']

_MESSAGE = 'WELCOME \n STARTING RUNNING YOUR WORKFLOW \n Data Input: {} \n Results Output: {} \n'


class Start(WorkflowElement):
    def __init__(self):
        super().__init__(
            name=NAME,
            description=DESCRIPTION,
            materialIcon=MATERIAL_ICON,
            optional=OPTIONAL,
            requirements=REQUIREMENTS,
            config={
                'data': {
                    'input': 'your_data_input',
                    'output': 'your_results_output',
                }
            }
        )

    def _is_filepath_valid(self, filepath: str) -> bool:
        return match('^((\w:/)|//|/|./|\.\./)?(\w+/)*(\w+\.\w+)$', filepath) and filepath

    def _is_filepath_valid_and_exists(self, filepath: str) -> bool:
        return self._is_filepath_valid(filepath=filepath) and isfile(filepath)

    def _create_message(self, input: str, output: str) -> str:
        return _MESSAGE.format(input, output)

    def _print_message(self, message: str):
        color = 'green'
        separator = colored('================================================\n', color)
        final_message = colored(message, color)
        print(separator, final_message, separator)

    def main(self, input=None, output=None, delimiter=',', **kwargs):
        """
        Validates filepaths and prints start message.
        **input**: filepath to the input
        **output**: filepath to the output
        **kwargs**: any other useful params
        """
        if not (self._is_filepath_valid_and_exists(filepath=input) and
                self._is_filepath_valid_and_exists(filepath=output)):
            raise FileExistsError

        self._print_message(
            message=self._create_message(
                input=input,
                output=output
            )
        )

    def quick_main(self, data: dict) -> dict:
        """
        Validates filepaths and returns exemplary start message.
        **data**: data for fast processing, defined in the config of the workflow element
        **returns**: dict with result in it
        """
        result = {'data': ''}

        in_fp = data.get('input', '')
        out_fp = data.get('output', '')

        if not (self._is_filepath_valid(filepath=in_fp) and
                self._is_filepath_valid(filepath=out_fp)):
            result['data'] = 'Files paths\' must be valid'
        else:
            result['data'] = self._create_message(input=in_fp, output=out_fp)

        return result
