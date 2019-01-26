# -*- coding: utf-8 -*-
import os
import logging
import argparse
import subprocess
from collections import OrderedDict

"""vinas
run vina against a receptor and a directory
of ligand with same argument
"""


def check_file_or_directory(file_or_directory):
    """check if the file or directory existed"""
    if os.path.exists(file_or_directory):
        return os.path.abspath(file_or_directory)
    raise argparse.ArgumentTypeError('invalid directory: %s' % file_or_directory)


class Cmd(object):
    def __init__(self, name):
        self.name = name
        self.args = OrderedDict()

    def __repr__(self):
        return self.name

    def args_to_list(self):
        """convert args dict to list
        eg:
            cmd = Cmd('vina')
            cmd.set_arg('--receptor', '/home/some_user/some_receptor.pdbqt')
            cmd.set_arg('--ligand', '/home/some_user/some_ligand.pdbqt')
            arg_list = cmd.args_to_list()

        the result will be:
            ['--receptor', '/home/some_user/some_receptor.pdbqt',
            '--ligand', '/home/some_user/some_ligand.pdbqt']
        """
        arg_list = [self.name]
        for arg_name, arg_value in self.args.items():
            if arg_value is None:
                arg_list.append(arg_name)
            else:
                arg_list.append(arg_name)
                arg_list.append(arg_value)
        return arg_list

    def set_arg(self, name, value=None):
        """set arg
        eg:
            cmd = Cmd('vina')
            cmd.set_arg('--receptor', '/home/some_user/some_receptor.pdbqt')

        if you want to send an positional arg, you could do like this:
            cmd = Cmd('vina')
            cmd.set_arg('--help')
        """
        self.args[name] = value

    def run(self):
        """run command
        a subprocess CompletedProcess will be returned.
        """
        return subprocess.run(
            self.args_to_list(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


def parse_arg_list(arg_list):
    """parse a list of arg to dict"""
    arg_dict = OrderedDict()
    for arg in arg_list:
        if '=' in arg:
            arg_name, arg_value = arg.split('=', 1)
        else:
            arg_name = arg
            arg_value = None
        arg_dict[arg_name] = arg_value
    return arg_dict


def get_args():
    """get arguments from commandline"""
    parser = argparse.ArgumentParser(
        'vinas', prefix_chars='+',
        description='run vina against a directory of ligands with same arguments'
    )
    parser.add_argument('+l', '++ligand', type=check_file_or_directory,
                        required=True, help='ligand directory')
    parser.add_argument('+o', '++out', type=check_file_or_directory,
                        required=True, help='output directory')
    parser.add_argument('+d', '++debug', action='store_true',
                        required=False, help='enable debug mode')
    parser.add_argument('+v', '++vina', action='append',
                        required=True, help='vina argument')
    args = parser.parse_args()
    return args


def vinas():
    logger = logging.getLogger(__file__)
    args = get_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)
    vina_arg_dict = parse_arg_list(args.vina)

    for ligand_filename in os.listdir(args.ligand):
        logger.debug('run vina against %s' % ligand_filename)
        ligand_file = os.path.join(args.ligand, ligand_filename)
        outfile = os.path.join(args.out, ligand_filename)
        vina_cmd = Cmd('vina')
        vina_cmd.set_arg('--ligand', ligand_file)
        vina_cmd.set_arg('--out', outfile)
        for vina_arg_name, vina_arg_value in vina_arg_dict.items():
            vina_cmd.set_arg(vina_arg_name, vina_arg_value)
        proc = vina_cmd.run()
        try:
            proc.check_returncode()
        except subprocess.CalledProcessError as ce:
            logger.exception(ce)


if __name__ == '__main__':
    vinas()
