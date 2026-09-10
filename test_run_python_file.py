from functions.run_python_file import run_python_file


def test() -> None:
    result1 = run_python_file("calculator", "main.py")
    print('run_python_file("calculator", "main.py")')
    print("-------")
    print(result1)
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print('run_python_file("calculator", "main.py")')
    print("-------")
    print(result2)
    result3 = run_python_file("calculator", "tests.py")
    print('run_python_file("calculator", "tests.py")')
    print("-------")
    print(result3)
    result4 = run_python_file("calculator", "../main.py")
    print('run_python_file("calculator", "../main.py")')
    print("-------")
    print(result4)
    result5 = run_python_file("calculator", "nonexistent.py")
    print('run_python_file("calculator", "nonexistent.py")')
    print("-------")
    print(result5)
    result6 = run_python_file("calculator", "lorem.txt")
    print('run_python_file("calculator", "lorem.txt")')
    print("-------")
    print(result6)


if __name__ == "__main__":
    test()
