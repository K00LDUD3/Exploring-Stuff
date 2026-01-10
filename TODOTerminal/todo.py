from pathlib import Path
import os
import pickle
from tabulate import tabulate
import argparse

app_dir = Path(os.getenv("LOCALAPPDATA")) / "SimpleTodo"
app_dir.mkdir(parents=True, exist_ok=True)
data_file = app_dir / "tasks.pkl"

MONTHLY = "Drift"#"Monthly"
WEEKLY = "Spiral" #"Weekly"
ASAP = "Tempest" #"ASAP"
ALL = "all"
PRIORITIES = [MONTHLY, WEEKLY, ASAP, ALL]

starter = {
    MONTHLY : [],
    WEEKLY : [],
    ASAP : []
}
"""
- Comes in 3 priorities: long term, short term, urgent 
- Format: 
    Keys: priority label
    Vals: list of tasks
    Task List: Each element is a Dictionary - {
        TASK - str,
        Done - bool,
            }
"""

def ReadFile(data_file : os.path) -> dict:
    t = {}
    with open(data_file, "rb") as f:
        t = pickle.load(f);
    return t

def WipeFile(data_file : os.path, replacement : dict):
    with open(data_file,"wb") as f:
        pickle.dump(replacement, f)

def PrintTasks(priority : str, tasks : list):
    print("\n")
    separ = '-'*len(priority)
    print(separ,priority,separ)
    print(tabulate(tasks, headers="keys", tablefmt="grid"))

def PrintF(data_file : os.path, option: str = ALL, show_done : bool = True):
    if option not in PRIORITIES:
        print(f"Enter a valid option ({ALL} / {MONTHLY} / {WEEKLY} / {ASAP})")
        return -1

    t = ReadFile(data_file)
    if option == ALL:
        for key,value in t.items():
            if len(value) > 0:
                PrintTasks(key, value)
            else:
                print(f"{key} list is empty")
    elif option in PRIORITIES:
        if len(t[option]) > 0:
            PrintTasks(option, t[option])
        else: 
            print(f"{option} todo list is empty")

def AddTask(data_file : os.path, task : str, priority : str):
    if priority in PRIORITIES and priority != ALL:
        tasks = ReadFile(data_file)
        t = tasks[priority]

        # print("before")
        # PrintF(data_file, priority)
        
        new_task_formatted = {
            "No." : len(t)+1,
            "Task" : task,
            "Done" : False
        }

        tasks[priority].append(new_task_formatted)
        # print(tasks)
        # print(t)
        # print("after:")
        WipeFile(data_file, tasks)
        PrintF(data_file, priority)
    else: 
        print(f"Enter a valid priority ({MONTHLY} / {WEEKLY} / {ASAP})")
        return -1

# def CompleteTask(data_file, task, category : str, delete = False, search_by = "idname"):
#     search_by_name = True if "name" in search_by.lower() else False
#     search_by_ID = True if 'id' in search_by.lower() else False
#     # print(f"{search_by_ID=}")
#     # print(f"{search_by_name=}")
#     if category in PRIORITIES:
#         tasks_removed = 0
#         raw_file = ReadFile(data_file)
#         if category == ALL:
#             for categ,tasks in raw_file.items():
#                 # print(categ)
#                 for i in range(len(tasks)):
#                     if search_by_name and tasks[i]['Task'] == task or search_by_ID and tasks[i]['No.'] == task:
#                         tasks_removed+=1
#                         if delete:
#                             del raw_file[categ][i]
#                         else:
#                             raw_file[categ][i]['Done'] = True
#         else:
#             tasks = raw_file[category]
#             for i in range(len(tasks)):
#                 if search_by_name and tasks[i]['Task'] == task or search_by_ID and tasks[i]['No.'] == task:
#                     print("hit")
#                     tasks_removed+=1
#                     if delete:
#                         raw_file[category].remove(i)
#                     else:
#                         raw_file[category][i]['Done'] = True
#         WipeFile(data_file, raw_file)
#         PrintF(data_file, category)
#         remove_str = "removed" if delete else "marked"
#         print(f"{tasks_removed} tasks {remove_str}")

#     else:
#         print(f"Enter a valid priority ({MONTHLY} / {WEEKLY} / {ASAP})")
#         return -1

def ClearCategory(data_file : os.path, category : str):
    if category in PRIORITIES and category != ALL:
        raw_file = ReadFile(data_file)
        raw_file[category] = []
        WipeFile(data_file, raw_file)

def FixNumbers(data_file : os.path):
    raw_file = ReadFile(data_file)
    for categ,tasks in raw_file.items():
        for i in range(len(tasks)):
            tasks[i]['No.'] = i+1
    WipeFile(data_file, raw_file)
def CompleteTask(data_file, task, category: str, delete=False, search_by="idname"):
    search_by_name = True if "name" in search_by.lower() else False
    search_by_ID = True if "id" in search_by.lower() else False

    if category in PRIORITIES:
        tasks_removed = 0
        raw_file = ReadFile(data_file)

        if category == ALL:
            for categ, tasks in raw_file.items():
                for i in range(len(tasks) - 1, -1, -1):
                    if (search_by_name and tasks[i]['Task'] == task) or \
                        (search_by_ID and tasks[i]['No.'] == task):
                        tasks_removed += 1
                        if delete:
                            del raw_file[categ][i]
                        else:
                            raw_file[categ][i]['Done'] = True
        else:
            tasks = raw_file[category]
            for i in range(len(tasks) - 1, -1, -1):
                if (search_by_name and tasks[i]['Task'] == task) or \
                    (search_by_ID and tasks[i]['No.'] == task):
                    tasks_removed += 1
                    if delete:
                        del raw_file[category][i]
                    else:
                        raw_file[category][i]['Done'] = True

        WipeFile(data_file, raw_file)
        FixNumbers(data_file)
        PrintF(data_file, category)
        remove_str = "removed" if delete else "marked"
        tasks_str = "tasks" if tasks_removed != 1 else "task"
        print(f"{tasks_removed} {tasks_str} {remove_str}")

    else:
        print(f"Enter a valid priority ({MONTHLY} / {WEEKLY} / {ASAP})")
        return -1


if not data_file.exists():
    print(f"FileNotFound @ {data_file}")
    print(f"Creating new file..")
    WipeFile(data_file, starter)


# WipeFile(data_file, starter)
# print(ReadFile(data_file))
# CompleteTask(data_file, f"{ASAP}_2", ASAP, delete=True)
# CompleteTask(data_file, 2, ASAP, delete=False)
# PrintF(data_file, ALL)
# ClearCategory(data_file, ASAP)
# ClearCategory(data_file, WEEKLY)
# ClearCategory(data_file, MONTHLY)
# PrintF(data_file, ALL)

# for priority in PRIORITIES:
#     if priority == ALL:
#         continue
#     for i in range(5):
#         AddTask(data_file, f"{priority}_{i+1}", priority)

def main():
    parser = argparse.ArgumentParser(prog="todo", description="Simple Todo CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_p = subparsers.add_parser("add", help="Add a task")
    add_p.add_argument("task", type=str)
    add_p.add_argument("-p", "--priority", required=True, choices=[MONTHLY, WEEKLY, ASAP])

    # list
    list_p = subparsers.add_parser("list", help="List tasks")
    list_p.add_argument("-p", "--priority", default=ALL, choices=PRIORITIES)

    # complete
    comp_p = subparsers.add_parser("done", help="Mark task complete")
    comp_p.add_argument("task")
    comp_p.add_argument("-p", "--priority", default=ALL, choices=PRIORITIES)
    comp_p.add_argument("--by", default="id", choices=["id", "name"])

    # delete
    del_p = subparsers.add_parser("del", help="Delete task")
    del_p.add_argument("task")
    del_p.add_argument("-p", "--priority", default=ALL, choices=PRIORITIES)
    del_p.add_argument("--by", default="id", choices=["id", "name"])

    args = parser.parse_args()

    if args.command == "add":
        AddTask(data_file, args.task, args.priority)

    elif args.command == "list":
        PrintF(data_file, args.priority)

    elif args.command == "done":
        CompleteTask(
            data_file,
            int(args.task) if args.by == "id" else args.task,
            args.priority,
            delete=False,
            search_by=args.by
        )

    elif args.command == "del":
        CompleteTask(
            data_file,
            int(args.task) if args.by == "id" else args.task,
            args.priority,
            delete=True,
            search_by=args.by
        )

if __name__ == "__main__":
    if not data_file.exists():
        print(f"FileNotFound @ {data_file}")
        print("Creating new file..")
        WipeFile(data_file, starter)

    main()
