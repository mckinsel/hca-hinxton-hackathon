import docker
import stat

c = get_config()

c.JupyterHub.logo_file = "/srv/jupyterhub/logo.png"
c.JupyterHub.spawner_class = 'cassinyspawner.SwarmSpawner'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.cleanup_servers = False
c.JupyterHub.slow_spawn_timeout = 60 * 6
c.SwarmSpawner.start_timeout = 60 * 6
c.SwarmSpawner.http_timeout = 60 * 6

# The name of the service that's running the hub
c.SwarmSpawner.jupyterhub_service_name = "{{ hub_service_name }}"

# The name of the overlay network that everything's connected to
c.SwarmSpawner.networks = ["{{ network_name }}"]

# Mounts
cloudstor_shared_config = docker.types.DriverConfig(
    "cloudstor:aws",
    {"backing": "shared"})

cloudstor_local_config = docker.types.DriverConfig(
    "cloudstor:aws",
    {"size": "{{ local_disk_size }}", "ebstype": "gp2", "backing": "relocatable"})

shared_resource_mount = {
    "target": "{{ read_only_shared_mount_point}}",
    "source": "{{ read_only_shared_volume }}",
    "type": "volume",
    "read_only": True,
    "driver_config": cloudstor_shared_config}

shared_scratch_mount = {
    "target": "{{ writable_shared_mount_point }}",
    "source": "{{ writable_shared_volume }}",
    "type": "volume",
    "read_only": False,
    "driver_config": cloudstor_shared_config}

local_scratch_mount = {
    "target": "{{ local_mount_point }}",
    "source": "{{ '{{{{' }}.Service.Name{{ '}}}}' }}-{{ '{{{{' }}.Task.Slot{{ '}}}}' }}-local-volume",
    "type": "volume",
    "read_only": False,
    "driver_config": cloudstor_local_config}

docker_socket_mount = {
    "target": "/var/run/docker.sock",
    "source": "/var/run/docker.sock",
    "type": "bind"}

mounts = [shared_resource_mount, shared_scratch_mount, local_scratch_mount,
          docker_socket_mount]

c.SwarmSpawner.notebook_dir = "{{ notebook_dir }}"

c.SwarmSpawner.container_spec = {
    'args' : ['/usr/local/bin/start-singleuser.sh'],
    'Image' : "{{ singleuser_image }}",
    'mounts' : mounts
    }

c.SwarmSpawner.resource_spec = {
    'cpu_reservation': {{ server_cpu_reservation }},
    'cpu_limit': {{ server_cpu_limit }},
    'mem_limit': {{ server_mem_limit }}
    }

c.JupyterHub.authenticator_class = 'hashauthenticator.HashAuthenticator'
c.HashAuthenticator.secret_key = "{{ secret_password_key }}"
c.HashAuthenticator.password_length = {{ password_length }}

c.Authenticator.admin_users = admin = set()
c.Authenticator.whitelist = whitelist = set()
with open('/srv/jupyterhub_users/userlist') as f:
    for line in f:
        if line.isspace():
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
