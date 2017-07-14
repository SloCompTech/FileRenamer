# Renamer
# charset=UTF-8
import os
import sys

# List handling
FILENAME_ARRAY1 = []
FILENAME_ARRAY2 = []
def addFileEntry(old,new):
    FILENAME_ARRAY1.append(old)
    FILENAME_ARRAY2.append(new)
def findFileEntry(old):
    for i in range(len(FILENAME_ARRAY1)):
        if FILENAME_ARRAY1[i] == old:
            return FILENAME_ARRAY2[i]
    return None

# Name escaping
OLD_CHAR = ['č','š','ž','Č','Š','Ž',':','.','!',' ','(',')','&']
NEW_CHAR = ['c','s','z','C','Š','Z','_','_','_','_','_','_','_']
def escapeName(old_name):
    return "".join([x for x in old_name if ord(x) < 128])
    buffer = ""
    found = False
    # For each char in old name
    for i in range(len(old_name)):
        # Check if in list
        found = False
        for li in range(len(OLD_CHAR)):
            if OLD_CHAR[li] == old_name[i]:
                buffer += NEW_CHAR[li]
                found = True
                break
        # If char not found in the list just append
        if not found:
            buffer += old_name[i]
    return buffer

# First check if we got all arguments
flag_check = True
dir_pos = 3
file_pos = 2
if len(sys.argv) > 0:
    if sys.argv[0] == "python":
        if len(sys.argv) < 4:
            flag_check = False
        else:
            file_pos = 2
            dir_pos = 3
    else:
        if len(sys.argv) < 3:
            flag_check = False
        else:
            file_pos = 1
            dir_pos = 2
if not flag_check:
    print("Usage: python <scriptname> <filename_list> <directory>")
    sys.exit(-1)

# Load filenames to rename
with open(sys.argv[file_pos]) as f:
    for line in f:
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        old_name,new_name = line.split(";")
        # Check if we need to remove extentions
        if old_name.rfind('.') != -1:
            old_name = old_name[:old_name.rindex('.')]
        if new_name.rfind('.') != -1:
            new_name = new_name[:new_name.rindex('.')]    
        addFileEntry(old_name,new_name)
print(str(len(FILENAME_ARRAY1)) + " entrys loaded")

# Search directory, rename things
RENAME_COUNTER = 0
for root,dirs,filenames in os.walk(sys.argv[dir_pos]):
    # First check files so we can end it quick
    for f in filenames:
        # Split filename and extension
        filename, file_extension = os.path.splitext(f)
        # Check if some name match in file
        new_name = findFileEntry(filename)
        if new_name != None:
            # Rename file
            new_name = escapeName(new_name)
            try:
                os.rename(os.path.join(root, f),os.path.join(root, new_name + file_extension))
            except FileExistsError:
                count = 1
                while True:
                    try:
                        # Try to rename
                        os.rename(os.path.join(root, f),os.path.join(root, new_name + "_" + str(count) + file_extension))
                        # Break loop if success
                        break
                    except FileExistsError:
                        # Increase counter
                        count = count + 1
            RENAME_COUNTER = RENAME_COUNTER + 1
            print(os.path.join(root, f) + " => " + new_name + file_extension)
        else:
            # Just print file, no changes were made to the file
            print(os.path.join(root, f))
    # Then check all folders
    for d in dirs: 
        # Check if some name match in dir
        new_name = findFileEntry(d)
        if new_name != None:
            # Rename dir
            new_name = escapeName(new_name)
            try:
                os.rename(os.path.join(root, d),os.path.join(root, new_name))
            except FileExistsError:
                count = 1
                while True:
                    try:
                        # Try to rename
                        os.rename(os.path.join(root, d),os.path.join(root, new_name + "_" + str(count)))
                        # Break loop if success
                        break
                    except FileExistsError:
                        # Increase counter
                        count = count + 1
            RENAME_COUNTER = RENAME_COUNTER + 1
            print(os.path.join(root, d) + " => " + new_name)
        else:
            # Just print dir, no changes were made to the dir
            print(os.path.join(root, d))
# Print progress
print(str(RENAME_COUNTER) + " objects renamed")
sys.exit(0)
