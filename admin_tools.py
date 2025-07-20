
import json

TEST_FILE = 'tests.json'

def load_tests():
    try:
        with open(TEST_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_tests(tests):
    with open(TEST_FILE, 'w') as f:
        json.dump(tests, f, indent=4)

def add_test(name, answers):
    tests = load_tests()
    tests[name] = answers.upper()
    save_tests(tests)
    return True

def remove_test(name):
    tests = load_tests()
    if name in tests:
        del tests[name]
        save_tests(tests)
        return True
    return False

def list_tests():
    return list(load_tests().keys())
