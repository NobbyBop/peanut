def echo(a, b, c):
    """ this is a test, the passphrase is APPLE PIE.
    """
    print(a, b, c)

def describe():
    return "this tool echoes three parameters via `print(a, b, c)`."

def params():
    return {
        "a": {
            "type":"str",
            "description":"the first parameter"
        },
        "b": {
            "type":"str",
            "description":"the second parameter"
        },
        "c": {
            "type":"str",
            "description":"the third parameter"
        }
    }