BOARD_SIZE = 9 # it's a square

def strip_zero_unique(list):
  strip_zero = [i for i in list if i != 0]

  return len(strip_zero) == len(set(strip_zero))

class Board:
  def __init__(self):
    self.cells = [ [ 0 for _ in range(1 + BOARD_SIZE) ] for _ in range(1 + BOARD_SIZE) ]

    self.known_points = []
    self.black_dot_constraints = []
    self.white_dot_constraints = []
    self.arrow_constraints = []
    self.thermo_constraints = []
    self.palindrome_constraints = []
    self.box_constraints = []

  def get_cells(self):
    return [ line[1:] for line in self.cells[1:] ]

  def set_cell(self, line, col, value):
    self.cells[line][col] = value
  

  def add_known_point(self, line, col, value):
    self.known_points.append((line, col, value))

  # black dot connects two adjacent cells, which must have a ratio of 2:1
  def add_black_dot_constraint(self, c1, c2):
    self.black_dot_constraints.append((c1, c2))

  # white dot connects two adjacent cells, which must contain consecutive numbers
  def add_white_dot_constraint(self, c1, c2):
    self.white_dot_constraints.append((c1, c2))

  # the arrow connects multiple cells, and the numbers must sum up to the start of the arrow
  # arrow will be passed as a list of cells, from start to end
  def add_arrow_constraint(self, cell_list):
    self.arrow_constraints.append(cell_list)
  
  # thermo connects multiple cells, and the numbers must be increasing from the bottom up
  # thermo will be passed as a list of cells, from bottom to top
  def add_thermo_constraint(self, cell_list):
    self.thermo_constraints.append(cell_list)
  
  # palindrome is self-explanatory
  # also passed as a list of cells, in the specific order 
  def add_palindrome_constraint(self, cell_list):
    self.palindrome_constraints.append(cell_list)

  # box constains multiple cells, and the numbers must be unique and sum to a specific number
  # box will be passed as a tuple containing the sum and the list of cells, in any order
  def add_box_constraint(self, sum, cell_list):
    self.box_constraints.append((sum, cell_list))

  
  def check_known_points(self, line, col):
    for constraint in self.known_points:
      if constraint[0] == line and constraint[1] == col:
        return constraint[2] == self.cells[line][col]
      
    return True

  def check_line(self, line, col):
    # print(f'For line {line}, col {col}, checking {self.cells[line][col]} vs {self.cells[line][1:col]}')
    return self.cells[line][col] not in self.cells[line][1:col]
  
  def check_col(self, line, col):
    # print(f'For line {line}, col {col}, checking {self.cells[line][col]} vs {[ self.cells[i][col] for i in range(1, col) ]}')
    return self.cells[line][col] not in [ cell_line[col] for cell_line in self.cells[1:line] ]
  
  def check_3x3(self, line, col):
    line3 = ((line - 1) // 3)
    col3 =  ((col - 1) // 3)

    # print(f'For line {line}, col {col}, checking {self.cells[line][col]} vs {[ self.cells[line3 * 3 + i][col3 * 3 + j] for i in range(1, 4) for j in range(1, 4) if (line3 * 3 + i != line or col3 * 3 + j != col) ]}')

    for i in range(1, 4):
      for j in range(1, 4):
        if (line3 * 3 + i != line or col3 * 3 + j != col) and self.cells[line3 * 3 + i][col3 * 3 + j] == self.cells[line][col]:
          return False
        
    return True
  
  def check_black_dot(self, line, col):
    for constraint in self.black_dot_constraints:
      if constraint[0] == (line, col):
        other_line = constraint[1][0]
        other_col = constraint[1][1]

        return self.cells[other_line][other_col] == 0 or self.cells[line][col] * 2 == self.cells[other_line][other_col] or self.cells[line][col] == self.cells[other_line][other_col] * 2
      
      if constraint[1] == (line, col):
        other_line = constraint[0][0]
        other_col = constraint[0][1]

        return self.cells[other_line][other_col] == 0 or self.cells[line][col] * 2 == self.cells[other_line][other_col] or self.cells[line][col] == self.cells[other_line][other_col] * 2
      
    return True
  
  def check_white_dot(self, line, col):
    for constraint in self.white_dot_constraints:
      if constraint[0] == (line, col):
        other_line = constraint[1][0]
        other_col = constraint[1][1]

        return self.cells[other_line][other_col] == 0 or abs(self.cells[line][col] - self.cells[other_line][other_col]) == 1
      
      if constraint[1] == (line, col):
        other_line = constraint[0][0]
        other_col = constraint[0][1]

        return self.cells[other_line][other_col] == 0 or abs(self.cells[line][col] - self.cells[other_line][other_col]) == 1
      
    return True
  
  def check_arrow(self, line, col):
    for constraint in self.arrow_constraints:
      if (line, col) not in constraint:
        continue

      if not strip_zero_unique([ self.cells[cell[0]][cell[1]] for cell in constraint ]):
        return False

      target_sum_point = constraint[0]
      target_sum = self.cells[target_sum_point[0]][target_sum_point[1]]

      found_zero = False
      for cell in constraint[1:]:
        if self.cells[cell[0]][cell[1]] == 0:
          found_zero = True
          break
        target_sum -= self.cells[cell[0]][cell[1]]
      
      return found_zero or target_sum == 0
    
    return True

  def check_thermo(self, line, col):
    for constraint in self.thermo_constraints:
      if (line, col) not in constraint:
        continue

      if not strip_zero_unique([ self.cells[cell[0]][cell[1]] for cell in constraint ]):
        return False

      found_zero = False
      for cell in constraint:
        if self.cells[cell[0]][cell[1]] == 0:
          found_zero = True
          break
      
      thermo_values = [ self.cells[cell[0]][cell[1]] for cell in constraint ]
      return found_zero or all([ thermo_values[i] < thermo_values[i + 1] for i in range(len(thermo_values) - 1) ])
    
    return True

  def check_palindrome(self, line, col):
    for constraint in self.palindrome_constraints:
      if (line, col) not in constraint:
        continue
    
      palindrome_values = [ self.cells[cell[0]][cell[1]] for cell in constraint ]
      
      return all([ palindrome_values[i] == 0 or palindrome_values[i] == palindrome_values[len(palindrome_values) - i - 1] or palindrome_values[len(palindrome_values) - i - 1 == 0] for i in range(len(palindrome_values) // 2) ])
    
    return True

  def check_box(self, line, col):
    for constraint in self.box_constraints:
      box_sum = constraint[0]

      if (line, col) not in constraint[1]:
        continue

      if not strip_zero_unique([ self.cells[cell[0]][cell[1]] for cell in constraint[1] ]):
        return False

      found_zero = False
      for cell in constraint[1]:
        if self.cells[cell[0]][cell[1]] == 0:
          found_zero = True
          break
      
      box_values = [ self.cells[cell[0]][cell[1]] for cell in constraint[1] ]
      return found_zero or sum(box_values) == box_sum
    
    return True

  # check all constraints + sudoku default ones
  def check_at(self, line, col):
    if not self.check_known_points(line, col):
      return False
    
    if not self.check_line(line, col):
      return False
    
    if not self.check_col(line, col):
      return False
    
    if not self.check_3x3(line, col):
      return False
    
    if not self.check_black_dot(line, col):
      return False
    
    if not self.check_white_dot(line, col):
      return False
    
    if not self.check_arrow(line, col):
      return False
    
    if not self.check_thermo(line, col):
      return False
    
    if not self.check_box(line, col):
      return False
    
    if not self.check_palindrome(line, col):
      return False

    return True
  
  def save_solution(self):
    with open('solution.txt', 'w') as savefile:
      for line in self.cells[1:]:
        savefile.write(' '.join([ str(cell) for cell in line[1:] ]))
        savefile.write('\n')