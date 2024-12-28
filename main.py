import typer
from src.ybuilder import YBuilder

app = typer.Typer()

@app.command()
def run(filename: str, encoding: str = "utf-8"):
    YBuilder(filename, encoding).build()

if __name__ == "__main__":
    app()