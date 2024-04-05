import random
from Neo4jConnection import Neo4jConnection

conn = Neo4jConnection()

def randomInt():
    return random.randint(1, 5)

def randomIntMovieYear():
    return random.randint(1995, 2020)

def create_user_node(name, userId):
    conn.query(f"MERGE (u:User {{name:'{name}', userId:{userId}}})")

def create_movie_node(title, tmdbld, relesed, imbdRating, movieId, year, plot):
    conn.query(f"MERGE (m:Movie {{title:'{title}', movieId:{movieId}, year:{year}, plot:'{plot}'}})")

def create_rated_relation(userId, movieId, rating, timestamp):
    conn.query(f"MATCH (u:User {{userId:{userId}}}), (m:Movie {{movieId:{movieId}}}) MERGE (u)-[r:RATED {{rating:{rating}, timestamp: {timestamp}}}]->(m)")

def main():
    ids = [1, 2, 3, 4, 5]
    names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    for num in ids:
        create_user_node(names[num-1], num)

    create_movie_node("The Shawshank Redemption", 1, 1999, "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.")
    create_movie_node("The Matrix", 2, 1999, "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.")
    create_movie_node("The Godfather", 3, 1999, "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.")
    create_movie_node("The Dark Knight", 4, 1999, "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.")
    create_movie_node("Pulp Fiction", 5, 1999, "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.")

    for num in ids:
        create_rated_relation(num, randomInt(), randomInt(), randomIntMovieYear())
        create_rated_relation(num, randomInt(), randomInt(), randomIntMovieYear())

if __name__ == '__main__':
    main()
