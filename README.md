**All files in this project, including "[dondns.sh](/dondnsample/dondns.sh)" and "[dondns.conf](dondnsample/dondns.sh)", fall under the GNU Lesser General Public License ("[LGPL](LICENSE)"**

---

Description here...

---

### Config sample

```
arch: amd64
cores: 1
features: nesting=1
hostname: Router
memory: 512
net0: name=eth0,bridge=vmbr0,firewall=1,gw=192.168.1.1,hwaddr=4E:0E:D2:77:98:8D,ip=192.168.1.2/24,type=veth
net1: name=eth170,bridge=vmbr170,firewall=1,hwaddr=5E:97:BD:87:7C:B5,ip=172.16.0.1/24,type=veth
ostype: debian
rootfs: local-lvm:vm-200-disk-0,size=8G
swap: 512
unprivileged: 1
```