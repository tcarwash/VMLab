import subprocess


def create(path, num):
    cmd = ['/usr/bin/terraform', 'apply', "--var=vm_num={}".format(num)]
    proc = subprocess.Popen(cmd, universal_newlines=True, cwd='/app/tf/' + path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value = proc.communicate()[0]
    print('\tstdout: {}'.format(stdout_value))
    stderr_value = proc.communicate()[1]
    print('\tstderr: {}'.format(stderr_value))
    return_code = proc.wait()


    return return_code


def destroy(path):
     proc = subprocess.Popen(['/usr/bin/terraform', 'destroy'], cwd='/app/tf/' + path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    return_code = proc.poll()

    return return_code
