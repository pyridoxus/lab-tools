"module importing a scope for global access"
_rcsid="hp_scope_module.py,v 1.3 2003/05/30 13:29:22 mendenhall Release-20050805"

from vxi_11_scopes import hp54542

class my_hp54542(hp54542):
	pass
	
		
if 0:
	scope=my_hp54542(host="172.24.24.30", portmap_proxy_host="127.0.0.1", portmap_proxy_port=1111,
			 device="gpib0,7",  timeout=4000, device_name="hp54542",
			raise_on_err=1)
else:
	scope=my_hp54542(host="172.24.24.30", 
			 device="gpib0,16",  timeout=5000, device_name="hp54542",
			raise_on_err=1)

