#! /usr/bin/env python3

import os
from parser import parameter_parser
from pdfrw import PdfReader, PdfWriter

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    NOTE = '\u001b[38;5;245m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PDFMetadataEditor:
    def __init__(self, filename):
        self.filename  = filename
        self.trailer   = PdfReader(self.filename)

    def _overwrite_confirmation(self):
        ans = input("Are you sure to overwrite the file? [y/n] ")
        if ans.lower() == "y":
            return True
        return False
    def _get_operation(self):
        ans = 1
        print("")
        print("#" * 25)
        print("Valid Operations:")
        print("1. Edit Current Metadata")
        print("2. Add Attributes to Metadata")
        print("3. Delete Attributes from Metadata")
        print("4. No operation")
        print("")
        while True:
            try:
                ans = int(input("Which operation would you like to perform? [1/2/3/4] "))
                if ans not in [1, 2, 3, 4]:
                    raise ValueError
                break
            except ValueError:
                print("Please provide a valid operation number.")
        print("#" * 25)
        print("")
        return ans

    def get_metadata_object(self):
        return self.trailer.Info

    def set_attribute(self, attr, value):
        if (attr[0] == "/"):
            attr = attr[1:]
        setattr(self.trailer.Info, attr, value)

    def summary(self):
        info = self.get_metadata_object()
        print("")
        print("#" * 25)
        print("SUMMARY")
        print("Number of Attributes: {}".format(len(info)))
        print("Current Metadata Attributes:")
        for key in info:
            if (key[0] == "/"):
                key = key[1:]
            print("    - {}".format(key))
        print("#" * 25)
        print("")

    def print_metadata(self):
        info = self.get_metadata_object()
        print("")
        print("#" * 25)
        print("{} Metadata:".format(self.filename))
        print("Number of Attributes: {}".format(len(info)))
        for key in info:
            if (key[0] == "/"):
                key = key[1:]
            print("    - {}: {}".format(key, getattr(info, key)))
        print("#" * 25)
        print("")

    def export_to_file(self, export_filename="edited.pdf"):
        if (export_filename):
            try:
                print("Exporting file...")
                PdfWriter(export_filename, trailer=self.trailer).write()
            except Exception as e:
                print("{}Error while exporting: {}{}".format(bcolors.FAIL, e, bcolors.ENDC))
            else:
                print("{}File is exported to {}.{}".format(bcolors.OKGREEN, export_filename, bcolors.ENDC))

    def edit_metadata(self):
        ans = input("Which attribute would you like to edit? [Name of the Attribute or leave it blank if you want to edit all of them] ")
        print("Note: Leave the value section blank, if you don't want to edit it.")
        if not ans:
            for key in self.trailer.Info:
                if (key[0] == "/"):
                    key = key[1:]
                value = input("{} {}[{}]{}: ".format(key, bcolors.NOTE, getattr(self.trailer.Info, key), bcolors.ENDC))
                if value:
                    self.set_attribute(key, value)
                    print("Attribute {} is changed to {}!".format(key, value))
        elif not hasattr(self.trailer.Info, ans):
            print("{}This attribute doesn't exist in the metadata. Please consider adding new attributes operation.{}".format(bcolors.FAIL, bcolors.ENDC))
        else:
            value = input("{} {}[{}]{}: ".format(ans, bcolors.NOTE, getattr(self.trailer.Info, ans), bcolors.ENDC))
            if value:
                self.set_attribute(ans, value)
                print("Attribute {} is changed to {}!".format(ans, value))

    def create_attribute(self):
        ans = "y"
        while (ans == "y"):
            ans = input("Would you like to create a new attribute? [y/n] ")
            if ans.lower() == "y":
                attr = input("Attribute Name: ")
                if (attr):
                    value = input("Attribute Value: ")
                    self.set_attribute(attr, value)
                    if (hasattr(self.trailer.Info, attr)):
                        print("Attribute {} is added with value {}!".format(attr, value))
                else:
                    print("Please provide a valid attribute name.")
                print("")

    def delete_attribute(self):
        ans = "y"
        while (ans == "y"):
            ans = input("Would you like to delete an existing attribute? [y/n] ")
            if ans.lower() == "y":
                attr = input("Attribute Name: ")
                if (attr and hasattr(self.trailer.Info, attr)):
                    self.trailer.Info.pop("/{}".format(attr))
                    print("Attribute {} is deleted!".format(attr))
                else:
                    print("Please provide a valid attribute name.")
                print("")

    def open_editor(self):
        operation  = self._get_operation()
        changeFlag = False
        while (operation != 4):
            self.summary()
            if (operation == 1):
                self.edit_metadata()
                changeFlag = True
            elif (operation == 2):
                self.create_attribute()
                changeFlag = True
            elif (operation == 3):
                self.delete_attribute()
                changeFlag = True

            if (changeFlag):
                print("")
                print("Operation is done!")
                ans = input("Would you like to the current status? [y/n] ")
                if (ans.lower() == 'y'):
                    self.print_metadata()
                ans = input("Would you like to perform another operation? [y/n] ")
                if (ans.lower() == 'y'):
                    operation = self._get_operation()
                else:
                    return changeFlag
        print("Closing the editor...")
        print("")
        return changeFlag

def main(args):
    document = PDFMetadataEditor(args.FILENAME)
    if (args.print):
        document.print_metadata()
    else:
        out_filename = args.export
        if args.overwrite:
            if document._overwrite_confirmation():
                out_filename = args.FILENAME
        if (document.open_editor()):
            document.export_to_file(export_filename=out_filename)

if (__name__ == "__main__"):
    args = parameter_parser()
    main(args)