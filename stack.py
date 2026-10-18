import re
from typing import Generic, Iterable, Iterator, List, Mapping, Optional, TypeVar


T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data = data
        self.next: Optional["Node[T]"] = None


class Stack(Generic[T]):
    """A linked last-in, first-out (LIFO) stack."""

    def __init__(self) -> None:
        self.top: Optional[Node[T]] = None
        self._size = 0

    def push(self, data: T) -> None:
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self) -> Optional[T]:
        if self.top is None:
            return None
        popped_node = self.top
        self.top = self.top.next
        popped_node.next = None
        self._size -= 1
        return popped_node.data

    def peek(self) -> Optional[T]:
        if self.top is None:
            return None
        return self.top.data

    def is_empty(self) -> bool:
        return self.top is None

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __iter__(self) -> Iterator[T]:
        current = self.top
        while current is not None:
            yield current.data
            current = current.next

    def print_stack(self) -> None:
        if self.is_empty():
            print("Stack is empty")
            return

        print("Stack elements (top to bottom):")
        for item in self:
            print(item)


_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_TOKEN_RE = re.compile(
    r"\s*(?:(\d+(?:\.\d*)?|\.\d+)([eE][+-]?\d+)?|"
    r"([A-Za-z_]\w*)|(\*\*|//|[()+\-*/%]))"
)
_PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "//": 2,
    "%": 2,
    "u+": 3,
    "u-": 3,
    "**": 4,
}
_RIGHT_ASSOCIATIVE = {"**", "u+", "u-"}


def _pop_required(stack: Stack[T]) -> T:
    item = stack.pop()
    if item is None:
        raise RuntimeError("internal stack unexpectedly became empty")
    return item


def decimal_to_base(number: int, base: int = 2) -> str:
    """Convert a decimal integer to a base from 2 through 36 using a stack."""
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError("number must be an integer")
    if not isinstance(base, int) or isinstance(base, bool) or not 2 <= base <= 36:
        raise ValueError("base must be an integer from 2 through 36")
    if number == 0:
        return "0"

    is_negative = number < 0
    number = abs(number)
    remainders: Stack[int] = Stack()
    while number:
        number, remainder = divmod(number, base)
        remainders.push(remainder)

    digits: List[str] = []
    while remainders:
        digits.append(_DIGITS[_pop_required(remainders)])
    converted = "".join(digits)
    return "-" + converted if is_negative else converted


def decimal_to_binary(number: int) -> str:
    return decimal_to_base(number, 2)


def decimal_to_octal(number: int) -> str:
    return decimal_to_base(number, 8)


def decimal_to_hexadecimal(number: int) -> str:
    return decimal_to_base(number, 16)


def reverse_string(text: str) -> str:
    """Return text in reverse order by pushing and popping its characters."""
    characters: Stack[str] = Stack()
    for character in text:
        characters.push(character)
    reversed_characters: List[str] = []
    while characters:
        reversed_characters.append(_pop_required(characters))
    return "".join(reversed_characters)


def has_balanced_delimiters(text: str) -> bool:
    """Check that (), [], and {} are correctly matched and nested."""
    opening_for = {")": "(", "]": "[", "}": "{"}
    openers = set(opening_for.values())
    delimiters: Stack[str] = Stack()

    for character in text:
        if character in openers:
            delimiters.push(character)
        elif character in opening_for:
            if delimiters.pop() != opening_for[character]:
                return False
    return delimiters.is_empty()


def _tokenize(expression: str) -> List[str]:
    expression = expression.strip()
    if not expression:
        raise ValueError("expression cannot be empty")

    tokens: List[str] = []
    position = 0
    while position < len(expression):
        match = _TOKEN_RE.match(expression, position)
        if match is None:
            raise ValueError("invalid character at position {}".format(position))
        if match.group(1) is not None:
            tokens.append(match.group(1) + (match.group(2) or ""))
        else:
            token = match.group(3) or match.group(4)
            if token is None:
                raise RuntimeError("token pattern matched without a token")
            tokens.append(token)
        position = match.end()
    return tokens


def infix_to_postfix(expression: str) -> str:
    """Convert an arithmetic infix expression to space-separated postfix."""
    output: List[str] = []
    operators: Stack[str] = Stack()
    expect_operand = True

    for token in _tokenize(expression):
        if token[0].isdigit() or token[0] == "." or token[0].isalpha() or token[0] == "_":
            if not expect_operand:
                raise ValueError("missing operator before {!r}".format(token))
            output.append(token)
            expect_operand = False
        elif token == "(":
            if not expect_operand:
                raise ValueError("missing operator before '('")
            operators.push(token)
        elif token == ")":
            if expect_operand:
                raise ValueError("missing operand before ')'")
            while operators and operators.peek() != "(":
                output.append(_pop_required(operators))
            if operators.is_empty():
                raise ValueError("unmatched closing parenthesis")
            _pop_required(operators)
            expect_operand = False
        elif token in _PRECEDENCE:
            if expect_operand:
                if token not in {"+", "-"}:
                    raise ValueError("operator {!r} has no left operand".format(token))
                token = "u" + token
                operators.push(token)
                continue

            while operators:
                top_operator = operators.peek()
                if top_operator not in _PRECEDENCE:
                    break
                should_pop = (
                    _PRECEDENCE[top_operator] > _PRECEDENCE[token]
                    or (
                        _PRECEDENCE[top_operator] == _PRECEDENCE[token]
                        and token not in _RIGHT_ASSOCIATIVE
                    )
                )
                if not should_pop:
                    break
                output.append(_pop_required(operators))
            operators.push(token)
            expect_operand = True

    if expect_operand:
        raise ValueError("expression cannot end with an operator")

    while operators:
        operator = _pop_required(operators)
        if operator == "(":
            raise ValueError("unmatched opening parenthesis")
        output.append(operator)

    return " ".join(output)


def evaluate_postfix(
    expression: str, variables: Optional[Mapping[str, float]] = None
) -> float:
    """Evaluate a postfix expression without using Python's eval()."""
    values: Stack[float] = Stack()
    variable_values = variables or {}
    operators = {"+", "-", "*", "/", "//", "%", "**", "u+", "u-"}

    for token in expression.split():
        if token in operators:
            if token in {"u+", "u-"}:
                if len(values) < 1:
                    raise ValueError("unary operator {!r} has no operand".format(token))
                operand = _pop_required(values)
                values.push(operand if token == "u+" else -operand)
                continue

            if len(values) < 2:
                raise ValueError("operator {!r} has too few operands".format(token))
            right = _pop_required(values)
            left = _pop_required(values)
            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            elif token == "/":
                result = left / right
            elif token == "//":
                result = left // right
            elif token == "%":
                result = left % right
            else:
                result = left ** right
            values.push(result)
        elif token in variable_values:
            values.push(float(variable_values[token]))
        else:
            try:
                values.push(float(token))
            except ValueError:
                raise ValueError("unknown variable or invalid operand {!r}".format(token))

    if len(values) != 1:
        raise ValueError("postfix expression must leave exactly one result")
    return _pop_required(values)


def evaluate_infix(
    expression: str, variables: Optional[Mapping[str, float]] = None
) -> float:
    """Convert an infix expression to postfix and evaluate the result."""
    return evaluate_postfix(infix_to_postfix(expression), variables)


def depth_first_search(graph: Mapping[T, Iterable[T]], start: T) -> List[T]:
    """Visit a graph iteratively, using a stack instead of recursive calls."""
    pending: Stack[T] = Stack()
    pending.push(start)
    visited = set()
    order: List[T] = []

    while pending:
        current = _pop_required(pending)
        if current in visited:
            continue
        visited.add(current)
        order.append(current)
        for neighbor in reversed(list(graph.get(current, ()))):
            if neighbor not in visited:
                pending.push(neighbor)
    return order


if __name__ == "__main__":
    stack = Stack[int]()
    stack.print_stack()
    for value in (10, 20, 30):
        stack.push(value)
    stack.print_stack()
    print("Top element:", stack.peek())
    print("Popped:", stack.pop())
    print("Popped:", stack.pop())
    stack.print_stack()
    print("Popped:", stack.pop())
    print("Popped from empty stack:", stack.pop())
    print("Peek on empty stack:", stack.peek())

    print("\nStack applications:")
    print("Decimal 42 in binary:", decimal_to_binary(42))
    print("Decimal 42 in octal:", decimal_to_octal(42))
    print("Decimal 42 in hexadecimal:", decimal_to_hexadecimal(42))
    print("Reverse of 'STACK':", reverse_string("STACK"))
    print("Balanced delimiters:", has_balanced_delimiters("{[()]}"))

    expression = "(12 + 3) * 2 ** 2"
    postfix = infix_to_postfix(expression)
    print("Infix:", expression)
    print("Postfix:", postfix)
    print("Evaluated result:", evaluate_postfix(postfix))

    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
        "D": [],
        "E": [],
    }
    print("Depth-first search:", depth_first_search(graph, "A"))
