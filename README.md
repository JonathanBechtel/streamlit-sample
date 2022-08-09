# Sample Streamlit App
This repo is meant to demonstrate how you could create and run a sample streamlit application and demonstrate its full capabilities.  Please refer to this repo 

## Instructions for Running

### Environment Setup
This application needs specific versions of certain libraries to run, so it's recommended that you build the application from a virtual environment.  

The following instructions can be followed using the anaconda package manager.  

 - Create a virtual environment named `streamlit` with the command `conda create --name streamlit`
 - Activate the virtual environment with the command `conda activate streamlit`
 - Install pip, so you can install other packages with the command `conda install pip`
 - Install the packages from the `requirements.txt` file with the command `pip install -r requirements.txt`
 
 This will take several minutes, but when everything is downloaded you will be ready to go.

### Starting the Application

In the `api` folder there is a file called `api.py` which contains REST endpoints for the model that was built for inference.  You'll need to first start this by running the command `flask --app api/api run`.  This command will work **if you are in the root directory of this repo.** The `api/api` section is meant to be a relative file path from that location.  If you are somewhere else in your command line then you will need to adjust the file path appropriately.  

If you are running an older version of flask, then the following command would be more appropriate:

`export FLASK_APP=api/api`
`flask run`

You'll need this to run before you first can start the streamlit application.  

Once you have this file running on a local server, you can then start the streamlit application by running the following command:

`streamlit run app.py`

Once you are finished you might be prompted to enter your email address at your command line which you can skip, and the app should automatically pop up in your browser window.
