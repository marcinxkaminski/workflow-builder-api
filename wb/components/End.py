try:
    from WorkflowElement import WorkflowElement
except ModuleNotFoundError:
    from components.WorkflowElement import WorkflowElement

from termcolor import colored
from fp_helper import is_filepath_valid, is_filepath_valid_and_exists

FILES = ['End.py', 'fp_helper.py']
CLASSNAME = 'End'
OPTIONAL = True
NAME = 'END'
DESCRIPTION = 'Validates filepaths and prints end message'
MATERIAL_ICON = 'stop'
INDEPENDENT = True
REQUIREMENTS = ['termcolor==1.1.0']

_MESSAGE = 'FINITO! \n Your results are in: {}\n'


class End(WorkflowElement):
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
                    'output': 'your_results_output',
                }
            }
        )

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
        if not (is_filepath_valid_and_exists(filepath=output)):
            raise FileExistsError

        self._print_message(message=self._create_message(output=output))

    def quick_main(self, data: dict) -> str:
        """
        Validates output filepath and returns exemplary end message.
        **data**: data for fast processing, defined in the config of the workflow element
        **returns**: dict with result in it
        """
        out_fp = data.get('output', '')

        if not (is_filepath_valid(filepath=out_fp)):
            return 'Files paths\' must be valid'

        return self._create_message(output=out_fp)
