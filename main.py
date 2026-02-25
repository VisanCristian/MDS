from commands import cmd_add, cmd_list, cmd_done, cmd_delete, cmd_show, cmd_edit, cmd_help

COMMANDS = {
    "add": lambda args: cmd_add(),
    "list": lambda args: cmd_list(args),
    "done": lambda args: cmd_done(args),
    "delete": lambda args: cmd_delete(args),
    "show": lambda args: cmd_show(args),
    "edit": lambda args: cmd_edit(args),
    "help": lambda args: cmd_help(),
}


def main():
    print("TODO List CLI - Scrie 'help' pentru comenzi disponibile.")

    while True:
        try:
            user_input = input("todo> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nLa revedere!")
            break

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in ("exit", "quit"):
            print("La revedere!")
            break

        handler = COMMANDS.get(command)
        if handler:
            try:
                handler(args)
            except Exception as e:
                print(f"  Eroare neasteptata: {e}")
        else:
            print(f"  Comanda '{command}' nu exista. Scrie 'help' pentru lista de comenzi.")


if __name__ == "__main__":
    main()
