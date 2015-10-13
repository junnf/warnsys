#!/usr/bin/env python

from string import Template

class WarnTemplate(Template):
    '''use delimiter = $'''
    delimiter = '$'

def test():
    string_temp = "$a like $b"
    t = WarnTemplate(string_temp)
    d = {'a':'wo','b':'cat'}
    print t.substitute(d)
    print WarnTemplate.delimiter
    print Template.delimiter

if __name__ == '__main__':
    test()
