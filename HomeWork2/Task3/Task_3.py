import os
import yaml

curr_dir = os.path.dirname(os.path.abspath(__file__))

file = os.path.join(curr_dir, 'example.yaml')

example = {
    'array': ['first', 'second', 'third'],
    'integer': 1,
    'dict': {
        'first_el': '€',
        'second_el': '€€',
        'third_el': '€€€',
    }
}

with open(file, 'w') as f:
    yaml.dump(example, f, default_flow_style=False, allow_unicode=True)

with open(file) as f:
    print(f.read())
