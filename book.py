from media import Media

KEY_DESC = {
            "title": "Title",
            "author": "Author",
            "pub_year": "Publication Year"
        }

class Book(Media):

    def __init__(self, book_id, title, author, pub_year, current_user_id = None, due_date = None, holds = []):
        super().__init__(title, current_user_id, due_date, holds)
        self.__book_id = book_id
        self.__author = author
        self.__pub_year = pub_year

    def __getitem__(self, key):
        if key == "book_id":
            return self.__book_id
        elif key == "author":
            return self.__author
        elif key == "pub_year":
            return self.__pub_year
        else:
            return super().__getitem__(key)
        
    def __setitem__(self, key, value):
        if key == "author":
            self.__author = value
        elif key == "pub_year":
            self.__pub_year = value
        else:
            return super().__setitem__(key, value)
        
    def __str__(self):
        return "-- " + self.__book_id + " --" + "".join("\n\t" + desc + ": " + str(self[key]) for key, desc in KEY_DESC.items())

    def __repr__(self):
        return str({key : self[key] for key in self.__init__.__code__.co_varnames[1:]})
    
    def key_desc():
        return KEY_DESC