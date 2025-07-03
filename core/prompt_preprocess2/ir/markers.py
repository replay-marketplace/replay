# Front End parser: parse User input prompt.txt file markers
# ToDo: rensme to FE_MARKERS
FE_MARKERS = [    "/TEMPLATE",      # 1 Specify dir with files to seed code folder
                  "/PROMPT",        # 2 Specify LLM call
                  "/DOCS",          # 3 Specify dir with read only docs
                  "/RUN",           # 4 Specify CLI call
                  "/DEBUG_LOOP",    # 5 Lowered into a conditional loop 
                  "/EXIT"]          # 6 

# Markers within a node after the IR_MARKER parsing, that trigger second order effects
INTRA_NODE_MARKERS = ["/RO"] 