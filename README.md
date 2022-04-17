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
usage: colima-helper [-h] [--daemon | --no-daemon] [--debug] [--verbose]
                     {fs-events,kill-fs-events} ...

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
[//]: <> (command-placeholder-end)

### Command `fs-event`
[//]: <> (command-placeholder-start "colima-helper fs-events --help")
```
usage: colima-helper fs-events [-h] [--path PATH] [--host HOST]
                               [--patterns PATTERNS [PATTERNS ...]]
                               [--ignore-patterns IGNORE_PATTERNS [IGNORE_PATTERNS ...]]
                               [--replace-patterns REPLACE_PATTERNS [REPLACE_PATTERNS ...]]
                               [--cooldown-timeout COOLDOWN_TIMEOUT]
                               [--address ADDRESS] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           path to watch
  --host HOST           colima host
  --patterns PATTERNS [PATTERNS ...]
                        pattern
  --ignore-patterns IGNORE_PATTERNS [IGNORE_PATTERNS ...]
                        ignore pattern
  --replace-patterns REPLACE_PATTERNS [REPLACE_PATTERNS ...]
                        replace pattern
  --cooldown-timeout COOLDOWN_TIMEOUT
                        cooldown timeout
  --address ADDRESS     http log address
  --port PORT           http log port
```
[//]: <> (command-placeholder-end)

### Command `kill-fs-events`
[//]: <> (command-placeholder-start "colima-helper kill-fs-events --help")
```
usage: colima-helper kill-fs-events [-h] [--path PATH]

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  watched path
```
[//]: <> (command-placeholder-end)

### fs-events

fsevent needs `coreutils` (`sudo apk add coreutils`) to use microsecond touch command

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

log: `/tmp/colima-helper-fs-events-projectname.log`
pid: `/tmp/colima-helper-fs-events-projectname.pid`

to kill previous version pid file instance:

`ls /tmp/colima-helper-fs-events.pid && kill -9 &grave;cat /tmp/colima-helper-fs-events.pid &grave; && rm /tmp/colima-helper-fs-events.pid; rm /tmp/colima-helper-fs-events.log`

# Todo
- migrate daemon mode to https://pypi.org/project/launchctl/ for fs-event

Merge requests are welcomed

