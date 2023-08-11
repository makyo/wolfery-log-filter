import re
import sys

from bs4 import BeautifulSoup
import yaml


def process(config, log):
    filters = [re.compile(filter) for filter in config['text']]
    soup = BeautifulSoup(log, 'html.parser')
    for tag in soup.find_all(class_='ev'):
        try:
            character = tag.find(class_='charlog--char')
            contents = tag.find(class_='common--formattext')

            if character in config['characters']:
                continue

            for filter in filters:
                if filter.match(contents):
                    continue

            tag['class'].append('hide')
        except:
            pass

    return soup


if __name__ == '__main__':
    config_file = sys.argv[1]
    log_file = sys.argv[2]
    
    with open(config_file) as f:
        config = yaml.safe_load(f)

    with open(log_file) as f:
        log = f.read()

    result = process(config, log)

    import pdb; pdb.set_trace()
