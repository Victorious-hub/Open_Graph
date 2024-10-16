import json

def prettify_json(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Prettify the data.json file
prettify_json('data.json', 'data.json')