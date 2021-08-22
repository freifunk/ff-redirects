# Freifunk Redirects Creation

This collection of scripts and configuration creates everything needed for redirects: letsencrypt certificates, vhosts and redirects.

## How to run

1. On the very first time run `ansible-galaxy install geerlingguy.certbot gcoop-libre.apache`
2. Configure the redirects you want in `vars/main.yaml`. See the example file.
3. run `./create_vars.py > vars/vhosts.yaml` to create the vhosts configuration
4. run `ansible-playbook -i inventory configure_redirects.yaml` to create everything. This can take a while.
