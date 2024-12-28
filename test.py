
from ybuilder import Reader
from ylexer import Lexer

from rich.console import Console


def test_lexer():
    global console

    file = "test/lexer.y"

    console.print("[black]--- TEST LEXER ---")
    console.print(f"Lexer test file: [bold]{file}[/bold]")
    console.print("")

    lexer = Lexer()
    data = Reader().readlines(file, "utf-8")

    expected = [
        ("COMMENT", [typer.YComment("# This is testing lexer file с юникодом #")]),
        ("INTEGER", [typer.YInteger("1")]),
        ("INTEGER UNDERLINE", [typer.YInteger("2_2")]),
        ("INTEGER DASH", [typer.YInteger("3-3")]),
        ("INTEGER UNDERLINE & DASH", [typer.YInteger("4-5_6")]),
        ("IDENTIFIER", [typer.YIdentifier("hello")]),
        ("IDENTIFIER UNICODE", [typer.YIdentifier("юникод")]),
        ("STRING DOUBLE QUOTES", [typer.YString("\"hello world\"")]),
        ("STRING SINGLE QUOTES", [typer.YString("\'hello world\'")]),
        ("STRING UNICODE", [typer.YString("\"юникод\"")]),
        ("UNARY OPERATOR", [typer.YOperator("+"), typer.YInteger("123")]),
        ("BINARY OPERATOR", [typer.YInteger("123"), typer.YOperator(">="), typer.YInteger("456")]),
        ("LIST", [typer.YList("[1, 2, 3]")]),
        ("TUPLE", [typer.YTuple("(1, 2, 3)")]),
        ("SET", [typer.YSet("{1, 2, 3}")]),
        ("DICT", [typer.YDict("{1: 2, 3: 4}")]),
        ("TAB SPACE", [typer.YSpace("    "), typer.YIdentifier("line")]),
        ("TAB TAB", [typer.YSpace("	"), typer.YIdentifier("line")]),
    ]
    actual = [lexer.tokenize(line)[:-1] for line in data]

    name_lenght = max(len(t[0]) for t in expected)
    token_lenght = max(len(str(t)) for t in actual)

    passed = 0

    for i in range(len(expected)):
        try:
            output = f"{expected[i][0]: <{name_lenght}} - {str(expected[i][1])[1:-1]: >{token_lenght}} ? {str(actual[i])[1:-1]: <{token_lenght}}"

            assert actual[i] == expected[i][1]

            passed += 1
        except AssertionError:
            console.print(f"[bold blink red]FAILED: {output}")
        except IndexError:
            console.print("\n[bold blink red]--- TEST FILE IS CORRUPTED ---")

            break
        else:
            console.print(f"[bold green]PASSED: {output}")
    else:
        if passed == len(expected):
            console.print("\n[bold green]--- ALL TESTS PASSED ---")
        else:
            console.print(f"\n[bold red]--- {len(expected) - passed} TESTS FAILED ---")


if __name__ == "__main__":
    console = Console()

    test_lexer()