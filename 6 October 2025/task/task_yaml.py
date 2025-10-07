import yaml
import logging

# Configure logging
logging.basicConfig(filename='task_yaml.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

try:
    with open('settings.yaml', 'r') as f:
        config = yaml.safe_load(f)
    logging.info("Config loaded successfully")

    db = config['database']
    print(f"Connecting to {db['host']}:{db['port']} as {db['user']}")

except FileNotFoundError:
    logging.error("settings.yaml not found")
    print("Error: settings.yaml not found")

except yaml.YAMLError as e:
    logging.error(f"YAML parsing error: {e}")
