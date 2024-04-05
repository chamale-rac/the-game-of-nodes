from datetime import datetime
import random
from Neo4jConnection import Neo4jConnection

conn = Neo4jConnection()

def randomInt():
    return random.randint(1, 5)

def randomIntMovieYear():
    return random.randint(1995, 2020)

def is_date(string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(string, date_format)
        return True
    except ValueError:
        return False
    
def getFields(fields):
    fields_string = ""
    for num, field in enumerate(fields):
        if type(field[1]) == str:
            if is_date(field[1]):
                fields_string += f"{field[0]}: date('{field[1]}')"
            else:
                fields_string += f"{field[0]}: '{field[1]}'"
        elif type(field[1]) == int or type(field[1]) == float or type(field[1]) == bool or type(field[1]) == list or type(field[1]) == dict:
            fields_string += f"{field[0]}: {field[1]}"
        
        if num != len(fields) - 1:
            fields_string += ", "
    
    return fields_string

def getTypes(types):
    types_string = ""
    for num, type in enumerate(types):
        types_string += f"{type}"
        if num != len(types) - 1:
            types_string += ":"
    
    return types_string

def create_node(type, fields):
    string_fields = getFields(fields)
    string_types = getTypes(type)
    conn.query(f"MERGE (n:{string_types} {{{string_fields}}})")

def create_relation(node1, value1, node2, value2, relation, fields):
    string_fields = getFields(fields)
    if fields != []:
        conn.query(f"MATCH (n1:{node1} {{{value1[0]}:{value1[1]}}}), (n2:{node2} {{{value2[0]}:{value2[1]}}}) MERGE (n1)-[r:{relation} {{{string_fields}}}]->(n2)")
    else:
        conn.query(f"MATCH (n1:{node1} {{{value1[0]}:{value1[1]}}}), (n2:{node2} {{{value2[0]}:{value2[1]}}}) MERGE (n1)-[r:{relation}]->(n2)")


def main():
    ids = [1, 2, 3, 4, 5]
    names = ["Alice", "Bob", "Charlie", "David", "Eve"]

    movies = ["The Shawshank Redemption", "The Matrix", "The Godfather", "The Dark Knight", "Pulp Fiction"]
    movies_description = ["Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."]
    
    for num in ids:
        create_node(["User"], [("name", names[num - 1]), ("userId", num)])

    for num in ids:
        create_node(["Movie"], [("title", movies[num - 1]), ("movieId", num), ("year", randomIntMovieYear()), ("plot", movies_description[num - 1])])

    for num in ids:
        number1 = randomInt()
        number2 = randomInt()
        if number1 == number2: number2 = randomInt()

        create_relation("User", ("userId", num), "Movie", ("movieId", randomInt()), "Rated", [("rating", randomInt()), ("timestamp", randomIntMovieYear())])
        create_relation("User", ("userId", num), "Movie", ("movieId", randomInt()), "Rated", [("rating", randomInt()), ("timestamp", randomIntMovieYear())])

if __name__ == '__main__':
    main()
