price: int = 5
title: str

def some_function(x: str, y: int) -> str:    
	return f'x = {x}, y = {y}'

def test_FunctionName(args):
    pass
    
print(some_function('test', 1))