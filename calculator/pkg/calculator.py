# calculator/pkg/calculator.py

from collections.abc import Callable


class Calculator:
    def __init__(self) -> None:
        # Binary operators: operator -> (precedence, associativity)
        # Higher number = higher precedence
        self.binary_ops: dict[str, tuple[int, str]] = {
            '+': (1, 'left'),
            '-': (1, 'left'),
            '*': (2, 'left'),
            '/': (2, 'left'),
            '%': (2, 'left'),
            '**': (3, 'right'),  # Exponentiation
        }
        # Unary operators: operator -> function
        self.unary_ops: dict[str, Callable[[float], float]] = {
            '-': lambda a: -a,
            '+': lambda a: a,
        }
        # Precedence for unary operators
        self.unary_precedence = 4  # Higher than ** so unary binds tightest with **

    def evaluate(self, expression: str) -> float | None:
        if not expression or expression.isspace():
            return None
        try:
            tokens = self._tokenize(expression)
            return self._evaluate_infix(tokens)
        except ValueError as e:
            raise ValueError(str(e)) from e

    def _tokenize(self, expression: str) -> list[str]:
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            c = expression[i]
            if c.isspace():
                i += 1
                continue
            if c in '()+-*/%':
                if c == '*' and i + 1 < n and expression[i + 1] == '*':
                    tokens.append('**')
                    i += 2
                    continue
                tokens.append(c)
                i += 1
            elif c.isdigit() or c == '.':
                j = i
                while j < n and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                num_str = expression[i:j]
                if num_str.count('.') > 1:
                    raise ValueError(f"Invalid number: {num_str}")
                tokens.append(num_str)
                i = j
            else:
                raise ValueError(f"Invalid character: {c}")
        return tokens

    def _precedence(self, op: str) -> int:
        if op.startswith("u"):
            return self.unary_precedence
        if op == '(':
            return 0
        if op in self.binary_ops:
            return self.binary_ops[op][0]
        #if op in self.unary_ops: # unreachable/dead
        #    return self.unary_precedence # unreachable/dead
        return 0

    def _associativity(self, op: str) -> str:
        if op in self.binary_ops:
            return self.binary_ops[op][1]
        return 'right'  # Unary is right-associative

    def _apply_binary_op(self, op: str, a: float, b: float) -> float:
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("division by zero")
            return a / b
        if op == '%':
            if b == 0:
                raise ZeroDivisionError("modulo by zero")
            return a % b
        if op == '**':
            return a ** b
        raise ValueError(f"Unknown binary operator: {op}")

    def _apply_top_operator(self, ops: list[str], values: list[float]) -> None:
        """Pop and apply the top operator from the stack."""
        if not ops:
            return
        op = ops.pop()
        if op.startswith("u"):
            real_op = op[1:]
            a = values.pop()
            values.append(self.unary_ops[real_op](a))
        else:
            if len(values) < 2:
                raise ValueError(f"Not enough operands for operator {op}")
            b = values.pop()
            a = values.pop()
            values.append(self._apply_binary_op(op, a, b))
        # if op in self.unary_ops: # Old dead code
        #     if len(values) < 1:
        #         raise ValueError(f"Not enough operands for unary operator {op}")
        #     a = values.pop()
        #     values.append(self.unary_ops[op](a))
        # else:
        #     if len(values) < 2:
        #         raise ValueError(f"Not enough operands for operator {op}")
        #     b = values.pop()
        #     a = values.pop()
        #     values.append(self._apply_binary_op(op, a, b))

    def _should_pop(self, top_op: str, current_op: str) -> bool:
        """Determine if top_op should be popped before pushing current_op."""
        if top_op == '(':
            return False
        top_prec = self._precedence(top_op)
        curr_prec = self._precedence(current_op)
        if top_prec > curr_prec:
            return True
        if top_prec == curr_prec:
            return self._associativity(current_op) == 'left'
        return False

    def _evaluate_infix(self, tokens: list[str]) -> float:
        values: list[float] = []
        ops: list[str] = []
        expect_operand = True  # Start expecting operand or unary op

        for token in tokens:
            # Determine if token is a unary operator (only when expecting operand)
            if token in self.unary_ops and expect_operand:
                #ops.append(token) #version no longer works
                ops.append("u" + token)  # e.g. "u-" for unary minus
                # expect_operand stays True
            elif token in self.binary_ops:
                if expect_operand:
                    raise ValueError(f"Operator '{token}' unexpected")
                # Pop operators with higher or equal precedence (based on associativity)
                while ops and self._should_pop(ops[-1], token):
                    self._apply_top_operator(ops, values)
                ops.append(token)
                expect_operand = True
            elif token == '(':
                if not expect_operand:
                    raise ValueError("'(' unexpected")
                ops.append(token)
                # expect_operand stays True
            elif token == ')':
                if expect_operand:
                    raise ValueError("')' unexpected")
                while ops and ops[-1] != '(':
                    self._apply_top_operator(ops, values)
                if not ops or ops[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                ops.pop()  # Remove '('
                expect_operand = False
            else:
                # Number
                if not expect_operand:
                    raise ValueError(f"Number '{token}' unexpected")
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid number: {token}")
                expect_operand = False

        # Apply remaining operators
        while ops:
            self._apply_top_operator(ops, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")
        return values[0]
