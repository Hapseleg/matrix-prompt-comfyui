#  Package Modules
import os
from typing import Union, BinaryIO, Dict, List, Tuple, Optional
import time
import itertools
import math
#  ComfyUI Modules
import folder_paths
from comfy.utils import ProgressBar

#  Your Modules
#from .modules.calculator import CalculatorModel


#  Basic practice to get paths from ComfyUI
custom_nodes_script_dir = os.path.dirname(os.path.abspath(__file__))
custom_nodes_model_dir = os.path.join(folder_paths.models_dir, "my-custom-nodes")
custom_nodes_output_dir = os.path.join(folder_paths.get_output_directory(), "my-custom-nodes")


#  These are example nodes that only contains basic functionalities with some comments.
#  If you need detailed explanation, please refer to : https://docs.comfy.org/essentials/custom_node_walkthrough

class MatrixPromptList:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "STRING": ("STRING", {"multiline": True}),
                "delimiter": ("STRING", {"default": "|"}),
                "put_at_start": ("BOOLEAN", {"default": True})
            }
        }
    
    TITLE = "Matrix prompt list"
    RETURN_TYPES = ("STRING", "LIST", "INT", "INT", "INT")
    RETURN_NAMES = ("STRING", "LIST", "length", "column_count", "row_count")
    OUTPUT_IS_LIST = (True, False, False, False, False,)
    FUNCTION = "run"
    CATEGORY = "utils"

    def run(self, STRING: str, delimiter: str, put_at_start: bool):
        
        # credit goes to automatic1111 for this code
        # https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/scripts/prompt_matrix.py#L73
        
        all_prompts = []
        prompt_matrix_parts = STRING.split(delimiter)
        combination_count = 2 ** (len(prompt_matrix_parts) - 1)
        for combination_num in range(combination_count):
            selected_prompts = [text.strip().strip(',') for n, text in enumerate(prompt_matrix_parts[1:]) if combination_num & (1 << n)]
            if put_at_start:
                selected_prompts = selected_prompts + [prompt_matrix_parts[0]]
            else:
                selected_prompts = [prompt_matrix_parts[0]] + selected_prompts

            all_prompts.append(delimiter.join(selected_prompts))
        
        
        # https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/images.py#L36
        rows = math.floor(math.sqrt(combination_count))
        print(rows)

        while combination_count % rows != 0:
            rows -= 1
        print(rows)
        cols = math.ceil(combination_count / rows)
        print(cols)
        
        return (all_prompts, all_prompts, combination_count, cols, rows)