# Vanish

Vanish is an installable python application that interacts with the IPVanish servers. It can
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
[See the todo page](TODO.md)
