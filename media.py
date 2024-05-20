class Media:
    
    def __init__(self, title, current_user_id, due_date, holds):
        self.__title = title
        self.__current_user_id = current_user_id
        self.__due_date = due_date
        self.__holds = holds

    def __getitem__(self, key):
        if key == "title":
            return self.__title
        elif key == "current_user_id":
            return self.__current_user_id
        elif key == "due_date":
            return self.__due_date
        elif key == "holds":
            return self.__holds
        
    def __setitem__(self, key, value):
        if key == "title":
            self.__title = value
        elif key == "current_user_id":
            self.__current_user_id = value
        elif key == "due_date":
            self.__due_date = value
    
    def is_available(self, user_id):
        if self.__current_user_id:
            return False
        elif not self.__holds:
            return True
        elif user_id == self.__holds[0]:
            return True
        else:
            return False
        
    def checkout(self, user_id):
        self.__current_user_id = user_id
        if user_id in self.__holds:
            self.__holds.remove(user_id)

    def checkin(self):
        self.__current_user_id = None

    def place_hold(self, user_id):
        self.__holds.append(user_id)

    def drop_hold(self, user_id):
        self.__holds.remove(user_id)