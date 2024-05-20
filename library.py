from user import User
from book import Book
from movie import Movie

class Library:

    MAX_HOLDS = 10

    def __init__(self):
        self.__users = {}
        self.__collection = {}

    def __getitem__(self, key):
        if key == "users":
            return self.__users
        if key == "collection":
            return self.__collection
        if key == "books":
            return {k:v for k,v in self.__collection.items() if type(v) == Book}

    def generate_user_id(self, name, birth_year):
        user_id = (name[0] + name.split()[-1][:3]).casefold() + str(birth_year)
        if user_id not in self.__users:
            return user_id
        user_id += "-"
        j = 1
        while user_id+str(j) in self.__users:
            j += 1
        return user_id+str(j)
    
    def generate_media_id(self, title, name, year):
        media_id = "".join(w[0] for w in title.split() + name.split()).casefold() + str(year)
        if media_id not in self.__collection:
            return media_id
        media_id += "-"
        j = 1
        while media_id+str(j) in self.__collection:
            j += 1
        return media_id+str(j)

    def add_user(self, **kwargs):
        user_id = self.generate_user_id(kwargs["name"], kwargs["birth_year"])
        self.__users[user_id] = User(user_id, **kwargs)

    def add_book(self, **kwargs):
        book_id = self.generate_media_id(kwargs["title"], kwargs["author"], kwargs["pub_year"])
        self.__collection[book_id] = Book(book_id, **kwargs)

    def add_movie(self, **kwargs):
        movie_id = self.generate_media_id(kwargs["title"], kwargs["director"], kwargs["rel_year"])
        self.__collection[movie_id] = Movie(movie_id, **kwargs)

    def in_collection(self, media_id):
        return media_id in self.__collection
    
    def in_users(self, user_id):
        return user_id in self.__users

    def checkout(self, user_id, media_id):
        if user_id not in self.__users:
            return "no user"
        elif media_id not in self.__collection:
            return "no media"
        elif self.__users[user_id].total_held() >= self.MAX_HOLDS:
            return "max"
        elif user_id == self.__collection[media_id]["current_user_id"]:
            return "dup"
        elif not self.__collection[media_id].is_available(user_id):
            return "out"
        self.__users[user_id].checkout(media_id)
        self.__collection[media_id].checkout(user_id)
        return "success"
    
    def checkin(self, user_id, media_id):
        if user_id not in self.__users:
            return "no user"
        elif media_id not in self.__collection:
            return "no media"
        if user_id != self.__collection[media_id]["current_user_id"]:
            return "not checked"
        self.__users[user_id].checkin(media_id)
        self.__collection[media_id].checkin()
        return "success"

    def place_hold(self, user_id, media_id):
        if user_id not in self.__users:
            return "no user"
        elif media_id not in self.__collection:
            return "no media"
        elif user_id in self.__collection[media_id]["holds"]:
            return "dup"
        self.__users[user_id].place_hold(media_id)
        self.__collection[media_id].place_hold(user_id)
        return "success"
    
    def drop_hold(self, user_id, media_id):
        if user_id not in self.__users:
            return "no user"
        elif media_id not in self.__collection:
            return "no media"
        elif media_id not in self.__users[user_id]["holds"]:
            return "no hold"
        self.__users[user_id].drop_hold(media_id)
        self.__collection[media_id].drop_hold(user_id)
        return "success"
    
    def media_key_desc(self, media_id):
        if isinstance(self.__collection[media_id], Book):
            return Book.key_desc()
        elif isinstance(self.__collection[media_id], Movie):
            return Movie.key_desc()
        
    def book_key_desc(self):
        return Book.key_desc()
    
    def movie_key_desc(self):
        return Movie.key_desc()
        
    def user_key_desc(self):
        return User.key_desc()
    
    def save_collection(self, file_name = "collection_data.txt"):
        with open(file_name, "w") as file:
            for media in self.__collection.values():
                file.write(repr(media)+"\n")

    def load_collection(self, file_name = "collection_data.txt"):
        with open(file_name, "r") as file:
            for line in file:
                kwargs = eval(line)
                if "book_id" in kwargs:
                    self.__collection[kwargs["book_id"]] = Book(**kwargs)
                if "movie_id" in kwargs:
                    self.__collection[kwargs["movie_id"]] = Movie(**kwargs)

    def save_users(self, file_name = "user_data.txt"):
        with open(file_name, "w") as file:
            for user in self.__users.values():
                file.write(repr(user)+"\n")

    def load_users(self, file_name = "user_data.txt"):
        with open(file_name, "r") as file:
            for line in file:
                kwargs = eval(line)
                self.__users[kwargs["user_id"]] = User(**kwargs)