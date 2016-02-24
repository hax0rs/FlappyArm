from flask import Flask, request
import os

app = Flask(__name__)


base_path = "/home/gagalug/"
projects = ["FlappyArm"]


@app.route("/", methods=['POST'])
def hook():
    # return ("Hooked me right in the gabber")
    git_pull_in_dir(base_path, service)

if __name__ == "__main__":
    app.run('0.0.0.0')



def git_pull_in_dir(base_path, service):
    """
    A service name should match with both its name in supervisor and its /srv/*
    path.
    """
    previous_cwd = os.getcwd()
    os.chdir(base_path + service)
    try:
        out = sp.check_output(["git", "pull"], timeout=120).decode('utf-8')
        code = 0
    except sp.CalledProcessError as e:
        out = e.output.decode('utf-8')
        out += "\nErrored out with code " + str(e.returncode) + "."
        code = e.returncode
    out += "\n"
    os.chdir(previous_cwd)
    return out, code
