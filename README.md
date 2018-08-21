# Vanish

## Overview
Vanish an installable python application that interacts with the IPVanish servers. It can
grab the latest server configurations and intelligently detect what servers to connec to
based on user defined filtering.

```
# Ping all the London servers
$ vanish ping --city London

# Ping US get servers
$ vanish ping --country US

# Ping servers in a specific region
$ vanish ping --country US --region "New York"

# Connect to a server
$ vanish connect --server uk-lon-a12
```

# To do
1. Add consistent logging interface with colour and font style controls.
1. Cache the geojson in the format we read rather than processing each time.
1. Move GeoJson and OvpnConfig control into their own model classes that use the Cache object.
1. Intelligently detect a server to connect to based on filtering.
1. Disallow 'connect' command with no filters applied.
1. Controlling the openvpn output including taking username and password on command line.
1. Improve "non-scenario" support so commands cannot be invoked without the minimum number of arguments.
1. Improve region possibilities (there are some "fake" regions that need removing)
1. Make filters case insensitive.
