
# get input from user
def get_new_project(args):
    code = args.code
    title = args.title
    project = {
        "code": code,
        "title": title,
        "goal": int(args.goal) if args.goal else 0,
    }
    if args.series:
        project["series"] = args.series

    return project

# create new project directory
