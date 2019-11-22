from abc import abstractmethod
from uuid import uuid4

FILES = ['WorkflowElement.py']  # the first file MUST be the workflow element's file.
CLASSNAME = 'WorkflowElement'  # class name that will be imported and used in workflow
OPTIONAL = False  # if the element is optional or mandatory
NAME = 'WORKFLOW_ELEMENT'  # name displayed to the user
DESCRIPTION = 'Empty, exemplary workflow element'  # description displayed to the user
MATERIAL_ICON = ''  # icon displayed to the user
INDEPENDENT = False  # if this element uses results of previous elements or not
REQUIREMENTS = []  # if any requirements are needed, put them here


class WorkflowElement():
    def __init__(
            self,
            name=NAME,
            description=DESCRIPTION,
            materialIcon=MATERIAL_ICON,
            optional=OPTIONAL,
            requirements=REQUIREMENTS,
            filenames=FILES,
            classname=CLASSNAME,
            independent=INDEPENDENT,
            config={}):
        """
        Initializes Workflow Element.
        It assings id to the element and allows to set it's name, description, icon, config etc.
        **name**: name of the workflow element
        **description**: description of the workflow element
        **materialIcon**: icon which could describe this workflow element
        **optional**: if the workflow element is optional or mandatory and should always be added
        **requirements**: requirements used in the workflow element (avoid repeating the same requirements in modules)
        **filenames**: name of the file where this element is placed
        **classname**: class name of the workflow element
        :config: config**: info required by the workflow element. Could contain "data" property for the "fast" method.
        """
        self.id = str(uuid4())
        self.name = name
        self.description = description
        self.materialIcon = materialIcon
        self.optional = optional
        self.requirements = requirements
        self.filenames = filenames
        self.classname = classname
        self.independent = independent
        self.config = config

    @abstractmethod
    def main(self, input: str = None, output: str = None, delimiter=',', **kwargs):
        """
        Main method for this Workflow Element.
        It should handle all needed operation on the input file and it's data and save it to output file.
        While there are some operations that doesn't require any input/output files you could omit them and
        save it anywhere else, but remember that other Worklow Elements will not be noticed about this file.
        IMPORTANT: remember, that even if your element is independent, you should copy your input to output, because
                    another element could use this results. This allows you to avaid problems with passing the data.
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
