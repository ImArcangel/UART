xst -ifn Loopback.xst
ngdbuild  -uc Loopback.ucf Loopback.ngc Loopback.ngd
map -ol high -w -pr b -timing -o Loopback_map.ncd Loopback.ngd Loopback.pcf
par -ol high -w Loopback_map.ncd Loopback.ncd Loopback.pcf
bitgen -w Loopback.ncd Loopback.bit
