#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("one", help="First positional argument")
parser.add_argument("two", help="Second positional argument")
parser.add_argument("-A","--aaa", help="An Example Optional argument, which by default, requires a parameter")
parser.add_argument("-B","--bbb", type=int, help="An Example Optional argument that requires an Integer parameter")
parser.add_argument("-C","--ccc", choices=["start","stop"],
                                  default="stop",
                                  help="An Example Optional argument that takes only one of a specific set of parameter values, and can be defaulted to some specific value if not provided")
parser.add_argument("-f","--flag",action="store_true", help="An Example Optional argument that will behave as flag")
args = parser.parse_args()

print("one = " + args.one)
print("two = " + args.two)
print("A|aaa = " + args.aaa if args.aaa else "A|aaa =: not provided")
print("B|bbb = " + str(args.bbb) if args.bbb else "B|bbb := not provided")
print("C|ccc = " + args.ccc if args.ccc else "C|ccc := not provided")
print("f|flag = " + str(args.flag)  if args.flag else "f|flag := not provided")
