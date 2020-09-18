# Veracode Delete Sandbox

A simple example script to delete a Sandbox if it exists in a Veracode 
application profile and you have the appropriate permissions.

## Setup

Clone this repository:

    git clone https://github.com/christyson/veracode_delete_sandbox

Install dependencies:

    cd veracode_delete_sandbox
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## usage

usage: veracode_delete_sandbox.py [-h] -a APP -s SANDBOX

Note: if it sucessfully deletes the sandbox it will exit with a 0 otherwise a 1

## Run

If you have saved credentials as above you can run:

    python veracode_delete_sandbox.py -a <your app name> -s <your sandbox name>
    
Otherwise you will need to set environment variables before running `example.py`:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python veracode_delete_sandbox.py -a <your app name> -s <your sandbox name>
