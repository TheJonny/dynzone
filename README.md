## Setup:
- install nsd
- clone into /etc/nsd
- create the zonefile in `zones/<zone.name.as.filena.me>`. The serial number can be anything less than the current timestamp, for example 1000000000. the script will break 2**31 seconds after this value. in the zonefile, `$INCLUDE current-ips

```
$ORIGIN rot1.bruckbu.de.
$TTL 300

@ IN SOA karpos-internal.rot1.bruckbu.de. root (
		1000000000 ;serial is set to timestamp by dnssec-signzone
		300 ; refresh
		300 ; retry
		300 ; expire
		300; negative ttl
		)
	IN  NS		platon.bruckbu.de.
	IN  NS      ns1.he.net.

@    IN      MX     10 mail.bruckbu.de.
; *    IN      MX     10 mail.bruckbu.de.

karpos-internal AAAA fd17::62
karpos-internal A 192.168.17.62

matrix IN CNAME selene
cloud IN CNAME selene

$INCLUDE current-ips
```

- include the zone in `nsd.conf.d/`

- create a file named suffixes with that looks like
```
selene ::63
karpos ::62
prometheus ::61
io ::60
```

run `make -C /etc/nsd sign && sysemctl restart nsd` every n minutes, or triggered by something like `ip monitor`
