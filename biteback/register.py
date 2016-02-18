#!/usr/bin/env python

tests = []

def get():
    global tests
    return tests;

def put(test):
    global tests
    tests.append(test)
