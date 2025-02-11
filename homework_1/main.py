from typing import Union

import uvicorn
from fastapi import FastAPI, Query, HTTPException

app = FastAPI()


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_operation(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        return a / b


def evaluate_expression(expression):
    def evaluate(tokens):
        values = []
        ops = []
        i = 0

        while i < len(tokens):
            if tokens[i] == ' ':
                i += 1
                continue
            if tokens[i].isdigit():
                value = int(tokens[i]) if '.' not in tokens[i] else float(tokens[i])
                values.append(value)
            elif tokens[i] == '(':
                ops.append(tokens[i])
            elif tokens[i] == ')':
                while ops and ops[-1] != '(':
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    values.append(apply_operation(val1, val2, op))
                ops.pop()
            else:
                while (ops and precedence(ops[-1]) >= precedence(tokens[i])):
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    values.append(apply_operation(val1, val2, op))
                ops.append(tokens[i])
            i += 1

        while ops:
            val2 = values.pop()
            val1 = values.pop()
            op = ops.pop()
            values.append(apply_operation(val1, val2, op))

        return values[0]

    # Разделяем строку на токены
    tokens = []
    current_token = ''
    for char in expression:
        if char in '()+-*/':
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ''
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)

    return evaluate(tokens)

@app.get('/')
async def root():
    return {'message': 'Добро пожаловать в наш калькулятор!'}


@app.get('/add/')
async def add(first_value: Union[int, float], second_value: Union[int, float]):
    return {'result': first_value + second_value}


@app.get('/subtract')
async def subtract(first_value: Union[int, float], second_value: Union[int, float]):
    return {'result': first_value - second_value}


@app.get('/multiply')
async def multiply(first_value: Union[int, float], second_value: Union[int, float]):
    return {'result': first_value * second_value}


@app.get('/divide')
async def divide(first_value: Union[int, float], second_value: Union[int, float] = Query(gt=0)):
    return {'result': first_value / second_value}


@app.get('/calculate_expression')
async def calculate_expression(expression: str):
    return {'result': evaluate_expression(expression)}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
    )

