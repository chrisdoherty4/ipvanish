import os
"""
This module contains the application configuration values.
"""

config = {}

""" GENERAL """

"""
The root configuration directory for the application.
"""
config["config.dir"] = os.path.abspath(
    os.path.expanduser(
        os.path.join('~', '.config', 'vanish')
        )
    )

"""
Path to the cache file where arbitrary data is cached.
"""
config["cache.path"] = os.path.join(config['config.dir'], "cache")


""" GEOJSON """

"""
URL to the IPVanish geojson. The geojson contains server status information
and contributes to how we interface witht he ovpn configuration files.
"""
config["geojson.url"] = "https://www.ipvanish.com/api/servers.geojson"

"""
A path to the geojson cache location.
"""
config['geojson.cache.path'] = os.path.join(
    config['config.dir'], 'servers.geojson')

"""
A timeout value indicating how long the geojson is valid for.
"""
config['geojson.cache.timeout'] = 30


""" OVPN CONFIG """

"""
URL to IPVanish ovpn configuration files. This is a zip containing .ovpn files
and the necessary certificate file to connect to IPVanish servers.
"""
config["ovpnconfigs.url"] = "https://www.ipvanish.com/software/configs/configs.zip"

"""
The location the ovpn configuration files will be stored.
"""
config["ovpnconfigs.cache.path"] = os.path.join(
    config['config.dir'], 'openvpn')
