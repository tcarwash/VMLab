#!/bin/sh

terraform apply
terraform-inventory -inventory ./ > inventory
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u tyler --ssh-extra-args='-J tyler@carr-lab2.home' --ask-become-pass -i inventory  playbook-post.yml
