import sys
import os

from board import *
from parsers import *

def init():
  '''
  'problem.txt' file format
  num_points_known
  {line} {col} {value} for each known point, split by newline
  num_black_dot_constraints
  {line1} {col1} {line2} {col2} for each black dot constraint, split by newline
  num_white_dot_constraints
  {line1} {col1} {line2} {col2} for each white dot constraint, split by newline
  num_arrow_constraints
  {num_cells} {line1} {col1} {line2} {col2} ... {lineN} {colN} for each arrow constraint, split by newline
  num_thermo_constraints
  {num_cells} {line1} {col1} {line2} {col2} ... {lineN} {colN} for each thermo constraint, split by newline
  num_palindrome_constraints
  {num_cells} {line1} {col1} {line2} {col2} ... {lineN} {colN} for each palindrome constraint, split by newline
  num_box_constraints
  {sum} {num_cells} {line1} {col1} {line2} {col2} ... {lineN} {colN} for each box constraint, split by newline
  '''

  board = Board()

  with open('./problem.txt', 'r') as f:
    # read known points
    num_known_points = int(f.readline())

    for _ in range(num_known_points):
      line = f.readline().split(' ')

      args = known_point_parser.parse_args(line)
      board.add_known_point(args.line, args.col, args.value)

      print(f'Added known point: ({args.line}, {args.col}) = {args.value}')

    # read black dot constraints
    num_black_dot_constraints = int(f.readline())

    for _ in range(num_black_dot_constraints):
      line = f.readline().split(' ')

      dot_constraint_parser.parse_args(line)

      args = dot_constraint_parser.parse_args(line)
      board.add_black_dot_constraint((args.line1, args.col1), (args.line2, args.col2))

      print(f'Added black dot constraint: ({args.line1}, {args.col1}) and ({args.line2}, {args.col2})')

    # read white dot constraints
    num_white_dot_constraints = int(f.readline())

    for _ in range(num_white_dot_constraints):
      line = f.readline().split(' ')

      dot_constraint_parser.parse_args(line)

      args = dot_constraint_parser.parse_args(line)
      board.add_white_dot_constraint((args.line1, args.col1), (args.line2, args.col2))

      print(f'Added white dot constraint: ({args.line1}, {args.col1}) and ({args.line2}, {args.col2})')

    # read arrow constraints
    num_arrow_constraints = int(f.readline())

    for _ in range(num_arrow_constraints):
      line = f.readline().split()

      num_points_in_arrow = int(line[0])

      line = line[1:]
      arrow_constraint_list = []

      if len(line) != num_points_in_arrow * 2:
        print(f'Invalid arrow constraint: expected {num_points_in_arrow} points, got {len(line) // 2}')

      for i in range(0, len(line), 2):
        point = simple_point_parser.parse_args(line[i:i+2])

        arrow_constraint_list.append((point.line, point.col))

      board.add_arrow_constraint(arrow_constraint_list)
      print(f'Added arrow constraint: {" -> ".join([ f"({point[0]}, {point[1]})" for point in arrow_constraint_list ]) }')

    # read thermo constraints
    num_thermo_constraints = int(f.readline())

    for _ in range(num_thermo_constraints):
      line = f.readline().split()

      num_points_in_thermo = int(line[0])

      line = line[1:]
      thermo_constraint_list = []

      if len(line) != num_points_in_thermo * 2:
        print(f'Invalid thermo constraint: expected {num_points_in_thermo} points, got {len(line) // 2}')

      for i in range(0, len(line), 2):
        point = simple_point_parser.parse_args(line[i:i+2])

        thermo_constraint_list.append((point.line, point.col))

      board.add_thermo_constraint(thermo_constraint_list)
      print(f'Added thermo constraint: {" -> ".join([ f"({point[0]}, {point[1]})" for point in thermo_constraint_list ]) }')

    # read palindrome constraints
    num_palindrome_constraints = int(f.readline())

    for _ in range(num_palindrome_constraints):
      line = f.readline().split()

      num_points_in_palindrome = int(line[0])

      line = line[1:]
      palindrome_constraint_list = []

      if len(line) != num_points_in_palindrome * 2:
        print(f'Invalid palindrome constraint: expected {num_points_in_palindrome} points, got {len(line) // 2}')

      for i in range(0, len(line), 2):
        point = simple_point_parser.parse_args(line[i:i+2])

        palindrome_constraint_list.append((point.line, point.col))

      board.add_palindrome_constraint(palindrome_constraint_list)
      print(f'Added palindrome constraint: {" -> ".join([ f"({point[0]}, {point[1]})" for point in palindrome_constraint_list ]) }')

    # read box constraints
    num_box_constraints = int(f.readline())

    for _ in range(num_box_constraints):
      line = f.readline().split()

      box_sum = int(line[0])
      num_points_in_box = int(line[1])

      line = line[2:]
      box_constraint_list = []

      if len(line) != num_points_in_box * 2:
        print(f'Invalid box constraint: expected {num_points_in_box} points, got {len(line) // 2}')

      for i in range(0, len(line), 2):
        point = simple_point_parser.parse_args(line[i:i+2])

        box_constraint_list.append((point.line, point.col))

      board.add_box_constraint(box_sum, box_constraint_list)
      print(f'Added box constraint: {box_sum} = {" + ".join([ f"({point[0]}, {point[1]})" for point in box_constraint_list ]) }')

  return board


def backtrack(board, depth_lin = 1, depth_col = 1):
  for i in range(1, 10):
    board.set_cell(depth_lin, depth_col, i)

    if board.check_at(depth_lin, depth_col):
      if depth_lin == BOARD_SIZE and depth_col == BOARD_SIZE:
        board.save_solution()
        print(f'Solved! Check solution.txt to find the solution')
        sys.exit(0)
      elif depth_col == BOARD_SIZE:
        backtrack(board, depth_lin + 1, 1)
      else:
        backtrack(board, depth_lin, depth_col + 1)
  
  board.set_cell(depth_lin, depth_col, 0)
        


def main():
  b = init()

  backtrack(b)

main()