from datetime import datetime
from models import (
    Task, DATE_FORMAT,
    validate_future_date, validate_priority, validate_time_interval, validate_date,
)
from storage import load_tasks, save_tasks, get_next_id, find_task_by_id


def prompt_field(label: str, validator=None):
    """Cere input de la utilizator, cu validare optionala."""
    while True:
        value = input(f"  {label}: ").strip()
        if not value:
            print("  Campul nu poate fi gol.")
            continue
        if validator:
            try:
                validator(value)
            except ValueError as e:
                print(f"  Eroare: {e}")
                continue
        return value


# --- Comanda ADD ---
def cmd_add():
    print("Creaza o sarcina noua:")
    title = prompt_field("Titlu")
    description = prompt_field("Descriere")
    deadline = prompt_field("Deadline (DD-MM-YYYY HH:MM)", validate_future_date)
    start_time = prompt_field("Ora inceput (DD-MM-YYYY HH:MM)", validate_date)
    end_time = prompt_field("Ora sfarsit (DD-MM-YYYY HH:MM)")

    try:
        validate_time_interval(start_time, end_time)
    except ValueError as e:
        print(f"  Eroare: {e}")
        return

    priority = prompt_field("Prioritate (low/medium/high)", validate_priority)

    tasks = load_tasks()
    new_task = Task(
        id=get_next_id(tasks),
        title=title,
        description=description,
        deadline=deadline,
        start_time=start_time,
        end_time=end_time,
        priority=priority.lower(),
    )
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"  Sarcina #{new_task.id} a fost creata.")


# --- Comanda LIST ---
def cmd_list(args: list[str]):
    tasks = load_tasks()
    if not tasks:
        print("  Nu exista sarcini.")
        return

    # Filtrare pe interval de date
    if args:
        filtered = _filter_tasks_by_args(tasks, args)
        if filtered is None:
            return
        tasks = filtered

    if not tasks:
        print("  Nu exista sarcini in intervalul specificat.")
        return

    for task in tasks:
        print(task)


def _filter_tasks_by_args(tasks: list[Task], args: list[str]) -> list[Task] | None:
    if args[0] == "today":
        today = datetime.now().strftime("%d-%m-%Y")
        return [t for t in tasks if t.start_time.startswith(today) or t.deadline.startswith(today)]

    if args[0] == "done":
        return [t for t in tasks if t.done]

    if args[0] == "pending":
        return [t for t in tasks if not t.done]

    # Interval: list DD-MM-YYYY DD-MM-YYYY
    if len(args) == 2:
        try:
            start = datetime.strptime(args[0], "%d-%m-%Y")
            end = datetime.strptime(args[1], "%d-%m-%Y").replace(hour=23, minute=59)
        except ValueError:
            print("  Format invalid. Foloseste: list DD-MM-YYYY DD-MM-YYYY")
            return None
        if end < start:
            print("  Data de sfarsit trebuie sa fie dupa data de inceput.")
            return None
        return [
            t for t in tasks
            if start <= datetime.strptime(t.start_time, DATE_FORMAT) <= end
            or start <= datetime.strptime(t.deadline, DATE_FORMAT) <= end
        ]

    print("  Argument necunoscut. Foloseste: list / list today / list done / list pending / list DD-MM-YYYY DD-MM-YYYY")
    return None


# --- Comanda DONE ---
def cmd_done(args: list[str]):
    if not args:
        print("  Folosire: done <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("  ID-ul trebuie sa fie un numar.")
        return

    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"  Sarcina #{task_id} nu exista.")
        return

    if task.done:
        print(f"  Sarcina #{task_id} este deja rezolvata.")
        return

    task.done = True
    save_tasks(tasks)
    print(f"  Sarcina #{task_id} a fost marcata ca rezolvata.")


# --- Comanda DELETE ---
def cmd_delete(args: list[str]):
    if not args:
        print("  Folosire: delete <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("  ID-ul trebuie sa fie un numar.")
        return

    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"  Sarcina #{task_id} nu exista.")
        return

    confirm = input(f"  Esti sigur ca vrei sa stergi '{task.title}'? (da/nu): ").strip().lower()
    if confirm != "da":
        print("  Stergere anulata.")
        return

    tasks = [t for t in tasks if t.id != task_id]
    save_tasks(tasks)
    print(f"  Sarcina #{task_id} a fost stearsa.")


# --- Comanda SHOW ---
def cmd_show(args: list[str]):
    if not args:
        print("  Folosire: show <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("  ID-ul trebuie sa fie un numar.")
        return

    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"  Sarcina #{task_id} nu exista.")
        return

    print(task)


# --- Comanda EDIT ---
def cmd_edit(args: list[str]):
    if not args:
        print("  Folosire: edit <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("  ID-ul trebuie sa fie un numar.")
        return

    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"  Sarcina #{task_id} nu exista.")
        return

    print(f"  Editare sarcina #{task_id} (apasa Enter pentru a pastra valoarea curenta):")

    # Titlu
    new_title = input(f"  Titlu [{task.title}]: ").strip()
    if new_title:
        task.title = new_title

    # Descriere
    new_desc = input(f"  Descriere [{task.description}]: ").strip()
    if new_desc:
        task.description = new_desc

    # Deadline
    new_deadline = input(f"  Deadline [{task.deadline}]: ").strip()
    if new_deadline:
        try:
            validate_future_date(new_deadline)
            task.deadline = new_deadline
        except ValueError as e:
            print(f"  Eroare: {e} - deadline pastrat.")

    # Interval orar
    new_start = input(f"  Ora inceput [{task.start_time}]: ").strip()
    new_end = input(f"  Ora sfarsit [{task.end_time}]: ").strip()
    s = new_start if new_start else task.start_time
    e = new_end if new_end else task.end_time
    try:
        validate_time_interval(s, e)
        task.start_time = s
        task.end_time = e
    except ValueError as err:
        print(f"  Eroare: {err} - interval orar pastrat.")

    # Prioritate
    new_prio = input(f"  Prioritate [{task.priority}]: ").strip()
    if new_prio:
        try:
            task.priority = validate_priority(new_prio)
        except ValueError as e:
            print(f"  Eroare: {e} - prioritate pastrata.")

    save_tasks(tasks)
    print(f"  Sarcina #{task_id} a fost actualizata.")


# --- Comanda HELP ---
def cmd_help():
    print("""
  Comenzi disponibile:
    add                          - Creaza o sarcina noua
    list                         - Listeaza toate sarcinile
    list today                   - Sarcinile de azi
    list done                    - Sarcinile rezolvate
    list pending                 - Sarcinile nerezolvate
    list DD-MM-YYYY DD-MM-YYYY   - Sarcinile dintr-un interval
    show <id>                    - Afiseaza detalii sarcina
    done <id>                    - Marcheaza sarcina ca rezolvata
    delete <id>                  - Sterge o sarcina
    edit <id>                    - Editeaza o sarcina
    help                         - Afiseaza acest mesaj
    exit / quit                  - Iesire
""")
