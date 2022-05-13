import subprocess


def create(path, num):
    proc = subprocess.Popen(['/usr/bin/terraform', '--target', '/app/tf/' + path, '--var="vm_num={}"'.format(num)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    return_code = proc.poll()

    return return_code


def destroy(path):
    proc = subprocess.Popen(['/usr/bin/terraform', '--target', '/app/tf/' + path, 'destroy'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    return_code = proc.poll()

    return return_code
