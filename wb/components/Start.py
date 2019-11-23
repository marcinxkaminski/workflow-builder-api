try:
    from WorkflowElement import WorkflowElement
except ModuleNotFoundError:
    from components.WorkflowElement import WorkflowElement

try:
    from fp_helper import is_filepath_valid, is_filepath_valid_and_exists
except ModuleNotFoundError:
    from components.fp_helper import is_filepath_valid, is_filepath_valid_and_exists

from termcolor import colored
from shutil import copyfile


FILES = ["Start.py", "fp_helper.py"]
CLASSNAME = "Start"
OPTIONAL = True
NAME = "START"
DESCRIPTION = "Validates filepaths and prints start message"
MATERIAL_ICON = "play_arrow"
INDEPENDENT = True
REQUIREMENTS = ["termcolor==1.1.0"]

_MESSAGE = "WELCOME \n STARTING RUNNING YOUR WORKFLOW \n Data Input: {} \n Results Output: {}\n"


class Start(WorkflowElement):
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
                "data": {"input": "your_data_input", "output": "your_results_output",}
            },
        )

    def _create_message(self, input: str, output: str) -> str:
        return _MESSAGE.format(input, output)

    def _print_message(self, message: str):
        color = "green"
        separator = colored("================================================\n", color)
        final_message = colored(message, color)
        print(separator, final_message, separator)

    def main(self, input=None, output=None, delimiter=",", **kwargs):
        """
        Validates filepaths, copies input to output file and prints start message.
        **input**: filepath to the input
        **output**: filepath to the output
        **kwargs**: any other useful params
        """
        if not is_filepath_valid_and_exists(filepath=input):
            raise FileExistsError

        copyfile(input, output)

        if not is_filepath_valid_and_exists(filepath=output):
            raise FileExistsError

        self._print_message(message=self._create_message(input=input, output=output))

    def quick_main(self, data: dict) -> str:
        """
        Validates filepaths and returns exemplary start message.
        **data**: data for fast processing, defined in the config of the workflow element
        **returns**: dict with result in it
        """
        in_fp = data.get("input", "")
        out_fp = data.get("output", "")

        if not (
            is_filepath_valid(filepath=in_fp) and is_filepath_valid(filepath=out_fp)
        ):
            return "Files paths' must be valid"

        return self._create_message(input=in_fp, output=out_fp)
