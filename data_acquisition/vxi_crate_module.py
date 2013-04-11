"Import all the devices in our crate at once"
_rcsid="vxi_crate_module.py,v 1.3 2003/05/30 13:29:23 mendenhall Release-20050805"

import vxi_crate_devices as v


scan_adc=v.e1413b(2)	
dac1=v.e1328a(3)
dac2=v.e1328a(4)
video=v.video_mux(5)
dio=v.e1458a(6)
thermo=v.thermometers(7)	
glue_board=v.glue(11)
pattern=v.dg600(12)

del v
