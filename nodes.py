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
                "prompt": ("STRING", {"forceInput": True, "multiline": True}),
                "matrix_prompt": ("STRING", {"multiline": True}),
                "delimiter": ("STRING", {"default": "|"}),
                "put_at_start": ("BOOLEAN", {"default": True}),
            }
        }
    
    TITLE = "Matrix prompt list"
    RETURN_TYPES = ("LIST", "LIST", "STRING", "LIST", "INT", "INT",)
    RETURN_NAMES = ("base_prompts", "full_prompts", "row_prompts", "combination_count", "row_count", "column_count", )
    OUTPUT_IS_LIST = (True, True, False, False, False, False,)
    FUNCTION = "run"
    CATEGORY = "utils"

    def run(self, prompt: str, matrix_prompt: str, delimiter: str, put_at_start: bool, ):
        
        # credit goes to automatic1111 for this code
        # https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/scripts/prompt_matrix.py#L73
        prompt = prompt.strip()
        matrix_prompt = matrix_prompt.strip()

        if put_at_start == False and prompt[-1] == ',':
             prompt = prompt[:-1]
        
        matrix_prompt_concat = prompt + delimiter + matrix_prompt

        all_prompts = []
        all_base_prompts = []
        prompt_matrix_parts = matrix_prompt_concat.split(delimiter)
        combination_count = 2 ** (len(prompt_matrix_parts) - 1)
        for combination_num in range(combination_count):
            selected_prompts = [text.strip().strip(',') for n, text in enumerate(prompt_matrix_parts[1:]) if combination_num & (1 << n)]
            all_base_prompts.append(','.join(selected_prompts))

            if put_at_start:
                selected_prompts = selected_prompts + [prompt_matrix_parts[0]]
            else:
                selected_prompts = [prompt_matrix_parts[0]] + selected_prompts
            all_prompts.append(','.join(selected_prompts))
        
        
        # https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/images.py#L36
        #row count
        row_count = math.floor(math.sqrt(combination_count))
        while combination_count % row_count != 0:
            row_count -= 1
        # print(row_count)

        #column count
        column_count = math.ceil(combination_count / row_count)
        # print(column_count)
        
        #prompts for rows
        # row_prompts = " |a|b|a,b\nc|a,c|b,c|a,b,c"
        #"|a|b|a,b\nc|a,c|b,c|a,b,c"
        #"|a||b||a|b||\nc|a|c|b|c|a|b|c|\n
        row_prompts = ""
        
        x = 0
        while x < combination_count:
            print(x)
            for n in range(x, column_count + x):
                print(n)
                print(all_prompts[n])
                row_prompts += all_prompts[n]
                if n < column_count + x - 1:
                    row_prompts += delimiter
            row_prompts += "\n"
            x += column_count
        print(row_prompts)

        
        return (all_base_prompts, all_prompts, row_prompts, combination_count, row_count, column_count, )