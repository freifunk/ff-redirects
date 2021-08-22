# Freifunk Redirects Creation

This collection of scripts and configuration creates everything needed for redirects: letsencrypt certificates, vhosts and redirects.

## How to run

1. Configure the redirects you want in `vars/main.yaml`. See the example file.
2. run `create_vars.py > vars/vhosts.yaml` to create the vhosts configuration
3. run `ansible-playbook -i inventory configure_redirects.yaml` to create everything. This can take a while.
