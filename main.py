from library import Library

def user_menu(library, user_id):
    while True:
        command = input(f"[{user_id}] view, edit, checkout, return, unhold, back>").strip().lower()
       
        if command == "view":
            cmnd = input(f"[{user_id}:View] info, borrowed, holds>")
            if cmnd == "info":
                print(str(library["users"][user_id]))
            elif cmnd == "borrowed":
                for media_id in library["users"][user_id]["borrowed"]:
                    print(str(library["collection"][media_id]))
            elif cmnd == "holds":
                for media_id in library["users"][user_id]["holds"]:
                    print(str(library["collection"][media_id]))
        
        elif command == "edit":
            field = input(f"[{user_id}:Edit] " + ", ".join(key for key in library.user_key_desc()) + ">").strip().lower()
            if field in library.user_key_desc():
                library["users"][user_id][field] = input("Enter new info: ").strip()
            else:
                print("No such field...")
       
        elif command == "checkout":
            media_id = input(f"[{user_id}:Checkout] Media ID>")
            result = library.checkout(user_id, media_id)
            if result == "success":
                print("Checkout successful!")
            elif result == "max":
                print("User is maxed out. Return stuff or drop holds to check more out...")
            elif result == "dup":
                print("User already has item checked out...")
            elif result == "out":
                cmd = input("Item unavailable. Place hold (y/n)? ")
                if cmd and cmd[0] == "y":
                    rslt = library.place_hold(user_id, media_id)
                    if rslt == "success":
                        print("Hold successfully placed!")
                    elif rslt == "dup":
                        print("Hold already placed...")
            elif result == "no media":
                print("Media unfound...")
        
        elif command == "return":
            media_id = input(f"[{user_id}:Return] Media ID>")
            result = library.checkin(user_id, media_id)
            if result == "success":
                print("Return successful!")
            elif result == "no media":
                print("Media unfound...")
            elif result == "not checked":
                print("User is not currently borrowing this item...")
        
        elif command == "unhold":
            media_id = input(f"[{user_id}:Drop Hold] Media ID>")
            result = library.drop_hold(user_id, media_id)
            if result == "success":
                print("Hold drop successful!")
            elif result == "no media":
                print("Media unfound...")
            elif result == "no hold":
                print("User has no hold this item...")
       
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def users_menu(library):
    while True:
        command = input("[Users] add, view, select, back>").strip().lower()
       
        if command == "add":
            kwargs = {key: input(f"{desc}: ").strip() for key,desc in library.user_key_desc().items()}
            library.add_user(**kwargs)
       
        elif command == "view":
            for user in library["users"].values():
                print(str(user))
        
        elif command == "select":
            user_id = input("[Users] User ID>").strip().lower()
            if library.in_users(user_id):
                user_menu(library, user_id)
            else:
                print("User unfound...")
       
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def media_menu(library, media_id):
    while True:
        command = input(f"[{media_id}] view, edit, checkout, return, unhold, back>").strip().lower()
        
        if command == "view":
            print(str(library["collection"][media_id]))
        
        elif command == "edit":
            field = input(f"[{media_id}:Edit] " + ", ".join(key for key in library.media_key_desc(media_id)) + ">").strip().lower()
            if field in library.media_key_desc(media_id):
                library["collection"][media_id][field] = input("Enter new info: ").strip()
            else:
                print("No such field...")
        
        elif command == "checkout":
            user_id = input(f"[{media_id}:Checkout] User ID>")
            result = library.checkout(user_id, media_id)
            if result == "success":
                print("Checkout successful!")
            elif result == "max":
                print("User is maxed out. Return stuff or drop holds to check more out...")
            elif result == "dup":
                print("User already has item checked out...")
            elif result == "out":
                cmd = input("Item unavailable. Place hold (y/n)? ")
                if cmd and cmd[0] == "y":
                    rslt = library.place_hold(user_id, media_id)
                    if rslt == "success":
                        print("Hold successfully placed!")
                    elif rslt == "dup":
                        print("Hold already placed...")
            elif result == "no user":
                print("User unfound...")
        
        elif command == "return":
            user_id = library["collection"][media_id]["current_user_id"]
            if user_id:
                library.checkin(user_id, media_id)
            else:
                print("Item is not checked out...")
        
        elif command == "unhold":
            user_id = input(f"[{media_id}:Drop Hold] User ID>")
            result = library.drop_hold(user_id, media_id)
            if result == "success":
                print("Hold drop successful!")
            elif result == "no user":
                print("User unfound...")
            elif result == "no hold":
                print("User has no hold this item...")
        
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def collection_menu(library):
    while True:
        command = input("[Collection] add, view, select, back>").strip().lower()
        
        if command == "add":
            medium = input("[Medium] book, movie>").strip().lower()
            if medium == "book":
                kwargs = {key: input(f"{desc}: ").strip() for key,desc in library.book_key_desc().items()}
                library.add_book(**kwargs)
            elif medium == "movie":
                kwargs = {key: input(f"{desc}: ").strip() for key,desc in library.movie_key_desc().items()}
                library.add_movie(**kwargs)
            else:
                print("Medium unsupported...")
        
        elif command == "view":
            for item in library["collection"].values():
                print(str(item))
        
        elif command == "select":
            media_id = input("[Collection] Media ID>").strip().lower()
            if library.in_collection(media_id):
                media_menu(library, media_id)
            else:
                print("Media unfound...")
        
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def main():
    library = Library()
    try:
        library.load_collection()
    except Exception:
        pass
    try:
        library.load_users()
    except Exception:
        pass

    while True:
        command = input("[Main Menu] users, collection, quit>").strip().lower()
        
        if command == "users":
            users_menu(library)
        
        elif command == "collection":
            collection_menu(library)
        
        elif command == "quit":
            break
        
        else:
            print("Command unrecognized...")

    library.save_collection()
    library.save_users()

main()