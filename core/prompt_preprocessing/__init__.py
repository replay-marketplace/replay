from .prompt_preprocessing import preprocess_prompt

def preprocess_prompt(input_file: str, output_dir: str) -> None:
    """
    Process a text file containing prompts and create a JSON file with the processed prompts.
    
    Args:
        input_file (str): Path to the input text file
        output_dir (str): Directory where the output JSON file will be saved
    """
    from .prompt_preprocessing import preprocess_prompt as _preprocess_prompt
    return _preprocess_prompt(input_file, output_dir)

__all__ = ['preprocess_prompt'] 