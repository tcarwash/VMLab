terraform {
  required_providers {
    proxmox = {
      source = "telmate/proxmox"
      version = "2.9.8"
  }
}
}
provider "proxmox" {
      pm_api_url="https://carr-dc1.home:8006/api2/json"
}

variable "vm_num" {
  type = number
  default = 4
}

resource "proxmox_vm_qemu" "worker" {
  for_each = zipmap(range(var.vm_num),range(var.vm_num))
  name  = "t-lab-worker${each.value + 1}"
  desc  = "testing terraform"
  clone = "Ubuntu-Cloudinit"
  full_clone = false
  target_node = "carr-dc1"
  os_type = "cloud-init"
  cores = 1
  ipconfig0 = "ip=10.0.1.2${format("%02d", each.value + 1)}/24,gw=10.0.1.1"
  agent = 1
  sockets = 1
  memory = 2048
  network {
    model = "virtio"
    bridge = "vmbr1"
  }
  connection {
    type = "ssh"
    user = "root"
    host = "${self.default_ipv4_address}"
    bastion_host = "192.168.1.203"
    private_key = "${file("/app/tf/ssh/id_rsa")}"
  }
  provisioner "remote-exec" {inline = ["ls",]}
  provisioner "local-exec" {
    command ="ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u root --key-file="//app//tf//ssh//id_rsa" --extra-vars='port_len=${var.vm_num} hostname=${self.name} vm_id=${each.value + 1} pmx_id=${element(split("//", self.id), length(split("//", self.id))-1)} ip=${self.default_ipv4_address} ssh_port=22${format("%02d", each.value + 1)} ttyd_port=30${format("%02d", each.value + 1)}' --ssh-extra-args='-J tyler@carr-lab2.home' -i '${self.default_ipv4_address},' playbook-init.yml"
  }
  provisioner "local-exec" {
    command ="ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u root --key-file="//app//tf//ssh//id_rsa" --extra-vars='ttyd_port_range=3001-${3000 + var.vm_num} ssh_port_range=2201-${2200 + var.vm_num} hostname=${self.name} ip=${self.default_ipv4_address} vm_id=${each.value + 1} ttyd_port=30${format("%02d", each.value + 1)} ssh_port=22${format("%02d", each.value + 1)}' -i '192.168.1.203,' --ssh-extra-args='-p 2200' playbook-post.yml"
  }
  provisioner "local-exec" {
    command ="ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u root --key-file="//app//tf//ssh//id_rsa" --extra-vars='ttyd_port_range=3001-${3000 + var.vm_num} ssh_port_range=2201-${2200 + var.vm_num} hostname=${self.name} ip=${self.default_ipv4_address} vm_id=${each.value + 1} ttyd_port=30${format("%02d", each.value + 1)} ssh_port=22${format("%02d", each.value + 1)}' -i '192.168.1.1,' playbook-haproxy.yml"
  }
#  provisioner "remote-exec" {inline = ["shutdown -r now",]}
}
