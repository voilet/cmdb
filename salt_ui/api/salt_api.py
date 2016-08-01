#coding=utf8
import salt.client
client = salt.client.LocalClient()

import salt.utils.event
#jobs_id = salt.client.APIClient()

event = salt.utils.event.MasterEvent('/var/run/salt/master')
#event = event.iter_events(wait=0.025,tag="salt", full=True)
def overview(request):
  target = request.GET.get("target",'*')
  try:
    grains = client.cmd(target, 'grains.items')
  except:
    grains = {}
  return grains

def execute(**kwargs):
  return client.cmd_async(**kwargs)

def get_state(target):
  try:
    states = client.cmd(target,'state.show_top')
  except:
    states = {}
  return states



if __name__ =="__main__":
  print get_state('60_12_201_27.nb_compute1.lightcloud.cn')

