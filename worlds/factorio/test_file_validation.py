"""Tests for error messages from YAML validation."""

import os
import unittest

import WebHostLib.check

FACTORIO_YAML="""
game: Factorio
Factorio:
  world_gen:
    autoplace_controls:
      coal:
        richness: 1
        frequency: {}
        size: 1
"""

def yamlWithFrequency(f):
    return FACTORIO_YAML.format(f)


class TestFileValidation(unittest.TestCase):
    def test_out_of_range(self):
        results, _ = WebHostLib.check.roll_options({"bob.yaml": yamlWithFrequency(1000)})
        self.assertIn("between 0 and 6", results["bob.yaml"])

    def test_bad_non_numeric(self):
        results, _ = WebHostLib.check.roll_options({"bob.yaml": yamlWithFrequency("not numeric")})
        self.assertIn("float", results["bob.yaml"])
        self.assertIn("int", results["bob.yaml"])

    def test_good_float(self):
        results, _ = WebHostLib.check.roll_options({"bob.yaml": yamlWithFrequency(1.0)})
        self.assertIs(results["bob.yaml"], True)

    def test_good_int(self):
        results, _ = WebHostLib.check.roll_options({"bob.yaml": yamlWithFrequency(1)})
        self.assertIs(results["bob.yaml"], True)
