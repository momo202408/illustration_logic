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

    def _check_consistency(self, board):
        """
        現在のボードの状態がヒントと矛盾しないかチェックし、
        単純なロジックで確定できるマスを埋める。
        戻り値: (矛盾がないか, 更新されたボード)
        """
        changed = True
        while changed:
            changed = False

            # 行のチェックと更新
            for i in range(self.height):
                current_row = board[i, :]
                possible_lines = self._get_possible_lines(self.row_hints[i], self.width)
                
                valid_lines = [
                    line for line in possible_lines
                    if all(current_row[j] in (UNKNOWN, line[j]) for j in range(self.width))
                ]
                
                if not valid_lines:
                    return False, None  # 矛盾発生

                for j in range(self.width):
                    if current_row[j] == UNKNOWN:
                        first_val = valid_lines[0][j]
                        if all(line[j] == first_val for line in valid_lines):
                            board[i, j] = first_val
                            changed = True

            # 列のチェックと更新
            for j in range(self.width):
                current_col = board[:, j]
                possible_lines = self._get_possible_lines(self.col_hints[j], self.height)
                
                valid_lines = [
                    line for line in possible_lines
                    if all(current_col[i] in (UNKNOWN, line[i]) for i in range(self.height))
                ]

                if not valid_lines:
                    return False, None # 矛盾発生
                
                for i in range(self.height):
                    if current_col[i] == UNKNOWN:
                        first_val = valid_lines[0][i]
                        if all(line[i] == first_val for line in valid_lines):
                            board[i, j] = first_val
                            changed = True
        return True, board

    def solve(self):
        """パズルを解くためのメイン関数。再帰的な解法を呼び出す。"""
        # 初めに基本的な絞り込みを行う
        is_consistent, initial_board = self._check_consistency(self.board.copy())
        if not is_consistent:
            print("\nInitial board is inconsistent. No solution possible.")
            self.print_board()
            return

        solution = self._solve_recursive(initial_board)
        
        if solution is not None:
            self.board = solution
            print("\nSolution found:")
        else:
            print("\nNo solution found.")

        self.print_board()

    def _solve_recursive(self, current_board):
        """バックトラッキング（仮置き）を用いた再帰的なソルバー"""
        
        # 未確定のマスを探す
        unknown_pos = np.where(current_board == UNKNOWN)
        if len(unknown_pos[0]) == 0:
            return current_board  # すべてのマスが確定したら、それが解

        # 最初の未確定のマスで試行錯誤する
        i, j = unknown_pos[0][0], unknown_pos[1][0]

        # 1. マスを FILLED (■) だと仮定してみる
        board_copy_filled = current_board.copy()
        board_copy_filled[i, j] = FILLED
        is_consistent, deduced_board = self._check_consistency(board_copy_filled)
        if is_consistent:
            solution = self._solve_recursive(deduced_board)
            if solution is not None:
                return solution

        # 2. マスを EMPTY (.) だと仮定してみる
        board_copy_empty = current_board.copy()
        board_copy_empty[i, j] = EMPTY
        is_consistent, deduced_board = self._check_consistency(board_copy_empty)
        if is_consistent:
            solution = self._solve_recursive(deduced_board)
            if solution is not None:
                return solution
            
        # どちらの仮定でも解けなかった
        return None






if __name__ == '__main__':
    # 5x5 "Cross" shape hints
    row_hints = [[1], [5], [1], [1], [1]]
    col_hints = [[1], [5], [1], [1], [1]]

    solver = NonogramSolver(row_hints, col_hints)
    print("\n\nInitial board (Solving Cross-shape):")
    solver.print_board()
    solver.solve()
