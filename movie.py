from media import Media

KEY_DESC = {
            "title": "Title",
            "director": "Director",
            "rel_year": "Release Year"
        }

class Movie(Media):

    def __init__(self, movie_id, title, director, rel_year, current_user_id = None, due_date = None, holds = []):
        super().__init__(title, current_user_id, due_date, holds)
        self.__movie_id = movie_id
        self.__director = director
        self.__rel_year = rel_year

    def __getitem__(self, key):
        if key == "movie_id":
            return self.__movie_id
        elif key == "director":
            return self.__director
        elif key == "rel_year":
            return self.__rel_year
        else:
            return super().__getitem__(key)
        
    def __setitem__(self, key, value):
        if key == "director":
            self.__director = value
        elif key == "rel_year":
            self.__rel_year = value
        else:
            return super().__setitem__(key, value)
        
    def __str__(self):
        return "-- " + self.__movie_id + " --" + "".join("\n\t" + desc + ": " + str(self[key]) for key, desc in KEY_DESC.items())

    def __repr__(self):
        return str({key : self[key] for key in self.__init__.__code__.co_varnames[1:]})
    
    def key_desc():
        return KEY_DESC