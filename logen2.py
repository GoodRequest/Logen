import sys
import subprocess
import os.path
import argparse
import re
import html

# - Classes

class Translation:
    def __init__(self, type, translation):
        self.type = type
        self.translation = translation

    def output(self):
        return """<key>{}</key>
        <string>{}</string>""".format(self.type, self.translation)


class Variable:
    def __init__(self, key, translations):
        self.key = key
        self.translations = translations

    def string_of_translations(self, translation):
        return translation.output()
    
    def output(self):
        list_of_transalations_strings = map(self.string_of_translations, list(self.translations))
        joined_strings = "\n".join(list_of_transalations_strings)
        return """<key>{}</key>
             <dict>
                 <key>NSStringFormatSpecTypeKey</key>
                 <string>NSStringPluralRuleType</string>
                 <key>NSStringFormatValueTypeKey</key>
                 <string>d</string>
                 {}
             </dict>""".format(self.key, joined_strings)

class LocalizedString:
    def __init__(self, key, string, variables):
        self.key = key
        self.string = string
        self.variables = variables

    def string_of_variables(self, variables):
        return variables.output()

    def output(self):
        list_of_transalations_strings = map(self.string_of_variables, list(self.variables))
        joined_strings = "\n".join(list_of_transalations_strings)
        value = """<key>{}</key>
         <dict>
             <key>NSStringLocalizedFormatKey</key>
             <string>{}</string>
             {}
         </dict>"""
        return value.format(self.key, self.string, joined_strings)

# - Ensure Google APIs are installed via PIP

def import_google_apis(firstAttempt):
    try:
        global Request
        global Credentials
        global InstalledAppFlow
        global HttpError
        global build

        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.errors import HttpError
        from googleapiclient.discovery import build
    except ImportError as error:
        pip_install_google_apis()

        if firstAttempt:
            import_google_apis(False)
        else:
            print("❌ FAILED TO IMPORT GOOGLE APIS ❌")
            sys.exit(1)


def pip_install_google_apis():
    PIP_INSTALL_LIBS = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib"
    ]
    subprocess.call(PIP_INSTALL_LIBS)

import_google_apis(True)

# - Variables

SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
LOCALIZATION_PATH: str = "Resources/Localization"

SPREADSHEET_ID: str = None
RANGE: str = None
PROJECT_NAME: str = None

# - Authentication

def authorize_and_get_spreadsheet():
    credentials = None
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPE)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPE
            )
            credentials = flow.run_local_server(port=8080)

        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE
        ).execute()
        values = result.get("values", [])

        if not values:
            print("❌ NO DATA FOUND IN RANGE IN SPREADSHEET ❌")
            exit()

        return values

    except HttpError as error:
        print("❌ HTTP error:", error, "❌")
        exit()

# - Localization generator

def get_languages(spreadsheet):
    headers = spreadsheet[0]
    languages = []
    for header in headers:
        if len(header) == 2:
            languages.append(header)

    return languages

def generate_strings(spreadsheet, language):
    ios_column_name = "iOS"
    ios_column_first_match = [header for header in spreadsheet[0] if ios_column_name in header][0]
    ios_column_index = spreadsheet[0].index(ios_column_first_match)

    language_column_index = spreadsheet[0].index(language)

    empty_string = ""
    list_of_strings = []
    pluralized_rows = []

    for row in spreadsheet:
        try:
            if not row[ios_column_index]:
                continue
            else:
                key = row[ios_column_index]
                if "(pluralized)" in key:
                    pluralized_rows.append(row)

                translation = fix_special_substrings(row[language_column_index])
                localized_entry = as_localized_entry(key, translation)
                list_of_strings.append(localized_entry)

        except IndexError:
            continue

    pluralized_strings = create_pluralized_file(pluralized_rows, language_column_index, ios_column_index)
    return list_of_strings, pluralized_strings

def create_pluralized_file(rows, language_index, ios_column_index):
    localized_strings = []
    key = ""
    for row in rows:
        localized_string = ""
        variables = []
        key = row[ios_column_index]
        for index, variable in enumerate(separate_strings(row[language_index])):
            if "%" in variable:
                localized_string = localized_string + "%#@variable{}@".format(index)
                variables.append(Variable("variable{}".format(index), extract_pluralized_translations(variable)))
            else:
                localized_string = localized_string + variable
        localized_strings.append(LocalizedString(key.replace("(pluralized)", ""), localized_string, variables))
    return localized_strings

# - Separate string for pluralized string 

def separate_strings(input_string):
    # Define a regular expression pattern to capture substrings around '%[0-9]+\$@'
    pattern = r'([^%]*)(%[0-9]+\$@[^%]*)'

    # Use re.split to split the input string around the specified pattern
    result = re.split(pattern, input_string)

    # Remove empty strings from the result
    result = [segment for segment in result if segment]

    return result

# - Extract translations from pluralized string

def extract_pluralized_translations(input_string):
    translations = []

    # Continue loop as long as there are pairs of tags
    while "<" in input_string and ">" in input_string:
        # Find the opening tag
        start_index = input_string.find("<")
        # Find the closing tag
        end_index = input_string.find(">")

        if start_index != -1 and end_index != -1:
            # Extract the tag content
            tag = input_string[start_index + 1:end_index]

            # Check if the tag is a valid pluralization tag
            if tag in ["one", "two", "few", "many", "other", "zero"]:
                # Find the opening tag of the translation content
                translation_start = input_string.find("<{}>".format(tag))
                # Find the closing tag of the translation content
                translation_end = input_string.find("</{}>".format(tag))

                if translation_start != -1 and translation_end != -1:
                    # Extract the translation content
                    translation = input_string[:start_index] + input_string[translation_start + len(tag) + 2:translation_end]

                    # Append the translation to the list
                    translations.append(Translation(tag, translation))

                    # Modify input_string to remove the current translation tag pair
                    input_string = input_string[:start_index] + input_string[translation_end + len(tag) + 3:]

    if not translations:
        # Default to 'other' if no specific pluralization tag is found
        translations.append(Translation("other", input_string))

    return translations

# - Fix escapes and substrings

def fix_special_substrings(string):
    s_substring = "%s"
    s_substring_replacement = "%@"

    quote_substring = '"'
    quote_substring_replacement = '\\"'

    if re.search(quote_substring, string):
        string = string.replace(
            quote_substring,
            quote_substring_replacement,
            string.count(quote_substring)
        )

    if re.search(s_substring, string):
        string = string.replace(
            s_substring,
            s_substring_replacement,
            string.count(s_substring)
        )

    string

    string = html.unescape(string)

    return string

def as_localized_entry(key, translation):
    return "\"{}\" = \"{}\";".format(key.replace("(pluralized)", ""), translation)

def save_strings(strings, language):
    file_path = prepare_path(language, False)
    if file_path:
        with open(file_path, "w") as output_file:
            output_file.write("/*\n * Generated by Logen v2\n")
            output_file.write(" */\n\n")

            for line in strings:
                output_file.write(line)
                output_file.write("\n")

    else:
        print("⚠️ Localization file not found - {} ⚠️".format(language))

def output_localized_plurals(value):
    return value.output()

def save_pluralized_strings(strings, language):
    file_path = prepare_path(language, True)
    mapped_values = map(lambda value: value.output(), list(strings))
    output = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
    {}
    </dict>
    </plist>""".format("\n".join(mapped_values))

    if file_path:
        with open(file_path, "w+") as output_file:
            output_file.write(output)

    else:
        print("⚠️ Output language file not found - {} ⚠️".format(language))

def prepare_path(language, isPluralizedFile):
    root_dir = os.path.abspath(os.curdir)
    path = "/{}/{}/{}/Localizable.{}".format(
        PROJECT_NAME,
        LOCALIZATION_PATH,
        "{}.lproj".format(language.lower()),
        "stringsdict" if isPluralizedFile else "strings"
    )
    print("ℹ️ Preparing localization file - {}".format(root_dir + path))
    if os.path.exists(root_dir + path):
        return root_dir + path
    else:
        return None

def print_success_message(languages):
    print("✅ Generated strings for {} language(s):".format(len(languages)))
    for language in languages:
        print("    - {}".format(language))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--last_column", required=True)
    parser.add_argument("--project", required=True)

    parser.add_argument("--token", required=False)
    parser.add_argument("--credentials", required=False)
    parser.add_argument("--first_row", required=False)
    parser.add_argument("--localization_path", required=False)
    arguments = parser.parse_args()

    global SPREADSHEET_ID
    global RANGE
    global PROJECT_NAME
    global TOKEN_FILE
    global CREDENTIALS_FILE
    global LOCALIZATION_PATH

    SPREADSHEET_ID = arguments.id
    PROJECT_NAME = arguments.project

    if arguments.first_row:
        RANGE = "'{}'!A{}:{}".format(
            arguments.sheet,
            arguments.first_row,
            arguments.last_column
        )
    else:
        RANGE = "'{}'!A1:{}".format(
            arguments.sheet,
            arguments.last_column
        )

    if arguments.token:
        TOKEN_FILE = arguments.token

    if arguments.credentials:
        CREDENTIALS_FILE = arguments.credentials

    if arguments.localization_path:
        LOCALIZATION_PATH = arguments.localization_path

# - Main

if __name__ == "__main__":
    parse_arguments()

    print("ℹ️ Generating localizations...")

    spreadsheet = authorize_and_get_spreadsheet()
    languages = get_languages(spreadsheet)
    for language in languages:
        strings, pluralizedStrings = generate_strings(spreadsheet, language)
        save_pluralized_strings(pluralizedStrings, language)
        save_strings(strings, language)

    print_success_message(languages)
    sys.exit(0)