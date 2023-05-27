from flask import Flask, render_template
import socket
import argparse
import logging
import os
import yaml

app = Flask(__name__)

@app.route('/')
def display_info():
    # To test entry point. If custom_app.py is run, title will be "Custom App"
    app_title = "Custom App"

    # Setting default values for parameter if there is no config file.
    app_name = 'Custom Default'
    environment = 'Custom Default'
    custom_tag = 'Custom Default'

    # Getting IP address and hostname of container
    ip_address = str(socket.gethostbyname(socket.gethostname()))
    hostname = socket.gethostname()

    # Check if the app_config.yaml file exists
    config_file = os.path.join(app.root_path, 'config', 'app_config.yaml')
    if os.path.exists(config_file):
        # Read the app-name and environment from the YAML file
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
            # Getting parameters from yaml file
            app_name = config_data.get('app-name', app_name)
            environment = config_data.get('environment', environment)
            custom_tag = config_data.get('custom-tag', custom_tag)
    
    # List the files in the data directory
    data_dir = os.path.join(app.root_path, 'data')
    file_list = os.listdir(data_dir)

    return render_template('index.html', app_title=app_title ,
                           ip_address=ip_address, hostname=hostname, 
                           custom_tag=custom_tag, app_name=app_name, 
                           environment=environment, file_list=file_list)


if __name__ == '__main__':
    # port number will be passed as argument > app.py <port-numer>.
    parser = argparse.ArgumentParser()
    # arg name is port, type is integer, description is "port number".
    parser.add_argument('port', type=int, help='Port number')
    # --debug is optional arg. If passed, "True" will be passed as value.
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    # log debug message to a log file
    log_dir = os.path.join(os.path.dirname(__file__), 'log')
    # if "Log" dir doesn't exist, create one.
    os.makedirs(log_dir, exist_ok=True)
    # log file name
    log_file = os.path.join(log_dir, 'debug.log')

    # log format. Log will be written to "Log_file", all DEBUG level logs will be record, timestamp with following format will be included.
    logging.basicConfig(filename=log_file, level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

    app.run(host='0.0.0.0', port=args.port, debug=args.debug)
