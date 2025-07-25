import sys
import re

def main(in_file, new_op_name, out_file):
  with open(in_file, 'r') as f:
    contents = f.read()

  # replace {OP_NAME} with op we are trying to generate
  contents = re.sub('{{OP_NAME}}', new_op_name, contents)

  with open(out_file, 'w') as f:
    f.write(contents)

if __name__ == "__main__":
  in_file = sys.argv[1]
  new_op_name = sys.argv[2]
  out_file = sys.argv[3]
  main(in_file, new_op_name, out_file)
