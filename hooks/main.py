from flask import Flask, request
import os

app = Flask(__name__)


base_path = "/home/gagalug/"
projects = ["FlappyArm"]



def git_pull_in_dir(base_path, service):
    """ """
    previous_cwd = os.getcwd()
    try:
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
    except:
        out = "Could not change directory."
        code = -1
    return out, code

def service_restart():
    os.system('sudo /home/gagalug/flappyarm_restart.sh')
    return 1


@app.route("/", methods=['POST'])
def hook():
    data = git_pull_in_dir(base_path, projects[0])
    restart = service_restart()
    return ("Completed")

if __name__ == "__main__":
    app.run('0.0.0.0')
