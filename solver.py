import numpy as np

# マスの状態を定義
UNKNOWN = 0
FILLED = 1
EMPTY = -1

class NonogramSolver:
    def __init__(self, row_hints, col_hints):
        self.row_hints = row_hints
        self.col_hints = col_hints
        self.height = len(row_hints)
        self.width = len(col_hints)
        self.board = np.full((self.height, self.width), UNKNOWN)

    def print_board(self):
        """盤面とヒントをきれいに表示する"""
        max_row_hint_len = max(len(h) for h in self.row_hints) if self.row_hints else 0
        row_hint_width = max_row_hint_len * 2 

        # Print column hints vertically
        max_col_hint_len = max(len(h) for h in self.col_hints) if self.col_hints else 0
        for i in range(max_col_hint_len):
            line = " " * (row_hint_width + 2)
            for h in self.col_hints:
                hint_idx = i - (max_col_hint_len - len(h))
                if hint_idx >= 0:
                    line += f"{h[hint_idx]} "
                else:
                    line += "  "
            print(line)
        
        print(" " * row_hint_width + "--" * self.width)

        # Print row hints and the board
        for i in range(self.height):
            hint_str = " ".join(map(str, self.row_hints[i]))
            line = f"{hint_str.rjust(row_hint_width)}| "
            for j in range(self.width):
                cell = self.board[i, j]
                if cell == FILLED:
                    line += "■ "
                elif cell == EMPTY:
                    line += ". "
                else:
                    line += "? "
            print(line)

    def _get_possible_lines(self, hints, length):
        """
        与えられたヒントと長さに合致する、可能性のあるすべての行/列のパターンを生成する
        """
        def _generate(h_idx, start_pos):
            if h_idx == len(hints):
                # All hints placed, yield a valid full line
                yield [EMPTY] * length

            else:
                hint = hints[h_idx]
                
                # Calculate remaining space needed for subsequent hints
                remaining_space = sum(hints[h_idx+1:]) + len(hints[h_idx+1:])
                
                # Iterate through all possible start positions for the current hint
                for pos in range(start_pos, length - remaining_space - hint + 1):
                    # For each valid sub-pattern for the rest of the hints...
                    for sub_pattern in _generate(h_idx + 1, pos + hint + 1):
                        # Construct the full pattern
                        new_line = list(sub_pattern)
                        for i in range(hint):
                            new_line[pos + i] = FILLED
                        yield new_line
        
        if not hints or hints == [0]:
            return [[EMPTY] * length]
        
        return list(_generate(0, 0))

    def solve(self):
        """ロジックに基づいてパズルを解く"""
        changed = True
        while changed:
            changed = False

            # 1. 行の更新
            for i in range(self.height):
                current_row_view = self.board[i, :]
                possible_lines = self._get_possible_lines(self.row_hints[i], self.width)
                
                # 現在の行の状態と矛盾しないパターンのみに絞り込む
                valid_lines = [
                    line for line in possible_lines 
                    if all(current_row_view[j] in (UNKNOWN, line[j]) for j in range(self.width))
                ]
                
                if not valid_lines: continue

                # 全ての有効なパターンで共通するセルを確定させる
                for j in range(self.width):
                    if current_row_view[j] == UNKNOWN:
                        first_val = valid_lines[0][j]
                        if all(line[j] == first_val for line in valid_lines):
                            self.board[i, j] = first_val
                            changed = True

            # 2. 列の更新
            for j in range(self.width):
                current_col_view = self.board[:, j]
                possible_lines = self._get_possible_lines(self.col_hints[j], self.height)
                
                valid_lines = [
                    line for line in possible_lines
                    if all(current_col_view[i] in (UNKNOWN, line[i]) for i in range(self.height))
                ]

                if not valid_lines: continue
                
                for i in range(self.height):
                    if current_col_view[i] == UNKNOWN:
                        first_val = valid_lines[0][i]
                        if all(line[i] == first_val for line in valid_lines):
                            self.board[i, j] = first_val
                            changed = True
        
        print("\nFinal board:")
        self.print_board()


if __name__ == '__main__':
    # 8x6 "Ship" shape hints
    row_ship = [[1], [2], [3], [7], [7], []]
    col_ship = [[2], [2], [3], [3], [4], [5], [2], []]

    solver = NonogramSolver(row_ship, col_ship)
    print("Initial board (Solving Ship-shape):")
    solver.print_board()
    solver.solve()
