# Colima Helper

![CI](https://github.com/micoli/colima-helper/actions/workflows/ci.yml/badge.svg)

`colima-helper` purpose is to add some little features to [colima](https://github.com/abiosoft/colima)
- fs-event: filesystem events forwarder from the host to colima instance (inspired from [dinghy fsevents_to_vm](https://github.com/codekitchen/fsevents_to_vm))


## Installation
```
pip install git+https://github.com/micoli/colima-helper.git
```
or for upgrade
```
pip install --upgrade --force-reinstall git+https://github.com/micoli/colima-helper.git
```

depending of your installation `pip` can be replaced by `pip3`

## Commands

### Help
[//]: <> (command-placeholder-start "colima-helper --help")
```
usage: colima-helper [-h] [--debug] [--verbose]
                     {fs-events,kill-fs-events,gui} ...

Colima host helper

positional arguments:
  {fs-events,kill-fs-events,gui}
                        commands
    fs-events           wath for filesystem changes and 'touch' on colima host
    kill-fs-events      kill fs-event daemon
    gui                 docker_container GUI

optional arguments:
  -h, --help            show this help message and exit
  --debug               Print lots of debugging statements
  --verbose             Be verbose
```
[//]: <> (command-placeholder-end)

### Command `fs-event`
[//]: <> (command-placeholder-start "colima-helper fs-events --help")
```
usage: colima-helper fs-events [-h] [--path PATH] [--host HOST]
                               [--patterns PATTERNS [PATTERNS ...]]
                               [--ignore-patterns IGNORE_PATTERNS [IGNORE_PATTERNS ...]]
                               [--daemon | --no-daemon] [--address ADDRESS]
                               [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           path to watch
  --host HOST           colima host
  --patterns PATTERNS [PATTERNS ...]
                        pattern
  --ignore-patterns IGNORE_PATTERNS [IGNORE_PATTERNS ...]
                        ignore pattern
  --daemon, --no-daemon
                        daemonize (default: False)
  --address ADDRESS     http log address
  --port PORT           http log port
```
[//]: <> (command-placeholder-end)

### Command `kill-fs-events`
[//]: <> (command-placeholder-start "colima-helper kill-fs-events --help")
```
usage: colima-helper kill-fs-events [-h]

optional arguments:
  -h, --help  show this help message and exit
```
[//]: <> (command-placeholder-end)

### Command `gui`
[//]: <> (command-placeholder-start "colima-helper gui --help")
```
usage: colima-helper gui [-h] [--docker-host DOCKER_HOST]
                         [--fsevents-address FSEVENTS_ADDRESS]
                         [--fsevents-port FSEVENTS_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --docker-host DOCKER_HOST
                        docker-host
  --fsevents-address FSEVENTS_ADDRESS
                        fsevents log address
  --fsevents-port FSEVENTS_PORT
                        fsevents log port
```
[//]: <> (command-placeholder-end)

### fs-events

#### Interactive
```
colima-helper fs-events --path=~/src/project/ --host=colima
```

#### Daemonized
```
colima-helper --verbose fs-events --path=~/src/project/ --daemon
colima-helper kill-fs-events --path=~/src/project/
```

#### Files location

log: `/tmp/colima-helper-fs-events.log`
pid: `/tmp/colima-helper-fs-events.pid`

# Todo
- migrate daemon mode to https://pypi.org/project/launchctl/ for fs-event

Merge requests are welcomed



# TODO
- plugin events messenger
- pm2 subprocesses
- local minimalist htop
