from abc import abstractmethod
from uuid import uuid4

FILE = 'EmptyWorkflowElement.py'
CLASSNAME = 'WorkflowElement'
OPTIONAL = False


class WorkflowElement():
    def __init__(self, name, description='', materialIcon='', optional=True, requirements=[], config={}):
        """
        Initializes Workflow Element.
        It assings id to the element and allows to set it's name, description, icon and config.
        **name**: name of the workflow element
        **description**: description of the workflow element
        **materialIcon**: icon which could describe this workflow element
        :config: config**: info required by the workflow element. Could contain "data" property for the "fast" method.
        """
        self.id = uuid4()
        self.name = name
        self.description = description
        self.materialIcon = materialIcon
        self.config = config

    @abstractmethod
    def main(self, input: str = None, output: str = None, delimiter=',', **kwargs):
        """
        Main method for this Workflow Element.
        It should handle all needed operation on the input file and it's data and save it to output file.
        While there are some operations that doesn't require any input/output files you could omit them and
        save it anywhere else, but remember that other Worklow Elements will not be noticed about this file.
        **input**: path to the input file
        **output**: path to the output file
        """
        raise NotImplementedError

    @abstractmethod
    def quick_main(self, data: dict) -> dict:
        """
        Handles fast operations on data. Should be "demo"/"trial" version of the main method.
        Usually it could be used for online purposes and operations. It should be fast and as simple as possible.
        This is optional function and if you don't want to use it just don't specify the "data" property
        in config of this object.
        However to allow user to use it you MUST specify "data" property in config e.g. config = {"data": {"ekg": []}}
        **data**: dictionary with all necessary for this Workflow Element data (e.g. list of EKG data).
        """
        pass
