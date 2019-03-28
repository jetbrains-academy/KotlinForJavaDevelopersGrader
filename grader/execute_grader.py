import base64
import json
import os
import subprocess
import sys

GSON = "gson-2.8.5.jar"

BUILD = "build"

HAMCREST_CORE = "hamcrest-core-1.3.jar"

JUNIT = "junit-4.12.jar"


def prepare_solution():
    with open("/shared/submission/submission", 'r') as submission:
        a = json.loads(submission.read())  # type: dict
        for (name, content) in a.items():
            path = 'solution/' + name
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as file:
                file.write(base64.b64decode(content))


def compile_kotlin(target_name, path_to_compile, destination, classpath=None):
    command = ["kotlinc", path_to_compile]
    if classpath:
        command.append("-cp")
        command.append(build_classpath(classpath))
    command.append("-include-runtime")
    command.append("-d")
    command.append(destination)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = result.stderr.decode("utf-8")
    if result.returncode != 0 and error:
        print_result(0.0, "Compile error in {0}:\n{1}".format(target_name, error))
        exit(0)


def build_classpath(classpath):
    classpath_with_current_dir = ["."]
    classpath_with_current_dir.extend(classpath)
    return ':'.join(classpath_with_current_dir)


def print_result(score, message):
    print(json.dumps({"fractionalScore": score, "feedback": message}))


if __name__ == '__main__':
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"

    os.chdir("grader")

    lessons = {
        "GWATl": ("strings", 1),
    }

    part_id = sys.argv[2]
    if part_id not in lessons.keys():
        print("No partId matched " + part_id)
    lesson_name = lessons[part_id][0]
    week_number = lessons[part_id][1]

    os.mkdir(BUILD)
    os.mkdir("solution")

    prepare_solution()

    solution = "build/solution.jar"

    compile_kotlin("solution", "solution/src", solution)

    initial_tests = "build/initial.jar"
    compile_kotlin("initial tests", "src/test/initial/_{0}week/{1}".format(week_number, lesson_name),
                   initial_tests, [JUNIT, HAMCREST_CORE, solution])

    compile_kotlin("hidden tests", "src/test/hidden/" + lesson_name, BUILD,
                   [JUNIT, HAMCREST_CORE, solution, initial_tests])

    compile_kotlin("test runner", "TestRunner.kt", BUILD, [JUNIT, GSON])

    tests_execution = subprocess.run(
        ["java", "-cp", build_classpath([JUNIT, HAMCREST_CORE, GSON, BUILD, solution, initial_tests]),
         "TestRunner", "hidden/" + lesson_name],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = tests_execution.stderr.decode("utf-8")

    if tests_execution.returncode != 0 and error:
        error_text = "Runtime error executing tests:\n" + error
        print_result(0.0, error_text)
        exit(0)

    print(tests_execution.stdout.decode("utf-8"))
