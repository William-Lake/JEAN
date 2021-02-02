import glob
import logging
import os
import subprocess


def convert_to_num(user_selection):

    try:

        return int(user_selection.strip())

    except:

        return None


def select_java_home(java_dirs):

    user_selection = None

    while user_selection is None:

        print("Please select one of the following as your new JAVA_HOME:\n")

        for idx, d in enumerate(java_dirs):

            print(f"[{idx + 1}] : {d}")

        user_selection = convert_to_num(input("\n\n\n?"))

        if user_selection is not None and (
            0 < user_selection and user_selection <= len(java_dirs)
        ):

            return java_dirs[user_selection - 1]

        print("PLEASE PROVIDE VALID INPUT" + os.linesep * 6)


def collect_java_dirs():

    java_dirs = []

    potential_java_dirs = [r"C:\Program Files\Java", r"C:\Program Files (x86)\Java"]

    for pjd in potential_java_dirs:

        dirs = [d for d in glob.glob(f"{pjd}/*")]

        for jd in dirs:

            is_java_dir = (
                len([d for d in glob.glob(f"{jd}/**/java.exe", recursive=True)]) > 0
            )

            if is_java_dir:

                java_dirs.append(jd)

    return java_dirs


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    print(
        "!!!!! THIS SCRIPT NEEDS TO BE RAN FROM AN ADMIN COMMAND PROMPT FOR IT TO WORK !!!!!\n\n\n"
    )

    java_home = None

    try:

        java_home = os.environ["JAVA_HOME"]

    except KeyError as e:

        logging.error(
            "No JAVA_HOME environment variable found. Set this variable, then try again."
        )

        exit(1)

    java_dirs = collect_java_dirs()

    if not java_dirs:

        logging.error(
            "No Java directory found. What? How did this even...never mind. Just install Java then get back to me."
        )

        exit(1)

    print(f"\t---  Current Java Home is {java_home}  ---\n\n\n")

    new_java_home = select_java_home(java_dirs)

    try:

        subprocess.run(
            ["setx", "JAVA_HOME", "-m", f"{new_java_home}"], shell=True, check=True
        )

    except:

        logging.error(
            "Error thrown when trying to set environment variable. You may need to run this script from an admin prompt."
        )

        exit(1)
