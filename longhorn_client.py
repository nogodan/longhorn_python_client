#!/usr/bin/env python3

""" 
    1 Aug 2022 Taeho Choi created for longhorn API python client
    KUBECONFIG needs to be imported properly before running this script 
"""

import time
import longhorn
import os
import json

#Warning msg to user
print("#"*40)
print("!! WARNING: This script can cause catastrophic consequences to your infrastructure !! ")
print("!! Please make sure you understand what you are trying to achieve clearly !! ")
print("#"*40)

print("Please make sure you have imported k8s config file correctly")
time.sleep(1)

print("Running kube proxy to redirect svc port to local")
os.system("kubectl port-forward services/longhorn-frontend 8080:http -n longhorn-system & ")
time.sleep(3)

#not using proxy since it will be internal network 
os.system("export http_proxy= ; export https_proxy= ")

# If automation/scripting tool is inside the same cluster in which Longhorn is installed
longhorn_url = 'http://longhorn-frontend.longhorn-system/v1'
# If forwarding `longhorn-frontend` service to localhost
longhorn_url = 'http://localhost:8080/v1'

#Check to see if port is listening 
os.system("curl http://localhost:8080/v1")

#Create longhorn client object with given URL
client = longhorn.Client(url=longhorn_url)

def print_menu():
    print("\n")
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
    print("\n")

#Volume Ops
def option1():
     print('Handle option \'Option 1\'')
     volumes = client.list_volume()
     vol_json = json.loads(json.dumps(volumes,default=vars))
     print("#"*200)
     print("These are the longhorn volumes")
     print("#"*200+"\n")
     for _ijson in vol_json["data"]:
        print("ID:{} STATE:{} CONTROLLER:{:<15} SIZE:{:<4}GB NS:{:<15} POD_NAME:{:<15}".format(_ijson["id"], _ijson["state"], _ijson["replicas"][0]["hostId"],int( _ijson["size"])/1024/1024/1024,_ijson["kubernetesStatus"]['namespace'], _ijson["kubernetesStatus"]['workloadsStatus'][0]['podName']))

def option2():
     print('Handle option \'Option 2\'')
     vol_id = input("what is the volume name or id to check: ")
     output = client.by_id_volume(id=vol_id)
     print(json.dumps(output, indent=4, default=vars))

def option3():
     print('Handle option \'Option 3\'')
     vol_id = input("what is the volume name or id to attach: ")
     node_id = input("what is the node id to attach: ")
     testvol1 = client.by_id_volume(id=vol_id)
     output = testvol1.attach(hostId=node_id)
     print(json.dumps(output, indent=4, default=vars))

def option4():
     print('Handle option \'Option 4\'')
     vol_id = input("what is the volume name or id to detach: ")
     testvol1 = client.by_id_volume(id=vol_id)
     print(type(testvol1))
     print(testvol1)
     output = testvol1.detach()
     print(json.dumps(output, indent=4, default=vars))

def option5():
     print('Handle option \'Option 5\'')
     vol_id = input("what is the volume name or id for snapshot: ")
     snapshot = input("what is the snapshot name to create: ")
     vol_client = client.by_id_volume(id=vol_id)
     output = vol_client.snapshotCreate(name=snapshot)
     print(json.dumps(output, indent=4, default=vars))

def option6():
     print('Handle option \'Option 6\'')
     vol_id = input("what is the volume name or id for backup: ")
     snapshot_name = input("what is the snampshot name to backup: ")
     vol_client = client.by_id_volume(id=vol_id)
     output = vol_client.snapshotBackup(name=snapshot_name)
     print(json.dumps(output, indent=4, default=vars))

def option7():
     print('Handle option \'Option 7\'')
     vol_id = input("what is the volume name or id to update replica count: ")
     no_rep = int(input("what is the new no of replica count?: "))
     vol_client = client.by_id_volume(id=vol_id)
     output = vol_client.updateReplicaCount(replicaCount=no_rep)
     print(json.dumps(output, indent=4, default=vars))

#Node Ops
def option8():
     print('Handle option \'Option 8\'')
     volumes = client.list_node()
     vol_json = json.loads(json.dumps(volumes,default=vars))
     print("#"*40)
     print("These are the longhorn nodes")
     print("#"*40)
     for i in vol_json["data"]:
        print(i["id"])
     print("#"*40)

def option9():
     print('Handle option \'Option 9\'')
     node_id = input("what is the node id or name to check: ")
     output = client.by_id_node(id=node_id)
     print(json.dumps(output, indent=4, default=vars))

def option10():
     print('Handle option \'Option 10\'')
     node_id = input("what is the node id or name to disable: ")
     node1_obj = client.by_id_node(id=node_id)
     output = client.update(node1_obj, allowScheduling=False)
     print(json.dumps(output, indent=4, default=vars))

def option11():
     print('Handle option \'Option 11\'')
     node_id = input("what is the node id or name to enable: ")
     node1_obj = client.by_id_node(id=node_id)
     output = client.update(node1_obj, allowScheduling=True)
     print(json.dumps(output, indent=4, default=vars))

#Setting Ops
def option12():
     print('Handle option \'Option 12\'')
     settings = client.list_setting()
     settings_json = json.loads(json.dumps(settings,default=vars))
     print("#"*40)
     print("These are the longhorn cluster settings")
     print("#"*40)
     print(json.dumps(settings,indent=4,default=vars))

def option13():
     print('Handle option \'Option 13\'')
     setting_id = input("what is setting id or name to check: ")
     output = client.by_id_setting(id=setting_id)
     print(json.dumps(output, indent=4, default=vars))

def option14():
     print('Handle option \'Option 14\'')
     setting_id = input("what is the setting id or name to update: ")
     new_val = input("what is the new value for the setting: ")
     setting_obj = client.by_id_setting(id=setting_id)
     output = client.update(setting_obj, value=new_val)
     print(json.dumps(output, indent=4, default=vars))

def option15():
     print('Handle option \'Option 15\'')
     print('Thanks message before exiting')
     exit()

#Set dict for menu option and func mapping
menu_options = {
    #Volume operation
    1: 'List all volumes',
    2: 'Get volume by NAME/ID',
    3: 'Attach volume to node',
    4: 'Detach TESTVOL1',
    5: 'Create a snapshot of TESTVOL1 with NAME',
    6: 'Create a backup from a snapshot NAME',
    7: 'Update the number of replicas of TESTVOL1',
    #node operation
    8: 'List all nodes',
    9: 'Get node by NAME/ID',
    10: 'Disable scheduling for NODE1',
    11: 'Enable scheduling for NODE1',
    #Setting operation
    12: 'List all settings',
    13: 'Get setting by NAME/ID',
    14: 'Update a setting',
    15: 'Exit',
}

options = {
                1: option1, 
                2: option2, 
                3: option3,
                4: option4, 
                5: option5, 
                6: option6,
                7: option7, 
                8: option8, 
                9: option9,
                10: option10, 
                11: option11, 
                12: option12,
                13: option13, 
                14: option14, 
                15: option15,
        }

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option in options:
            options[option]()
        else:
            print('Invalid option. Please enter a number between 1 and 15.')

