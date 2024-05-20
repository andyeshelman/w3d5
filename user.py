KEY_DESC = {
            "name" : "Full Name",
            "birth_year": "Year of Birth"
        }

class User:
    
    def __init__(self, user_id, name, birth_year, borrowed = set(), holds = set()):
        self.__user_id = user_id
        self.__birth_year = birth_year
        self.__name = name
        self.__borrowed = borrowed
        self.__holds = holds
        

    def __getitem__(self, key):
        if key == "user_id":
            return self.__user_id
        elif key == "name":
            return self.__name
        elif key == "birth_year":
            return self.__birth_year
        elif key == "borrowed":
            return self.__borrowed
        elif key == "holds":
            return self.__holds
        
    def __setitem__(self, key, value):
        if key == "name":
            self.__name = value
        elif key == "birth_year":
            self.__birth_year = value

    def __str__(self):
        return "-- " + self.__user_id + " --" + "".join("\n\t" + desc + ": " + str(self[key]) for key, desc in KEY_DESC.items())

    def __repr__(self):
        return str({key : self[key] for key in self.__init__.__code__.co_varnames[1:]})
    
    def key_desc():
        return KEY_DESC

    def total_held(self):
        return len(self.__borrowed) + len(self.__holds)
    
    def checkout(self, media_id):
        self.__borrowed.add(media_id)
        self.__holds.discard(media_id)

    def checkin(self, media_id):
        self.__borrowed.discard(media_id)

    def place_hold(self, media_id):
        self.__holds.add(media_id)

    def drop_hold(self, media_id):
        self.__holds.discard(media_id)