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

## Example of executions:

### help
```
$ colima-helper --help
usage: colima-helper [-h] [--daemon | --no-daemon] [--debug] [--verbose] {fs-events,kill-fs-events} ...

Colima host helper

positional arguments:
  {fs-events,kill-fs-events}
                        commands
    fs-events           wath for filesystem changes and "touch" on colima host
    kill-fs-events      kill fs-event daemon

optional arguments:
  -h, --help            show this help message and exit
  --daemon, --no-daemon
                        daemonize (default: False)
  --debug               Print lots of debugging statements
  --verbose             Be verbose
```

### fs-events

fsevent needs `coreutils` (`sudo apk add coreutils`) to use microsecond touch command

#### Interactive
```
colima-helper fs-events --path=~/src/project/ --host=colima
```

#### Daemonized
```
colima-helper --daemon --verbose fs-events --path=~/src/project/
colima-helper kill-fs-events --path=~/src/project/
```

#### Files location

log: `/tmp/colima-helper-fs-events.log`
pid: `/tmp/colima-helper-fs-events.pid`

# Todo
- migrate daemon mode to https://pypi.org/project/launchctl/ for fs-event

Merge requests are welcomed


# TODO
- sort event
- fs event watcher
- docker-compose support
- plugin events messenger
- stderr/stdout
- docker.APIClient/context/from_env DI
- local htop
