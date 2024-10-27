# LLM_motion
Codebase for generating expressive robot motion with a large language model (LLM aka GPT-4)

### Link to Research Paper
TBA


## Main Files and User Study
This codebase uses the framework as described in our submitted paper. In this implimentation, the GPT-4 model is used. The main files in this repo are:

### Jupyter notebook used to generate the prompt and query the LLM 
(Start of this notebook includes an explanation of the OpenAI API hyper-parameters used in this work)
https://github.com/liamreneroy/LLM_motion/blob/main/scripts/llm_to_motion.ipynb

### Prompt structure used to query the LLM:
https://github.com/liamreneroy/LLM_motion/blob/main/media/sample_prompt.txt

### Sample output from the LLM based on the prompt:
https://github.com/liamreneroy/LLM_motion/blob/main/media/sample_output.txt

### User data collection survey 01 description:
https://github.com/liamreneroy/LLM_motion/blob/main/media/survey_01_data_collection/survey01_user_data_collection_descript.txt

### Classification accuracy survey 02 description:
https://github.com/liamreneroy/LLM_motion/blob/main/media/survey_02_classifcation_accuracy/survey02_classification_accuracy_descript.txt

### Task and robot description presented to users both surveys:
https://github.com/liamreneroy/LLM_motion/blob/main/media/survey_01_data_collection/task_description.txt

### The statistical analyses for our two hypotheses (H1, H2) are here:
https://github.com/liamreneroy/LLM_motion/blob/main/stats/

### All the raw data collected for the user study is here:
https://github.com/liamreneroy/LLM_motion/blob/main/data/

### Youtube Playlist Links:
Motion Parameters:  https://tinyurl.com/eight-motion-parameters

Final Poses:        https://tinyurl.com/final-poses


## Secondary LLM-Generated Audio Experiment
To evaluate the generalizability of our framework, we conducted a second experiment to test its ability to generate nonverbal audio expressions.
https://github.com/liamreneroy/LLM_motion/tree/main/llm_audio_testcase

### LLM-generated audio files for three target robot states (plus original audio):
https://github.com/liamreneroy/LLM_motion/tree/main/llm_audio_testcase/selected%20sounds

### Plots LLM-generated audio and expressions generated in our prior work:
https://github.com/liamreneroy/LLM_motion/tree/main/llm_audio_testcase/plots

### All the parameterized audio files from our prior work (RL_Audio repo):
https://github.com/liamreneroy/RL_audio/tree/main/notebooks/audio/sonif_libA/looped


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