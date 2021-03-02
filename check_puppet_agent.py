#!/usr/bin/python3
# Requirements:
#  pip3 install python-dateutil click NagiosCheckHelper pyyaml

from NagiosCheckHelper import NagErrors, NagEval
from datetime import datetime
from yaml import load
try:
        from yaml import CLoader as Loader
except ImportError:
        from yaml import Loader


import click
import dateutil.parser

class Globals(object):
    def __init__(self, statusfile=None):
        self.statusfile = statusfile

@click.group()
@click.option("--statusFile", "-s", default="/opt/puppetlabs/puppet/cache/state/last_run_report.yaml", help="Puppet Status yaml file")
@click.pass_context
def cli(ctx, statusfile):
    """This script parses the Puppet status file and monitors for errors

    \b
    Commands:
    success	- Test that the last run was successful
    lastRunTime	- Number of seconds since last Run

    \b
    Examples:
    check_puppet_agent -s last_run_report.yaml success
    check_puppet_agent -s last_run_report.yaml lastRunTime -w 1920 -c 7200
    """
    ctx.obj = Globals(statusfile)

@cli.command("lastRunTime")
@click.option("--warning", "-w", default=1920, help="Warn when last run time exceeds # of seconds")
@click.option("--critical", "-c", default=7200, help="Critical when last run time exceeds # of seconds")
@click.pass_context
def lastRunTime(ctx, warning, critical):
    nerr = NagErrors()
    neval = NagEval(nerr)

    with open(ctx.obj.statusfile, 'r') as f:
    	f.readline()
    	fcontents = f.read()

    sf = load(fcontents, Loader=Loader)

    lastrun = datetime.timestamp(dateutil.parser.parse(sf["time"]))
    now = datetime.timestamp(datetime.now())
    neval.evalNumberAsc(int(now-lastrun), warningAbove=warning, criticalAbove=critical, numberUnits=" sec")
    nerr.printStatus()
    nerr.doExit()

@cli.command("success")
@click.pass_context
def success(ctx):
    nerr = NagErrors()
    neval = NagEval(nerr)

    with open(ctx.obj.statusfile, 'r') as f:
    	f.readline()
    	fcontents = f.read()

    sf = load(fcontents, Loader=Loader)

    neval.evalEnum(sf["status"], okValues=['changed', 'unchanged'], criticalValues=['failed'], prefixText="Status ")
    for log in sf["logs"]:
        if log["level"] == "notice":
            continue
        print("Log %s %s"%(log["level"], log["time"]))
        print(log["message"])
        print("\n")

    nerr.printStatus()
    nerr.doExit()


if __name__ == "__main__":
    cli()
