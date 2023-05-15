# AirBnB_clone

In this project I endeavor to build an AirBnB clone.

The first step is to write classes and a command interpreter to manage my
objects.

## Writing Classes and Command Interpreter

### **Classes**

The classes include:

- `BaseModel` -> Acts as the parent class for all other classes.
- `User`
- `Place`
- `City`
- `State`
- `Amenity`
- `Review`

The `BaseModel` class acts as a parent class taking care of initialization,
serialization and deserialization of future instances.

A file storage engine is also put in place to take care of writing and loading
of objects from a file. The engine provides a `FileStorage` class that contains
methods used in storage operations.

When all the above classes have been implemented correctly, then a simple flow
of serialization/deserialization can be achieved.
i.e Instance <-> Dictionary <-> JSON string <-> file

### **Command Interpreter**

A command interpreter is created to handle the objects of our project.
The command interpreter is implemented in the `console.py` file.
The `cmd` module is used to create the interpreter.

To start the interpreter run `./console.py` in bash at the root
of this project. You have to make sure that console.py is executable.

After starting the interpreter, a `(hbnb)` prompt will be displayed after
which you can enter your command.

```Shell
kim@eternity:~/Dev/ALX/AirBnB_clone$ ./console.py
(hbnb) all
(hbnb) create User
b8465159-2ad8-4d69-8419-1965ffb4b2fc
(hbnb) create City
d225b784-8bb6-4ecd-8462-11c9987c401a
(hbnb) all
["[User] (b8465159-2ad8-4d69-8419-1965ffb4b2fc) {'id': 'b8465159-2ad8-4d69-8419-1965ffb4b2fc', 'created_at': datetime.datetime(2023, 5, 14, 15, 28, 6, 748910), 'updated_at': datetime.datetime(2023, 5, 14, 15, 28, 6, 748959)}", "[City] (d225b784-8bb6-4ecd-8462-11c9987c401a) {'id': 'd225b784-8bb6-4ecd-8462-11c9987c401a', 'created_at': datetime.datetime(2023, 5, 14, 15, 28, 38, 227798), 'updated_at': datetime.datetime(2023, 5, 14, 15, 28, 38, 227830)}"]
(hbnb)
(hbnb) quit
kim@eternity:~/Dev/ALX/AirBnB_clone$
```

The `quit` command can be used to exit the interpreter. You can also enter
`EOF` or press `Ctrl-D` to exit.

Nothing happens when an `empty line + ENTER` is entered as command.

The above snippet is just a few of the operations that can be done by the
command interpreter. You can find the above and more operations explained
in detail below.

1. **Create new object**

A new object of any class implemented can be created through the interpreter.
The id of the object is printed after the object creation and object is added
to the `FileStorage.__objects` so that it can be saved.

Syntax:

- `create <class name>`

If the class name is missing or an invalid class is given an error message is
printed as shown below.

```Text
(hbnb) create User
a5999506-a045-42ac-919f-e9224183a527
(hbnb)
(hbnb) create
** class name missing **
(hbnb)
(hbnb) create ClassNotFound
** class doesn't exist **
(hbnb)
(hbnb) create BaseModel
7f267122-09d8-4aa6-bd65-5b8df8d33f9d
(hbnb)
```

2. **Show an object**

An object's string representation can be printed by calling the `show` command on
that object. The show command takes the objects class and id so as to
reconstruct its key in `FileStorage.__objects` and obtain the correspondng
object to be printed.

It has two syntaxes:

- `show <class name> <id>`
- `<class name>.show(<id>)`

If the class name is missing or an invalid class or invalid id is given, an
error message is printed as show below.

```Text
(hbnb) show User a5999506-a045-42ac-919f-e9224183a527   # object created previously.
[User] (a5999506-a045-42ac-919f-e9224183a527) {'id': 'a5999506-a045-42ac-919f-e9224183a527', 'created_at': datetime.datetime(2023, 5, 14, 13, 18, 25, 272448), 'updated_at': datetime.datetime(2023, 5, 14, 13, 18, 25, 272491)}
(hbnb)
(hbnb) show
** class name missing **
(hbnb)
(hbnb) show User
** instance id missing **
(hbnb)
(hbnb) show ClassNotFound a5999506-a045-42ac-919f-e9224183a527
** class doesn't exist **
(hbnb)
(hbnb) show User 1234
** no instance found **
(hbnb)
(hbnb)
(hbnb) User.show(a5999506-a045-42ac-919f-e9224183a527)
[User] (a5999506-a045-42ac-919f-e9224183a527) {'id': 'a5999506-a045-42ac-919f-e9224183a527', 'created_at': datetime.datetime(2023, 5, 14, 13, 18, 25, 272448), 'updated_at': datetime.datetime(2023, 5, 14, 13, 18, 25, 272491)}
(hbnb)
(hbnb) User.show()
** instance id missing **
(hbnb)
(hbnb) ClassNotFound.show()
** class doesn't exist **
(hbnb)
(hbnb) User.show(1234)
** no instance found **
(hbnb)
(hbnb) BaseModel.show(7f267122-09d8-4aa6-bd65-5b8df8d33f9d)
[BaseModel] (7f267122-09d8-4aa6-bd65-5b8df8d33f9d) {'id': '7f267122-09d8-4aa6-bd65-5b8df8d33f9d', 'created_at': datetime.datetime(2023, 5, 14, 13, 43, 46, 401830), 'updated_at': datetime.datetime(2023, 5, 14, 13, 43, 46, 401884)}
(hbnb)
```

3. **Destroy an existing object**

An object can be destroyed by calling the `destroy` command with the object's
class name and its id. Prints nothing if the object has been destroyed
successfully.

It has two syntaxes:

- `destroy <class name> <id>`
- `<class name>.destroy(<id>)`

If the class name is missing or an invalid class or invalid id is given, an
error message is printed as show below.

```Text
(hbnb) destroy BaseModel f267122-09d8-4aa6-bd65-5b8df8d33f9d    # object destroyed successfully.
(hbnb)
(hbnb) destroy BaseModel f267122-09d8-4aa6-bd65-5b8df8d33f9d    # object has already been destroyed.
** instance not found **
(hbnb)
(hbnb) destroy BaseModel 1234
** instance not found **
(hbnb)
(hbnb) destroy ClassNotFound a5999506-a045-42ac-919f-e9224183a527
** class doesn't exist **
(hbnb)
(hbnb) destroy User
** instance id missing **
(hbnb)
(hbnb) destroy
** class name missing **
(hbnb)
(hbnb) User.destroy(a5999506-a045-42ac-919f-e9224183a527)
(hbnb)
(hbnb) User.destroy(1234)
** instance not found **
(hbnb)
(hbnb) ClassNotFound.destroy()
** class doesn't exist **
(hbnb)
```

4. **Display all objects**

This can be accomplished using the `all` command.
The command can either be called witout any arguments to print all objects
or called with a specific class to print objects of that class only.

Syntax:

- `all`
- `all <class name>`
- `<class_name>.all()`

Using the `all <class name>` syntax is synonymous to `<class name>.all()`. They
both only print objects of given class.

If a class is given, it has to be an implemented class otherwise an error is
printed as show below.

```Text
(hbnb) all  # No object has been created yet hence nothing is printed.
(hbnb)
(hbnb) create Place
5f688b64-5306-4a08-9761-f6deeb722ef4
(hbnb) create City
481cce6e-ecf8-493c-ac83-2063d411c401
(hbnb) create User
500ffdec-d650-46af-87c3-a8d34bd8a2e2
(hbnb)
(hbnb) all
["[Place] (5f688b64-5306-4a08-9761-f6deeb722ef4) {'id': '5f688b64-5306-4a08-9761-f6deeb722ef4', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 28, 132497), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 28, 132522)}", "[City] (481cce6e-ecf8-493c-ac83-2063d411c401) {'id': '481cce6e-ecf8-493c-ac83-2063d411c401', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 32, 468915), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 32, 468949)}", "[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867946)}"]
(hbnb)
(hbnb) create State
d280bab-8318-4fc2-be4d-9ede4ead4191
(hbnb)
(hbnb) all
["[Place] (5f688b64-5306-4a08-9761-f6deeb722ef4) {'id': '5f688b64-5306-4a08-9761-f6deeb722ef4', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 28, 132497), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 28, 132522)}", "[City] (481cce6e-ecf8-493c-ac83-2063d411c401) {'id': '481cce6e-ecf8-493c-ac83-2063d411c401', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 32, 468915), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 32, 468949)}", "[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867946)}", "[State] (3d280bab-8318-4fc2-be4d-9ede4ead4191) {'id': '3d280bab-8318-4fc2-be4d-9ede4ead4191', 'created_at': datetime.datetime(2023, 5, 14, 14, 13, 59, 916280), 'updated_at': datetime.datetime(2023, 5, 14, 14, 13, 59, 916320)}"]
(hbnb)
(hbnb) all State
["[State] (3d280bab-8318-4fc2-be4d-9ede4ead4191) {'id': '3d280bab-8318-4fc2-be4d-9ede4ead4191', 'created_at': datetime.datetime(2023, 5, 14, 14, 13, 59, 916280), 'updated_at': datetime.datetime(2023, 5, 14, 14, 13, 59, 916320)}"]
(hbnb)
(hbnb) create State
d4a1f54d-9c69-48b4-9e1d-34a6eda90299
(hbnb) all State
["[State] (3d280bab-8318-4fc2-be4d-9ede4ead4191) {'id': '3d280bab-8318-4fc2-be4d-9ede4ead4191', 'created_at': datetime.datetime(2023, 5, 14, 14, 13, 59, 916280), 'updated_at': datetime.datetime(2023, 5, 14, 14, 13, 59, 916320)}", "[State] (d4a1f54d-9c69-48b4-9e1d-34a6eda90299) {'id': 'd4a1f54d-9c69-48b4-9e1d-34a6eda90299', 'created_at': datetime.datetime(2023, 5, 14, 14, 15, 8, 282666), 'updated_at': datetime.datetime(2023, 5, 14, 14, 15, 8, 282693)}"]
(hbnb)
(hbnb) all ClassNotFound
** class doesn't exist **
(hbnb)
(hbnb) Place.all()
["[Place] (5f688b64-5306-4a08-9761-f6deeb722ef4) {'id': '5f688b64-5306-4a08-9761-f6deeb722ef4', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 28, 132497), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 28, 132522)}"]
(hbnb)
(hbnb) ClassNotFound.all()
** class doesn't exist **
```

5. **Update an object's attributes**

The `update` command can be used to update an object's attributes.

Syntax:

- `update <class name> <id> <attribute name> <attribute value>`
- `<class name>.update(<id>, <attribute name>, <attribute value>)`
- `<class name>.update(<id>, <dict of attr_name/attr_value pairs>)`

Using the first two syntaxes, you can only update one attribute at a time
while the third one allows you to provide a dictionary of one or more
attributes to be updated.

Attribute values are converted to either int or float if they are of those
types otherwise are left as strings.
Example:
In the command `update User 500ffdec-d650-46af-87c3-a8d34bd8a2e2 "zip_code" "0001"`,
the zip code is converted into an integer before being assigned to zip_code.

If the class name or id are invalid, error messages are printed.
The same happens when either the attribute name or the value is not given.

```Text
(hbnb) show User 500ffdec-d650-46af-87c3-a8d34bd8a2e2   # Before updating.
[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867946)}
(hbnb)
(hbnb) update User 500ffdec-d650-46af-87c3-a8d34bd8a2e2 "first_name" "Brian"    # Adding new attribute.
(hbnb)
(hbnb) show User 500ffdec-d650-46af-87c3-a8d34bd8a2e2   # After updating
[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 31, 7, 939813), 'first_name': 'Brian'}
(hbnb)
(hbnb) update
** class name missing **
(hbnb)
(hbnb) update User 1234 'last_name' 'Kim'
** instance not found **
(hbnb)
(hbnb) update ClassNotFound 500ffdec-d650-46af-87c3-a8d34bd8a2e2 last_name "Kim"
** class doesn't exist **
(hbnb)
(hbnb) update User 500ffdec-d650-46af-87c3-a8d34bd8a2e2
** attribute name missing **
(hbnb)
(hbnb) update User 500ffdec-d650-46af-87c3-a8d34bd8a2e2 "last_name"
** value missing **
(hbnb)
(hbnb) User.update("500ffdec-d650-46af-87c3-a8d34bd8a2e2", "last_name", "Kim")    # Adding new attribute.
(hbnb)
(hbnb) User.show("500ffdec-d650-46af-87c3-a8d34bd8a2e2")
[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 31, 27, 239003), 'first_name': 'Brian', 'last_name': 'Kim'}
(hbnb)
(hbnb) User.update("500ffdec-d650-46af-87c3-a8d34bd8a2e2", "last_name")
** value missing **
(hbnb)
(hbnb) User.update("500ffdec-d650-46af-87c3-a8d34bd8a2e2", "last_name", "Kimathi")    # Updating existing attribute
(hbnb)
(hbnb) User.show("500ffdec-d650-46af-87c3-a8d34bd8a2e2")
[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 31, 57, 131813), 'first_name': 'Brian', 'last_name': 'Kimathi'}
(hbnb)
(hbnb) User.update("500ffdec-d650-46af-87c3-a8d34bd8a2e2", {'middle_name': 'Mid'})    # Using one attribute in dictionary.
(hbnb) User.show(500ffdec-d650-46af-87c3-a8d34bd8a2e2)
[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 32, 14, 939000), 'first_name': 'Brian', 'last_name': 'Kimathi', 'middle_name': 'Mid'}
(hbnb)
(hbnb) User.update("500ffdec-d650-46af-87c3-a8d34bd8a2e2", {'age': "20", "gender": "male", "mobile": "0712345678"})    # Using several attributes in dictionary.
(hbnb) User.show("500ffdec-d650-46af-87c3-a8d34bd8a2e2")
[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 32, 34, 932300), 'first_name': 'Brian', 'last_name': 'Kimathi', 'middle_name': 'Mid', 'age': 20, 'gender': 'male', 'mobile': 0712345678}
(hbnb)
(hbnb) User.update("500ffdec-d650-46af-87c3-a8d34bd8a2e2", "bio", "A smart guy")    # A space separated value can be placed between double quotes.
(hbnb)
(hbnb) User.show(500ffdec-d650-46af-87c3-a8d34bd8a2e2)
[User] (500ffdec-d650-46af-87c3-a8d34bd8a2e2) {'id': '500ffdec-d650-46af-87c3-a8d34bd8a2e2', 'created_at': datetime.datetime(2023, 5, 14, 14, 12, 36, 867910), 'updated_at': datetime.datetime(2023, 5, 14, 14, 32, 56, 512600), 'first_name': 'Brian', 'last_name': 'Kimathi', 'middle_name': 'Mid', 'age': 20, 'gender': 'male', 'mobile': 0712345678, 'bio': 'A smart guy'}
(hbnb)
```

6. **Counting number of instances of an object**

The `count` command can be applied on a certain class to get number of
instances of that class.

Synatx:

- `<class name>.count()`

If class is not implemented, an error message is printed as shown below.

```Text
(hbnb) all User
["[User] (36d7f111-8c61-43ec-9247-eadd4a0cbe86) {'id': '36d7f111-8c61-43ec-9247-eadd4a0cbe86', 'created_at': datetime.datetime(2023, 5, 14, 15, 15, 33, 268285), 'updated_at': datetime.datetime(2023, 5, 14, 15, 15, 33, 268330)}", "[User] (8d51fc94-b60c-4b1a-ac1f-8845e66d82ca) {'id': '8d51fc94-b60c-4b1a-ac1f-8845e66d82ca', 'created_at': datetime.datetime(2023, 5, 14, 15, 15, 34, 394980), 'updated_at': datetime.datetime(2023, 5, 14, 15, 15, 34, 395013)}", "[User] (217bae05-977a-43c4-8ad1-1e2354871dfa) {'id': '217bae05-977a-43c4-8ad1-1e2354871dfa', 'created_at': datetime.datetime(2023, 5, 14, 15, 15, 34, 985364), 'updated_at': datetime.datetime(2023, 5, 14, 15, 15, 34, 985397)}", "[User] (e337000e-cd99-4b62-8a67-f9086d11abc9) {'id': 'e337000e-cd99-4b62-8a67-f9086d11abc9', 'created_at': datetime.datetime(2023, 5, 14, 15, 15, 35, 582496), 'updated_at': datetime.datetime(2023, 5, 14, 15, 15, 35, 582529)}"]
(hbnb)
(hbnb) User.count()
4
(hbnb)
(hbnb) User.destroy(36d7f111-8c61-43ec-9247-eadd4a0cbe86)
(hbnb)
(hbnb) User.count()
3
(hbnb)
(hbnb) ClassNotFound.count()
** class doesn't exist **
(hbnb)
(hbnb) all Place    # No Place instance exists.
(hbnb)
(hbnb) Place.count()
0
```

The interpreter can perform above tasks while taking care of any errors that
may arise.

### **More Info**

To find out more about individual classes and methods, you can look into
the documentation of the specific class or method in the module it's found in.

### Author(s)

- [Brian Kimathi](https://github.com/bryokim)
