#!/usr/bin/python3
"""shorewall check for status

This check determines if shorewall is active.
"""

import nagiosplugin
import argparse
import subprocess

class Shorewall(nagiosplugin.Resource):

    def run_shorewall_status(shorewall_bin='/sbin/shorewall'):
        try:
            status = subprocess.check_output([shorweall_bin, 'status'], stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            print('{}'.format(e))
        print(status)

    def probe(self):
        self.run_shorewall_status()
        return [nagiosplugin.Metric('shorewall', True, context='null')]


def main():
    
    check = nagiosplugin.Check(Shorewall())
    check.main()


if __name__ == '__main__':
    main()
