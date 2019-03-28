import os
import sys
import base64
import json


def get_encoded_file_text(file):
    return base64.b64encode(open(file, 'rb').read()).decode("utf-8")


if __name__ == '__main__':
    submission_folder = sys.argv[1]
    encoded_submission = dict()
    for (base_dir, _, file_names) in os.walk(submission_folder):
        for file_name in file_names:
            if file_name not in ["task.md", ".DS_Store"]:
                rel_path = os.path.relpath(os.path.join(base_dir, file_name), submission_folder).replace(os.sep, "/")
                encoded_submission['src/' + os.path.basename(submission_folder) + '/' + rel_path] = get_encoded_file_text(
                    os.path.join(base_dir, file_name))

    open(sys.argv[2], 'w').write(json.dumps(encoded_submission))
