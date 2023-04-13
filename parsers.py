import argparse

known_point_parser = argparse.ArgumentParser(description='Known point parser')
known_point_parser.add_argument('line', type=int, help='Line of the known point')
known_point_parser.add_argument('col', type=int, help='Column of the known point')
known_point_parser.add_argument('value', type=int, help='Value of the known point')

dot_constraint_parser = argparse.ArgumentParser(description='Dot constraint parser | I didn\'t bother making two of them, they work the exact same')
dot_constraint_parser.add_argument('line1', type=int, help='Line of the first cell')
dot_constraint_parser.add_argument('col1', type=int, help='Column of the first cell')
dot_constraint_parser.add_argument('line2', type=int, help='Line of the second cell')
dot_constraint_parser.add_argument('col2', type=int, help='Column of the second cell')
# todo verify if they're adjacent

simple_point_parser = argparse.ArgumentParser(description='Point parser')
simple_point_parser.add_argument('line', type=int, help='Line of the point')
simple_point_parser.add_argument('col', type=int, help='Column of the point')
