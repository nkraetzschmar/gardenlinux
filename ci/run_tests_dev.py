#!/usr/bin/env python3

# default run command (runs all tests in  integration_tests):
# ci/test_tests.pytest.py
# All arguments are passed to pytest.
# run specific tests, example (see also -k -m options in 
# https://docs.pytest.org/en/6.2.x/usage.html#specifying-tests-selecting-tests):
# ci/test_tests.py integration_tests/aws/aws_test.py

import os, sys
import sys,os;sys.path.insert(1,os.path.abspath("ci/steps"))
import run_tests
if len(sys.argv) > 1:
    args = sys.argv[1:]
else:
    args = None

run_tests.run_tests(
    architecture="amd64",
    cicd_cfg_name= "default",
    committish="ad9ae55f55e75ac82ccebadbd27e572c2c1cf0c6",
    gardenlinux_epoch= "477",
    modifiers='_nopkg,_prod,_readonly,_slim,base,cloud,gardener,server',
    platform="aws",
    publishing_actions="run_tests, manifests",
    repo_dir="/Users/d058463/git/gardenlinux",
    suite="bullseye",
    snapshot_timestamp="20210721",
    version="477.0",
    pytest_args=args,
)
