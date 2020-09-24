from fp.fp import FreeProxy
from datetime import datetime
import pickle
def get_proxies(number=10):
  #return List[dict()]
  proxies = list()
  prox_ts = dict()
  while(len(proxies)<number):
    prox_ts=dict()
    proxie = FreeProxy(rand=True, timeout=0.5).get()
    if proxie in [[a for a in i.keys()][0] for i in proxies] or proxie == None:
      continue
    else:
      ts = datetime.timestamp(datetime.now())
      prox_ts[proxie] = ts
      proxies.append(prox_ts)
 
  return proxies

n_proxies = int(input('Enter number of proxies: '))

proxies_list = get_proxies(n_proxies)
proxies_file = open('proxies.txt','wb')
pickle.dump(proxies_list, proxies_file)
proxies_file.close()
print('Done')