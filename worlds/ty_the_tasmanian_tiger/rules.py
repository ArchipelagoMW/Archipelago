from typing import Callable
import re

from worlds.ty_the_tasmanian_tiger.options import Ty1Options

# Tokenizing the expression
def tokenize(expression):
    # Tokenize based on parentheses, operators, and conditions (multi-word names and quantities)
    return re.findall(r'\(|\)|[\w\'-]+(?: [\w\'-]+)*(?:,\d+)?|[|&]', expression)

# Parsing the tokenized expression into a logical tree structure
def parse_tokens(tokens):
    def parse_expression(tokens, start=0):
        # Recursive function to parse AND/OR logic with parentheses
        result = []
        i = start
        while i < len(tokens):
            token = tokens[i]

            if token == '(':
                sub_expr, i = parse_expression(tokens, i + 1)  # Parse subexpression within parentheses
                result.append(sub_expr)
            elif token == ')':
                return result, i + 1  # Return the parsed result and the index after the closing parenthesis
            elif token in ('&', '|'):
                result.append(token)  # Append logical operators
                i += 1
            else:  # It's a condition (with optional quantity)
                if ',' in token:  # It's a condition with a quantity (e.g., 'Progressive Rang,7')
                    name, count = token.split(',', 1)
                    result.append((name, int(count)))
                else:
                    result.append((token, 1))  # Default count is 1 for conditions without a quantity
                i += 1
        return result, i

    parsed_expr, _ = parse_expression(tokens, 0)
    return parsed_expr

def evaluate_condition(cond, state, player, options):
    """
    Evaluate a single condition (either simple or with a quantity).
    """
    if isinstance(cond, tuple):
        name, count = cond
        # Here, you would evaluate the condition based on `name` and `count`
        # For now, it's just a placeholder for demonstration
        return state.has(name, player, count)
    else:
        return False  # Or raise an error if needed

def parse_logical_conditions(condition_block, state, player, options):
    """
    Recursively evaluate a logical expression (AND/OR).
    """
    if isinstance(condition_block, list):
        # If it's a list, it represents a group of conditions with operators between them
        result = evaluate_condition(condition_block[0], state, player, options)
        operator = None
        for i in range(1, len(condition_block), 2):
            operator = condition_block[i]
            if operator == '&':
                result = result and evaluate_condition(condition_block[i + 1], state, player, options)
            elif operator == '|':
                result = result or evaluate_condition(condition_block[i + 1], state, player, options)
        return result
    else:
        return evaluate_condition(condition_block, state, player, options)

# Final parsing function
def parse_condition_string(cond_str):
    tokens = tokenize(cond_str)
    parsed_expression = parse_tokens(tokens)
    return parsed_expression


def calculate_rule(player: int, options: Ty1Options, req_items) -> Callable:
    """
    Generate a callable rule function based on the logical conditions.
    """
    def rule(state):
        return parse_logical_conditions(req_items, state, player, options)
    return rule
