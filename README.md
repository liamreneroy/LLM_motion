# LLM_motion
Codebase for generating expressive robot motion with a large language model (LLM aka GPT-4)

### Link to Research Paper
TBA


## Main Files
This codebase uses the framework as described in our submitted paper. In this implimentation, the GPT-4 model is used. The main files in this repo are:

### The Jupyter notebook used to generate the prompt and query the LLM:
https://github.com/liamreneroy/LLM_motion/blob/main/scripts/llm_to_motion.ipynb

### The prompt structure used to query the LLM:
https://github.com/liamreneroy/LLM_motion/blob/main/media/sample_prompt.txt

### Sample output from the LLM based on the prompt:
https://github.com/liamreneroy/LLM_motion/blob/main/media/sample_output.txt

### The task and robot description presented to users in our user study:
https://github.com/liamreneroy/LLM_motion/blob/main/media/task_description.txt

### The statistical analyses for our two hypotheses (H1, H2) are here:
https://github.com/liamreneroy/LLM_motion/blob/main/stats/

### All the raw data collected throughout our study is here:
https://github.com/liamreneroy/RL_audio/blob/main/data/


## Packages to Install:
pygame   (see this webpage ~ https://www.pygame.org/wiki/GettingStarted)  
jupyterlab, numpy, termcolor, openpyxl, nbconvert-webpdf, openai, wandb  


Either use:    
--> sudo apt-get install <package_name>  
--> python3 -m pip install <package_name>  
--> conda install -c conda-forge <package_name>  


Example using conda:  
--> conda install -c conda-forge <package_name>  

jupyterlab or notebook  
numpy  
termcolor  
openpyxl  
nbconvert-webpdf              
openai
wandb  


## Owner: 
Liam Rene Roy
Liamreneroy@gmail.com
Liam.roy@monash.edu