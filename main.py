from datetime import datetime
import random
from Neo4jConnection import Neo4jConnection

conn = Neo4jConnection()

paises = ["Japan","Australia","Canada","Mexico","Brazil","France","Italy","Germany","India","China","Thailand","Egypt","Kenya","Peru","Greece","Spain","Morocco","South Africa","Nigeria","Indonesia","Argentina","Vietnam"]

def randomInt():
    return random.randint(1, 5)

def randomDecimal():
    return random.uniform(0, 10)

def randomIntMovieYear():
    return random.randint(1995, 2020)

def randomListCountry():
    countries = []
    countries.append(paises[random.randint(0, len(paises) - 1)])
    countries.append(paises[random.randint(0, len(paises) - 1)])
    countries.append(paises[random.randint(0, len(paises) - 1)])
    return countries

def randomDate():
    year = random.randint(1900, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month}-{day}"

def randomIntMovieDuration():
    return random.randint(60, 180)

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
    if fields != []:
        string_fields = getFields(fields)
    if fields != []:
        query = f"MATCH (n1:{node1} {{{value1[0]}:{value1[1]}}}), (n2:{node2} {{{value2[0]}:{value2[1]}}}) MERGE (n1)-[r:{relation} {{{string_fields}}}]->(n2)"
        conn.query(query)
        print(query)
    else:
        query = f"MATCH (n1:{node1} {{{value1[0]}:{value1[1]}}}), (n2:{node2} {{{value2[0]}:{value2[1]}}}) MERGE (n1)-[r:{relation}]->(n2)"
        conn.query(query)
        print(query)

def find_relation(node1, value1, node2, value2, relation):
    conn.query(f"MATCH (n1:{node1} {{{value1[0]}:{value1[1]}}}), (n2:{node2} {{{value2[0]}:{value2[1]}}}) MERGE (n1)-[r:{relation}]->(n2)")


def main():
    # ids = [1, 2, 3, 4, 5]
    # names = ["Alice", "Bob", "Charlie", "David", "Eve"]

    # movies = ["The Shawshank Redemption", "The Matrix", "The Godfather", "The Dark Knight", "Pulp Fiction"]
    # movies_description = ["Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."]

    # for num in ids:
    #     create_node(["User"], [("name", names[num - 1]), ("userId", num)])

    # for num in ids:
    #     create_node(["Movie"], [("title", movies[num - 1]), ("movieId", num), ("year", randomIntMovieYear()), ("plot", movies_description[num - 1])])

    # for num in ids:
    #     number1 = randomInt()
    #     number2 = randomInt()
    #     if number1 == number2: number2 = randomInt()

    #     create_relation("User", ("userId", num), "Movie", ("movieId", randomInt()), "Rated", [("rating", randomInt()), ("timestamp", randomIntMovieYear())])
    #     create_relation("User", ("userId", num), "Movie", ("movieId", randomInt()), "Rated", [("rating", randomInt()), ("timestamp", randomIntMovieYear())])

    numId = 1

    create_node(["User"], [("name", "Alice"), ("userId", 1)])

    create_node(["Movie"], [("title", "The Shawshank Redemption"), ("tmdbId", numId), ("released", randomDate()), ("imdbRating", randomDecimal()),  ("movieId", 1), ("year", randomIntMovieYear()), ("imdbId", numId), ("runtime", randomIntMovieDuration()), ("countries", randomListCountry()), ("imdbVotes", randomInt()), ("url", "www.com"), ("plot", "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."), ("poster", "www.com"), ("budget", 1000000), ("languages", ["English", "Spanish"])])

    numId += 1

    create_node(["Person", "Actor", "Director"], [("name", "Tim Robbins"), ("tmdbId", numId), ("born", randomDate()), ("died", randomDate()), ("bornIn", "Los Angeles, United States"), ("url", "www.com"), ("imdbId", numId), ("bio", "Tim Robbins is an American actor, screenwriter, director, producer, and musician."), ("poster", "www.com")])

    create_relation("Actor", ("tmdbId", numId), "Movie", ("movieId", 1), "ACTED_IN", [("role", "Andy Dufresne")])

    create_relation("Director", ("tmdbId", numId), "Movie", ("movieId", 1), "DIRECTED", [("role", "Director")])

    numId += 1
    create_node(["Person", "Actor"], [("name", "Sergie Carlson"), ("tmdbId", numId), ("born", randomDate()), ("died", randomDate()), ("bornIn", "Nebraska, United States"), ("url", "www.com"), ("imdbId", numId), ("bio", "Sergie Carlson is an American actor and narrator."), ("poster", "www.com")])

    create_relation("Actor", ("tmdbId", numId), "Movie", ("movieId", 1), "ACTED_IN", [("role", "Red")])

    numId += 1
    create_node(["Person", "Director"], [("name", "Frank Darabont"), ("tmdbId", numId), ("born", randomDate()), ("died", randomDate()), ("bornIn", "Montbéliard, France"), ("url", "www.com"), ("imdbId", numId), ("bio", "Frank Darabont is a Hungarian-American film director, screenwriter and producer."), ("poster", "www.com")])

    create_relation("Director", ("tmdbId", numId), "Movie", ("movieId", 1), "DIRECTED", [("role", "Director")])

    numId += 1
    create_node(["Genre"], [("name", "Drama")])

    create_relation("Movie", ("movieId", 1), "Genre", ("name", "'Drama'"), "HAS_GENRE", [])

if __name__ == '__main__':
    main()
