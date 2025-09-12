import sys
from pathlib import Path
from rich import print
from db_manager import add_faq, list_faqs, import_from_json, init_db
from chatbot import Chatbot

def print_help():
    print("[bold cyan]Commands:[/bold cyan]")
    print("/help      - show help")
    print("/listfaqs  - list all FAQs")
    print("/addfaq    - add a new FAQ")
    print("/import    - import FAQs from data/faqs.json")
    print("/reload    - reload DB")
    print("/quit      - exit")

def interactive_add():
    q = input("Question: ").strip()
    if not q: return
    a = input("Answer: ").strip()
    tags = input("Tags: ").strip()
    add_faq(q, a, tags)
    print("[green]FAQ saved.[/green]")

def list_all():
    rows = list_faqs()
    if not rows:
        print("[yellow]No FAQs yet.[/yellow]")
    for r in rows:
        print(f"[blue]{r['id']}[/blue] {r['question']}\n   -> {r['answer']}")

def main():
    init_db()
    bot = Chatbot()
    print("[bold magenta]University Chatbot[/bold magenta] (type /help)")
    while True:
        try:
            text = input("You> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!"); break
        if text.startswith('/'):
            if text in ('/quit','/exit'): break
            if text == '/help': print_help(); continue
            if text == '/listfaqs': list_all(); continue
            if text == '/addfaq': interactive_add(); bot.refresh(); continue
            if text.startswith('/import'):
                path = Path("data/faqs.json")
                if not path.exists():
                    print("[red]data/faqs.json not found[/red]")
                    continue
                count = import_from_json(str(path))
                bot.refresh()
                print(f"[green]Imported {count} FAQs[/green]")
                continue
            if text == '/reload': bot.refresh(); print("Reloaded."); continue
            print("Unknown command.")
        else:
            print(f"[italic]{bot.respond(text)}[/italic]\n")

if __name__ == "__main__":
    main()