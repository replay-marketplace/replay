#! /bin/bash

# Run test coverage and generate report
coverage run -m unittest discover tests
coverage report -m
