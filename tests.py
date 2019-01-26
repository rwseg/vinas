# -*- coding: utf-8 -*-
import unittest
from collections import OrderedDict

from vinas import Cmd, parse_arg_list


class CmdTest(unittest.TestCase):
    def setUp(self):
        self.cmd = Cmd('vina')
        self.cmd.set_arg('--receptor', 'receptor.pdbqt')
        self.cmd.set_arg('--ligand', 'ligand.pdbqt')
        self.cmd.set_arg('--help')

    def test_set_arg(self):
        self.assertIn('--receptor', self.cmd.args)
        self.assertIn('--ligand', self.cmd.args)
        self.assertIn('--help', self.cmd.args)
        self.assertEqual(self.cmd.args['--receptor'], 'receptor.pdbqt')
        self.assertEqual(self.cmd.args['--ligand'], 'ligand.pdbqt')

    def test_args_to_list(self):
        self.assertListEqual(
            self.cmd.args_to_list(),
            ['vina', '--receptor', 'receptor.pdbqt', '--ligand', 'ligand.pdbqt', '--help']
        )


class ParseArgListTest(unittest.TestCase):
    def test(self):
        arg_list = [
            '--receptor=receptor.pdbqt',
            '--center_x=10',
            '--center_y=10',
            '--center_z=10',
            '--size_x=10',
            '--size_y=10',
            '--size_z=10',
            '--out=out.pdbqt',
            '--num_modes=9',
            '--energy_range=1',
        ]
        arg_dict = OrderedDict([
            ('--receptor', 'receptor.pdbqt'),
            ('--center_x', '10'),
            ('--center_y', '10'),
            ('--center_z', '10'),
            ('--size_x', '10'),
            ('--size_y', '10'),
            ('--size_z', '10'),
            ('--out', 'out.pdbqt'),
            ('--num_modes', '9'),
            ('--energy_range', '1'),
        ])
        self.assertDictEqual(arg_dict, parse_arg_list(arg_list))
