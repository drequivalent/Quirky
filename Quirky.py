"""A module for working with Typing Quirk regular expressions.

The regular expressions for quirkification and dequirkification are defined by simple XML format. See documentation for particular class or function to learn more.
Written for Homestuck Translation Project."""

import re
from xml.etree import ElementTree

class TypingQuirk:
    """A typing quirk for particular character.
    
    One character can have multiple identifying aliases, multiple regular expression replacing rules for quirkification or dequirkification of the string. Theese attributes are defined as lists. The name and color of the character is a string."""
    
    def __init__(self):
        """Declares attributes, such as name of character that uses this quirk, color of the character, their aliases, their rules for quirkification and rules for dequirkification. Takes no arguments."""   
        self.name = ""
        self.color = ""
        self.aliases = []
        self.direct = []
        self.inverse = []
    
    def set_quirk_name(self, name):
        """Sets the name of character that uses this quirk. The name is used only for the purposes of clarity and has no say in quirkification process. Takes the only argument, which is a string. If it's not the case, raises the TypeError exception."""
        if type(name) is str:
            self.name = name
        else:
            raise TypeError("name must be a string.")
        
    def set_color(self, color):
        """Sets color of the quirk. This can be used to discriminate one character (or state of character) from another. Takes the only argument, which is a string. If it's not the case, raises the TypeError exception."""
        if type(color) is str:
            self.color = color
        else:
            raise TypeError("color must be a string.")
    
    def add_alias(self, alias):
        """Adds aliases for character that uses this quirk. Aliases are used to discriminate one character from another. Takes one argument, which can be a string or a list of strings. If it's not the case, raises the TypeError exception."""
        if type(alias) is list:
            if all(isinstance(item, str) for item in alias) == True:
                self.aliases.extend(alias)
            else:
                raise TypeError("list must contain only strings.")
        elif type(alias) is str:
            self.aliases.append(alias)
        else:
            raise TypeError("alias must be string or list of strings.")
    
    def add_direct_rule(self, rule):
        """Adds rules for quirkification. Theese rules are used to quirkify a raw string. Takes one argument, which can be an instance of Rule class or a list of such instances. If it's not the case, raises the TypeError exception."""
        if type(rule) is list:
            if all(isinstance(item, Rule) for item in rule) == True:
                self.direct.extend(rule) 
            else:
                raise TypeError("list must contain only Rule instances.")
        else:
            if isinstance(rule, Rule) == True:
                self.direct.append(rule)
            else:
                raise TypeError("this method takes only Rule class instances or lists of Rule class instances.")
    
    
    def add_inverse_rule(self, rule):
        """Adds rules for dequirkification. Theese rules are used to dequirkify a quirkified string. Takes one argument, which can be an instance of Rule class or a list of such instances. If it's not the case, raises the TypeError exception."""
        if type(rule) is list:
            if all(isinstance(item, Rule) for item in rule) == True:
                self.inverse.extend(rule) 
            else:
                raise TypeError("list must contain only Rule instances.")
        else:
            if isinstance(rule, Rule) == True:
                self.inverse.append(rule)
            else:
                raise TypeError("this method takes only Rule class instances or lists of Rule class instances.")
    
    def get_name(self):
        """Returns name of character that uses this quirk. Takes no arguments."""
        return self.name
        
    def get_color(self):
        """Returns color of character that uses this quirk. Takes no arguments."""
        return self.color
        
    def get_aliases(self):
        """Returns list of aliases for the character. Takes no arguments."""
        return self.aliases
        
    def get_direct_rules(self):
        """Returns list of Rule instances for quirkification. Takes no arguments."""
        return self.direct
    
    def get_inverse_rules(self):
        """Returns list of Rule instances for dequirkification. Takes no arguments."""
        return self.inverse
    
    def quirkify(self, string):
        """Quirkifies a string, which means if you give it a normal, healthy human-speech string, it will output the string with a typing quirk of the character, according to rules of quirkification defined by the attribute. Takes the only argument, which must be a string and returns a quirkified string. If it's not the case, raises TypeError exception."""
        if type(string) is str:
            for rule in self.direct:
                string = re.sub(rule.get_regexp(), rule.get_replacer(), string)
            return string
        else:
            raise TypeError("this method takes only strings.")
    
    def dequirkify(self, string):
        """Dequirkifies a string, which means if you give it a string with a typing quirk of the character, it will output you a normal comprehensive string, corrected according to rules of dequirkification defined by the attribute. Takes only one argument, which must be a string and returns a dequirkified string. If it's not the case, raises TypeError exception."""
        if type(string) is str:
            for rule in self.inverse:
                string = re.sub(rule.get_regexp(), rule.get_replacer(), string)
            return string
        else:
            raise TypeError("this method takes only strings.")

class Rule:
    """A rule for quirkification or dequirkification.
    
    Has only two attributes, which are strings. One defines the regular expression to look for, the other defines the regular expression to replace with."""
    regexp = ""
    replacewith = ""
    
    def set_regexp(self, regexp):
        """Sets a regular expression to look for. Takes one argument which must be a string. If it's not the case, raises a TypeError exception."""
        if type(regexp) == str:
            self.regexp = regexp
        else:
            raise TypeError("regexp must be a string.")
    
    def set_replacer(self, regexp):
        """Sets a regular expression to replace with. Takes one argument which must be a string. If it's not the case, raises a TypeError exception."""
        if type(regexp) == str:
            self.replacewith = regexp
        else:
            raise TypeError("regexp must be a string.")
    
    def get_regexp(self):
        """Returns a regular expression to look for. Takes no arguments."""
        return self.regexp
    
    def get_replacer(self):
        """Returns a regular expression to replace with. Takes no arguments."""
        return self.replacewith


def create_quirk(name, color, aliases, direct, inverse, verbose = False):
    """Creates a typing quirk for particular character. Takes four arguments, which are name of the character (string), color of the character (string) aliases of the character (string or list of strings), rules for quirkification (Rule class instance or list of those) and rules for dequirkification (Rule class instance or list of those). The "verbose" key value is not obligatory, it defines if you want an output to the console for testing/checking purposes. We stay quiet by default."""
    created_quirk = TypingQuirk()
    created_quirk.set_quirk_name(name)
    created_quirk.set_color(color)
    created_quirk.add_alias(aliases)
    created_quirk.add_direct_rule(direct)
    created_quirk.add_inverse_rule(inverse)
    if verbose:
        check_list_direct = []
        check_list_inverse = []
        for item in direct:
           check_list_direct.append(item.get_regexp() + " to " + item.get_replacer())
        for item in inverse:
           check_list_inverse.append(item.get_regexp() + " to " + item.get_replacer())
        check_tuple = (name, color, ' or '.join(aliases), ', '.join(check_list_direct), ', '.join(check_list_inverse))
        print("Creating %s with color of %s as %s with %s as quirkification rules and %s as dequirkification rules" % check_tuple)
    return created_quirk

def create_rule(regexp, replacewith):
    """Creates a rule for replacement. Takes two arguments - a regular expression to look for and a regular expression to replace with, which both must be strings, and returns a Rule instance. If it's not the case, raises TypeError exception."""
    created_rule = Rule()
    if type(regexp) is str:
        created_rule.set_regexp(regexp)
    else:
        raise TypeError("the regular expression to look for must be a string.")
    if type(replacewith) is str:
        created_rule.set_replacer(replacewith)
    else:
        raise TypeError("the regular expression to replace with must be a string.")
    return created_rule

def create_quirks_list(xmlstring, verbose = False):
    """Creates list of typing quirks from XML string. Takes one argument, which must be a string full of sweet XML, and returns a list filled with delicious TypingQuirk instances. The "verbose" key value is not obligatory, it defines if you want an output to the console for testing/checking purposes. We stay quiet by default."""
    tree = ElementTree.fromstring(xmlstring)
    quirks = []
    for element in tree.iter(tag="rule"):
        quirk_name = element.attrib['name']
        color = element.attrib['color']
        aliases = []
        direct_rules = []
        inverse_rules = []
        for subelement in element.iter(tag="alias"):
            alias = subelement.attrib['value']
            aliases.append(alias)
        for subelement in element.iter(tag="quirk"):
            direct_from = subelement.attrib['from']
            direct_to = subelement.attrib['to']
            direct_rules.append(create_rule(direct_from, direct_to))
        for subelement in element.iter(tag="dequirk"):
            inverse_from = subelement.attrib['from']
            inverse_to = subelement.attrib['to']
            inverse_rules.append(create_rule(inverse_from, inverse_to))
        quirks.append(create_quirk(quirk_name, color, aliases, direct_rules, inverse_rules, verbose = verbose))
    return quirks
    
def create_quirks_dict(xmlstring, verbose = False):
    """Creates a dictionary of typing quirks from XML string. Takes one argument, which must be a string full of sweet XML, and returns a dictionary filled with delicious pairs of character names and TypingQuirk instances. The "verbose" key value is not obligatory, it defines if you want an output to the console for testing/checking purposes. We stay quiet by default."""
    quirklist = create_quirks_list(xmlstring, verbose = verbose)
    quirk_dictionary = {}
    for quirk in quirklist:
        quirk_dictionary[quirk.get_name()] = quirk
    return quirk_dictionary

def create_quirks_dict_from_quirks_list(quirklist):
    """Creates a dictionary of typing quirks from list of typing quirks. Takes one argument, which must be a list of TypingQuirk instances, and returns a dictionary of character name - TypingQuirk instance pairs.
    May be deprecated in the future."""
    quirk_dictionary = {}
    for quirk in quirklist:
        quirk_dictionary[quirk.get_name()] = quirk
    return quirk_dictionary
    
def create_quirks_list_from_file(filename, verbose = False):
    """Creates list of typing quirks from XML file. Takes one argument, which must be a string with the filesystem path pointing to a file full of sweet XML, and returns a list filled with delicious TypingQuirk instances. The "verbose" key value is not obligatory, it defines if you want an output to the console for testing/checking purposes. We stay quiet by default."""
    return create_quirks_list(open(filename, "r").read(), verbose = verbose)

def create_quirks_dict_from_file(filename, verbose = False):
    """Creates list of typing quirks from XML file. Takes one argument, which must be a string with the filesystem path pointing to a file full of sweet XML, and returns a list filled with delicious pairs of character names and TypingQuirk instances. The "verbose" key value is not obligatory, it defines if you want an output to the console for testing/checking purposes. We stay quiet by default."""
    return create_quirks_dict(open(filename, "r").read(), verbose = verbose)

def quirks_to_xml(source, nice = True):
    """Creates a string of sweet XML full of exquisite typing quirks for later use from objects in source. Takes one, maybe two arguments, the first one must be a list or a dictionary of TypingQuirk class instances, and returns a string with the gorgeous XML markup. If it's not the case, raises TypeError exception. The second argument is not obligatory, it just defines if you want your output nice and pretty and indented and all. It says yes by default."""
    if type(source) is dict:
        source = source.values()
    if all(isinstance(item, TypingQuirk) for item in source) == True:
        doc_element = ElementTree.Element("document")
        for item in source:
            rule_element = ElementTree.SubElement(doc_element, "rule")
            rule_element.set("name", item.get_name())
            rule_element.set("color", item.get_color())
            for alias in item.get_aliases():
                alias_element = ElementTree.SubElement(rule_element, "alias")
                alias_element.set("value", alias)
            for quirk in item.get_direct_rules():
                quirk_element = ElementTree.SubElement(rule_element, "quirk")
                quirk_element.set("from", quirk.get_regexp())
                quirk_element.set("to", quirk.get_replacer())
            for dequirk in item.get_inverse_rules():
                dequirk_element = ElementTree.SubElement(rule_element, "dequirk")
                dequirk_element.set("from", dequirk.get_regexp())
                dequirk_element.set("to", dequirk.get_replacer())
        #~ Oh my god, the following is ugly
        xml_string = "<?xml version='1.0' encoding='utf-8'?>" + ElementTree.tostring(doc_element, encoding="utf-8")
        if nice == True:
            import xml.dom.minidom
            return xml.dom.minidom.parseString(xml_string).toprettyxml(encoding="utf-8")
        else:
            return xml_string
    else:
        raise TypeError("source argument must contain only TypingQuirk instances")
