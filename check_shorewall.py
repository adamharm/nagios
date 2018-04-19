#!/usr/bin/python3
"""shorewall check for status

This check determines if shorewall is active.

This plugin needs to be executed with root privileges (usually via sudo)
"""

import nagiosplugin
import argparse
import subprocess
import logging

_log = logging.getLogger('nagiosplugin')


class Shorewall(nagiosplugin.Resource):
    def probe(self):
        try:
            status = subprocess.check_output(['sudo', '/sbin/shorewall', 'status'], stderr=subprocess.STDOUT)
            _log.debug('shorewall status output: {}'.format(status))
            return [nagiosplugin.Metric('shorewall_state', True, context='shorewall')]
        except subprocess.CalledProcessError as e:
            if e.returncode is 4:
                return [nagiosplugin.Metric('shorewall_state', False, context='shorewall')]
            raise nagiosplugin.CheckError('cannot determine status of shorewall: {}'.format(e.output.rstrip().decode('ascii')))


class BooleanContext(nagiosplugin.Context):
    def __init__(self, name):
        super(BooleanContext, self).__init__(name)

    def evaluate(self, metric, resource):
        if metric.value is True:
            return self.result_cls(nagiosplugin.Ok, 'Shorewall running')
        return self.result_cls(nagiosplugin.Critical, 'Shorewall not running')


@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-v', '--verbose', action='count', default=0)
    args = argp.parse_args()
    check = nagiosplugin.Check(Shorewall(),
                               BooleanContext('shorewall'))
    check.main(args.verbose)

if __name__ == '__main__':
    main()
