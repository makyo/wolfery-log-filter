import re
import sys
import traceback

from bs4 import BeautifulSoup
import yaml


def process(config, log):
    '''
    Process a log file, hiding lines that don't match a set of filters using `style` attributes.

    Arguments:

    - `config`: a dict with a `filters` key containing an array of regular expressions to keep.
    - `log`: the text of the Wolfery log file.
    '''

    total = 0
    hidden = 0
    remaining = 0
    
    filters = [re.compile(r'\b' + text + r'\b', re.IGNORECASE if text[0] == text[0].lower() else 0) for text in config['filters']]
    soup = BeautifulSoup(log, 'html.parser')

    for tag in soup.find_all(class_='ev'):
        total += 1
        try:
            found = False
            for filter in filters:
                if filter.search(repr(tag)):
                    found = True
                    break

            if not found:
                tag.attrs['style'] = 'display: none;'
                hidden += 1
            else:
                remaining += 1
        except:
            traceback.print_exc()

    print(f'{hidden} / {total} events hidden ({round(remaining/total * 100, 2)}% remaining)', file=sys.stderr)
    return soup


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'''USAGE:
        {sys.argv[0]} <config file> <log file>
        ''')
        sys.exit(1)

    config_file = sys.argv[1]
    log_file = sys.argv[2]

    # Load the YAML config file from the first argument.
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # Load the log file from the second argument.
    with open(log_file, encoding='utf-8') as f:
        log = f.read()

    result = process(config, log)

    print(repr(result))
