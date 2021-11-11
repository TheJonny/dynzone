zonefiles = $(wildcard zones/*)
zones = $(patsubst zones/%,%,$(zonefiles))
signedzonefiles = $(patsubst zones/%,signed/%,$(zonefiles))
conffiles = $(wildcard nsd.conf.d/*)
etcfiles = $(patsubst %,/etc/nsd/%,$(conffiles) $(signedzonefiles))


.PHONY: nsd info sign

info:
	@echo zonefiles: $(zonefiles)
	@echo zones: $(zones)
	@echo signedzonefiles: $(signedzonefiles)
	@echo etcfiles: $(etcfiles)
	@echo
	@echo use make sign to sign all zones
	@echo use make nsd to update nsd config
	@echo
	@for z in $(zones); do grep -h 257 keys/K$$z.*; cat dsset-$$z.; done


/etc/nsd/%: %
	sudo install -D -o root -g nsd -m 640 $< $@

nsd: $(etcfiles)
	sudo systemctl restart nsd.service
	sudo systemctl reload nsd.service

sign: $(signedzonefiles)

signed/% dsset-%.: zones/%
	dnssec-signzone -q -S -K keys  -f $@  -N unixtime -e +15552000 -o $*. $<

.PHONY: getips
getips:
	./getips.py
current-ips: getips
signed/rot1.bruckbu.de: current-ips
