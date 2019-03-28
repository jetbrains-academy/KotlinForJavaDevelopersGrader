import os
import sys
import json
import base64

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as submission:
        a = json.loads(submission.read())  # type: dict
        for (name, content) in a.items():
            path = 'solution/' + name
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path,  'wb') as file:
                file.write(base64.b64decode(content))