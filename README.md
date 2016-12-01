Google API - Python App
=======================
by *David Cunningham*
This is a prototype Python API for the Google Python API.  This makes using the Google Python API easier by giving the user classes that define the kinds of relationships the user can have with the different API services - Drive, Docs, Gmail, etc.

I built this in a (late) night a few months ago after deciding I wanted to figure out how to use the Google API, and it still has a few quirks with multiple API accesses that need to be worked out (feel free to send suggestions!), but I thought I would release what I've made so far and hopefully get around to fixing more later.  Obviously the user needs to have an API account with Google (https://console.developers.google.com/apis/library), and also needs to edit the file paths at the top of g_api_utils.py (CREDENTIALS_FILE_NAME, client_secrets_dir, CLIENT_SECRET_FILE) to match their respective authentication/secret file locations and names.  Also, note that CREDENTIALS_FILE_NAME should be stored in [home]/.credentials/.  These configuration details will be made more user friendly when I get around to it.

Feel free to contribute!  Enjoy!