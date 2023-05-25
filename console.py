#!/usr/bin/python3
"""HBNB Command Interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
import re
from shlex import split
from models.user import User
from models.state import State
from models.city import City
from models.place import Place



def parse(line):
    curly_brackets = re.search(r"\{(.*?)\}", line)
    bracket = re.search(r"\[(.*?)\]", line)
    if curly_brackets is None:
        if bracket is None:
            return [i.strip(",") for i in split(line)]
        else:
            l_line = split(line[bracket.span()[0]])
            r_line = [i.strip(",") for i in l_line]
            r_line.append(bracket.group())
            return r_line
    else:
        l_line = split(line[:curly_brackets.span()[0]])
        r_line = [i.strip(",") for i in l_line]
        r_line.append(curly_brackets.group())
        return r_line

class HBNBCommand(cmd.Cmd):
    """Starts the HBNB Command interpreter"""
    prompt = "(hbnb) "


    def do_create(self, line):
        """Create a new object instance and prints its id"""
        if len(parse(line)) == 0:
            print("** class name missing **")
        elif parse(line)[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(parse(line)[0]().id))
            storage.save()

    def do_show(self, line):
        """Print the string representation of an instance"""
        if len(parse(line)) == 0:
            print("** class name is missing **")
        elif parse(line)[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(parse(line)) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(parse(line)[0], parse(line)[1]) not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()["{}.{}".format(parse(line)[0], parse(line)[1])])

    def do_destroy(self,line):
        """"""
        if len(parse(line)) == 0:
            print("** class name missing **")
        elif parse(line)[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(parse(line)) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(parse(line)[0], parse(line)[1]) not in storage.all().keys():
            print("** no instance found **")
        else:
            del storage.all()["{}.{}".format(parse(line)[0], parse(line)[1])]
            storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances based on or not
        on the class name"""
        if len(parse(line)) > 0 and parse(line)[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            my_ob = []
            for ob in storage.all().values():
                if len(parse(line)) > 0 parse(line)[0] == ob.__class__.__name__:
                    my_ob.append(ob.__str__())
                elif len(parse(line)) == 0:
                    my_ob.append(ob.__str__())
            print(my_ob)
            
    def do_update(self, line):
        """"""
        if len(parse(line)) == 0:
            print("** class name missing **")
            return False
        if parse(line)[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(parse(line)) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(parse(line)[0], parse(line)[1]) not in storage.all().keys():
            print("** no instance found **")
            return False
        if len(parse(line)) == 2:
            print("** attribute name missing **")
            return False
        if len(parse(line)) == 3:
            try:
                type(eval(parse(line)[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(parse(line)) == 4:
            obj = storage.all()["{}.{}".format(parse(line)[0], parse(line)[1])]
            if parse(line)[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[parse(line)[2]])
                obj.__dict__[parse(line)[2]] = value_type(parse(line)[3])
            else:
                obj.__dict__[parse(line)[2]] = parse(line)[3]
        elif type(eval(parse(line)[2])) == dict:
            obj = storage.all()["{}.{}".format(parse(line)[0], parse(line)[1])]
            for k, v in eval(parse(line)[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = value_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


    def emptyline(self):
        pass

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Exit the program"""
        return True

if __name__ == "__main__":
    HBNBCommand().cmdloop()
