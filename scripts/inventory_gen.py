#!/usr/bin/env python3

import json
import sys
import yaml

def generate_dict(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_yaml_to_file_from_dict(filename, data_dict):
    with open(filename, 'w') as f:
        yaml.dump(
            data_dict,
            f,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            allow_unicode=True
        )

def generate_inventory_dict(host_ip_dict, host_key_dict):
    inventory = {
        'linux': {
            'children': {
                'nginx_proxy': {
                    'hosts': {}
                },
                'nginx_server': {
                    'hosts': {}
                }
            },
            'vars': {}
        }
    }
    
    cnt = 0
    
    for host, ip in host_ip_dict.items():
        child_key = 'nginx_proxy' if cnt < 1 else 'nginx_server'
        cnt += 1
        inventory['linux']['children'][child_key]['hosts'][host] = {
            'ansible_host': ip,
            'ansible_user': 'ubuntu',
            'ansible_ssh_private_key_file': host_key_dict[host]
        }
        
    inventory['linux']['vars'] = {
        'connection_protocol': 'ssh',
        'ansible_become': 'true',
        'ansible_become_method': 'sudo',
        'ansible_become_user': 'root'
    }
    
    return inventory

if __name__ == '__main__':

    host_ip_file_path = sys.argv[1]
    host_key_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    
    write_yaml_to_file_from_dict(output_file_path, generate_inventory_dict(generate_dict(host_ip_file_path), generate_dict(host_key_file_path)))
