# check_puppet_agent

Usage: check_puppet_agent.sh [OPTIONS] COMMAND [ARGS]...

This script parses the Puppet status file and monitors for errors

## Commands:
success     - Test that the last run was successful\
lastRunTime - Number of seconds since last Run\

## Global Options:
  -s, --statusFile TEXT  Puppet Status yaml file (default:/opt/puppetlabs/puppet/cache/state/last_run_report.yaml)\
  --help                 Show this message and exit.\

### Command: success
This tests that the run was successfull or not. Will print errored log lines if failed.

### Command: lastRunTime
This tests the last run time of the puppet agent.

#### lastRunTime Options:
-w, --warning INTEGER   Warn when last run time exceeds # of seconds (default: 1920)\
-c, --critical INTEGER  Critical when last run time exceeds # of seconds (default: 7200)


## Examples:
```
check_puppet_agent -s last_run_report.yaml success
check_puppet_agent -s last_run_report.yaml lastRunTime -w 1920 -c 7200
```
 
