## AI_CU

AI_CU is a program that helps students pay attention to video lectures by detecting face presence and closed eyes. The program pauses the video and gives an alarm if inattention is detected from more than 5 seconds. 

### Requirements before running the program

#### For Windows
- download the entire github folder and unzip the folder. Make sure that the folder is unzipped insides the Downloads folder and not anywhere else.
- run `install.bat` file in the folder. This will install all the dependencies necessary to run the program.
- make sure that both the file names are `AI_CU_main` and not anything else. Otherwise, an error relating to file paths may occur.
- open command prompt and go to the `AI_CU_main` folder using `cd`.
- run `ai_cu_env\Scripts\activate` to get inside the virtual environment.
- run either `py control_group.py` or `py experimental_group.py` depending on what group the user is assgined to.

### Description of Python Files
- `experiment_group.py`: program to run for experiment group
- `control_group.py`: program to run for control group
- `DisplayIntro.py`: intro screen that gives a brief description of the experiment/program
- `DisplayLink.py`: end screen that provides link to quiz and survey
- `WebCamVideo.py`: program that receives camera input concurrently using threading



