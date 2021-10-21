# list_manager
Simple whitelists and blacklists CLI manager

## Installation
`https://github.com/xaled/list_manager.git` 

## Usage
```
$ ./list_manager.py  --help
usage: list_manager.py [-h] {add,remove,cron} ...

positional arguments:
  {add,remove,cron}  action
    add              add new entry
    remove           remove entry
    cron             run cron

optional arguments:
  --list-dir LIST_DIR  target lists directory (default: )
  -h, --help         show this help message and exit
```
```
$ ./list_manager.py add --help
usage: list_manager.py add [-h] [-v VALIDITY] [-c COMMENT] [-l LIST] range

positional arguments:
  range                 IP range

optional arguments:
  -h, --help            show this help message and exit
  -v VALIDITY, --validity VALIDITY
                        validity in days (default: 7)
  -c COMMENT, --comment COMMENT
                        entry comment
  -l LIST, --list LIST  target list (default: default_list)
```
```
$ ./list_manager.py remove --help
usage: list_manager.py remove [-h] [-l LIST] range

positional arguments:
  range                 IP range

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  target list (default: default_list)

```
## Examples
### Adding IP addresses
```
$ ./list_manager.py add 192.168.1.0/24
$ ./list_manager.py add 192.168.1.0
$ cat default_list 
192.168.1.0/24 # no comment - expires in 6 days
192.168.1.0 # no comment - expires in 6 days
$ ./list_manager.py add 192.168.1.0 -l blacklist
$ cat blacklist 
192.168.1.0 # no comment - expires in 6 days
```
### Cron configuration
```0 0 * * * /path/to/script/list_manager.py cron```
