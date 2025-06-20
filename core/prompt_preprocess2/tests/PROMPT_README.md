User-facing Prompt Text Files:

prompt.txt files can contain the following "markers":

1. Template file or directory. 
Format: "/TEMPLATE path/file_or_dir"
MUST be the first line in the file. 
There can be zero or 1 of these within the prompt.txt. 

2. Agent prompts
Format: "/PROMPT text text text text text ..."
There MUST be at least 1 /PROMPT per file. 
On average 2-4 /PROMPTs

3. Read-only files or directories. 
Format "/RO source_path/source_file_or_dir"
There can be zero to N of these within the text of a prompt. 
These files will get copied into the replay_output directory 
