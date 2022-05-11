import subprocess


def create(path, num):
    proc = subprocess.Popen(['terraform -target', '/app/tf/' + path, '--var="vm_num={}"'.format(num)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    return_code = proc.poll()

    return return_code


