# Sample Streamlit App
This repo is meant to demonstrate how you could create and run a sample streamlit application.

## Instructions for Running
In the `api` folder there is a file called `api.py` which contains REST endpoints for the model that was built for inference.  You'll need to first start this by running the command `flask --app api/api run`.  This command will work **if you are in the root directory of this repo.** The `api/api` section is meant to be a relative file path from that location.  If you are somewhere else in your command line then you will need to adjust the file path appropriately.  

If you are running an older version of flask, then the following command would be more appropriate:

`export FLASK_APP=api/api`
`flask run`

You'll need this to run before you first can start the streamlit application.  

Once you have this file running on a local server, you can then start the streamlit application by running the following command:

`streamlit run app.py`

Once you are finished you might be prompted to enter your email address at your command line which you can skip, and the app should automatically pop up in your browser window.
