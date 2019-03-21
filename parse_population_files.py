import csv


def parseUsers(filename):
    if type(filename) != str:
        raise ValueError("Input must be a string")

    users = {}

    try:
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                user = row.pop("username")
                users[user] = row
                line_count += 1
            print(f' {line_count} lines.')
    except:
        raise TypeError("%s must be a csv file" % filename)

    return users


def parsePosts(filename):
    if type(filename) != str:
        raise ValueError("Input must be a string")

    posts = {}

    try:
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                user = row.pop("user")
                posts[user] = posts.get(user, [])
                posts[user].append(row)
                line_count += 1
            print(f' {line_count} lines.')
    except:
        raise TypeError("%s must be a csv file" % filename)
    return posts


def parseCatrgories(filename):
    """returns a list of tuples where each tuple stores the name and filename of the category"""
    if type(filename) != str:
        raise ValueError("Input must be a string")

    categories = []

    try:
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                categories.append(tuple(row.values()))
                line_count += 1
            print(f' {line_count} lines.')
    except:
        raise TypeError("%s must be a csv file" % filename)
    return categories


def parseComments(filename):
    """returns a list of comments"""
    if type(filename) != str:
        raise ValueError("Input must be a string")

    comments = []

    try:
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                comments.append(tuple(row.values())[0])
                line_count += 1
            print(f' {line_count} lines.')
    except:
        raise TypeError("%s must be a csv file" % filename)
    return comments
