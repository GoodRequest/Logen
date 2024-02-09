<a href="https://www.goodrequest.com/">
    <img src="https://global-uploads.webflow.com/5dca73a3dff894e401b4d7c0/5ed9fa51800a236c9261b703_GR_new%20logos-02.svg" alt="" class="gr-logo" align="right">
</a>

# LOGEN (**Lo**calization **Gen**erator)

![Version](https://img.shields.io/badge/latest_version-2.0.3-blueviolet)
[![Python Version](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/downloads/release/python-390/)
![Swift Version](https://img.shields.io/badge/swift-5+-yellow)
![SPM](https://img.shields.io/badge/SwiftPM-supported-green)
![Hotel](https://img.shields.io/badge/Hotel%3F-Trivago-orange)

# How to set up

## Python

First of all you need to install `python 3.9` on your machine:

Recommended way of installing python on macOS is via *Homebrew Package Manager*. You can grab Homebrew from the official website:

```
https://brew.sh
```

Use Homebrew to download the latest Python 3 version using the following command:

```
brew install python
```

Check if Python is available and installed correctly. You should see a path to the Python binary in your system.

```
which python3
```

Check if you have `pip` python package manager installed. The path should lead to the same directory as the command above.

```
which pip3
```

---

## Xcode integration

Add Logen to your [Swift Build Tools' `Package.swift`](https://github.com/GoodRequest/Logen/blob/main/res/BuildToolsTutorial.md) via SwiftPM.

```
.package(url: "git@bitbucket.org:GoodRequest/logen_ios.git", .upToNextMajor(from: "2.0.0"))
```

Hit *Cmd+S* and you should see Xcode starting to fetch the package for you. Wait until all package dependencies are resolved.

Open project settings and create a new build target

- Click `+` in the bottom left corner
- Open tab "Other"
- Select "Aggregate"
- Give it a name (eg. "Logen 2")
- and "Finish"

Select the target you just created and switch to "Build Phases" tab.

- Click `+` in the top left corner
- Select "New Run Script Phase"
- (not required) Rename the build phase to something more descriptive

Copy and paste this script (also remove two wild `#`, those are there only to prevent Bitbucket from obliterating the formatting of this readme):

```
SCRIPT_PATH="${BUILD_DIR%/Build/*}/SourcePackages/checkouts/Logen/logen2.py"
CREDS="${BUILD_DIR%/Build/*}/SourcePackages/checkouts/Logen/credentials.json"
TOKEN="${PROJECT_DIR}/logen2_token.json"#
GOOGLE_SHEETS_ID="SHEET ID HERE"
SHEET="SHEET NAME HERE"
FIRST_ROW="1"
LAST_COLUMN="E"#if test -f "${SCRIPT_PATH}"; then
    python3 "${SCRIPT_PATH}" --id "${GOOGLE_SHEETS_ID}" --sheet "${SHEET}" --first_row "${FIRST_ROW}" --last_column "${LAST_COLUMN}" --project "${PROJECT_NAME}" --credentials "${CREDS}" --token "${TOKEN}"else
    echo "warning: Script not found, add it from https://github.org/GoodRequest/logen_ios/ 😭😩🤦‍♂️"fi
```

| Parameters | Required | Description |
| --- | --- | --- |
| --id | yes | Spreadsheet identifier. You can find it inside a link from your browser, when you open google spreadsheets (for example, if your link is https://docs.google.com/spreadsheets/d/ASDFGHJKL/edit#gid=0, the identifier is ASDFGHJKL). |
| --project | yes | Project name. Recommended value is "${PROJECT_NAME}" (Xcode build variable). |
| --sheet | yes | Name of the sheet in spreadsheet. You can find it in the bottom left. |
| --first_row | no | First row of the spreadsheet. This is an optional argument (with a default value of 1) in case you need to skip the first couple of rows. |
| --last_column | yes | Last column in the sheet that contains data. For example if your spreadsheet has 7 columns, the last one is marked G.P.S. if you need explaining what sheets and ranges are, you should probably take an Excel course |
| --credentials | no | Credentials authorizing the app to use google's API. Recommended value is the location of credentials.json in build directory. "${BUILD_DIR%/Build/*}/SourcePackages/checkouts/logen_ios/credentials.json"Default value points to credentials.json file in the same directory where the script is invoked from. |
| --token | no | Credentials authorizing the user to use google's API. Recommended value is "${PROJECT_DIR}/logen2_token.json", or anywhere else in the user's computer. This token should not be pushed to git. |
| --localization_path | no | Path inside the project directory, where the final localization files should be exported into. Does not start nor end with a slash. Does not specify the localization language. Default value: Resources/Localization. |

Generate your token file:

- Run the target!
- Your web browser should open. Log in with your google account ending in `@goodrequest.com`. It's best to have your password already saved in the browser/keychain, since the timeout is rather short.
- Give Logen 2 access to spreadsheets API
- In case the browser gets stuck on loading, hit *Cmd+R* to refresh the website (but it shouldn't really happen)
- You should get redirected to a success screen
1. Add the token file to `.gitignore`
2. Enjoy your localizations!

![Slovak parrot](https://cultofthepartyparrot.com/flags/hd/slovakiaparrot.gif)
![USA parrot](https://cultofthepartyparrot.com/flags/hd/unitedstatesofamericaparrot.gif)
![Deutscher papagei](https://cultofthepartyparrot.com/flags/hd/germanyparrot.gif)
![Spain parrot](https://cultofthepartyparrot.com/flags/hd/spainparrot.gif)

# How to use

## Spreadsheet setup

There isn't much to set up in the spreadsheets. They should follow this general formatting:

| Description | 1234 iOS ASDF | Android | SK | EN |
| --- | --- | --- | --- | --- |
| Any | Title of this column | This should | Preklad 1 | Translation 1 |
| description | should contain | burn in hell | Preklad 2 | Translation 2 |
| you | the word "iOS" |  | Preklad 3 | Translation 3 |
| want | somewhere |  | Preklad 4 | ... |

It's important to note that the language column should be exactly 2 letters long and reflect the same language code that's used in the project.

## Localizations with parameter

### Valid parameters

[String Format Specifiers](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Strings/Articles/formatSpecifiers.html)

### Examples

## Pluralized localizations

To inform Logen that this localization should be treated as pluralized you will need to include (pluralized) tag somewhere in localization id. Example: ios.pluralized_string(pluralized)

### Plularized tags options

[Localizing strings that contain plurals | Apple Developer Documentation](https://developer.apple.com/documentation/xcode/localizing-strings-that-contain-plurals)

### Examples

| Location | Identifier iOS | CS |
| --- | --- | --- |
|  | test.pluralized.normalString | %s string |
|  | test.pluralized.pluralString(pluralized) | %1$d<one> den</one><few> dní</few><other> dnů</other> |
|  | test.pluralized.multiplePluralString(pluralized) | %1$@ GB, %2$@. zóna, zbývá %3$d<one> den</one><few> dní</few><other> dnů</other> |
|  | test.pluralized.multipleMorePluralString(pluralized) | %1$d<one> den</one><few> dní</few><other> dnů</other>, %2$@. zóna, zbývá %3$d<one> den</one><few> dní</few><other> dnů</other> |
|  | test.pluralized.multiplePluralTagOnly(pluralized) | %@ GB, %@. zóna, zbývá %d<one> den</one><few> dní</few><other> dnů</other> |
|  | test.pluralized.multiplePluralStringReverseOrder(pluralized) | %1$@ GB, %2$@. zóna, zbývá %3$d<one> den</one><few> dní</few><other> dnů</other> |

## Other Localized files

You can also use Logen to generate different files that you want to be localized. For example InfoPlist.stings, in this case all you need to do is to write Property List Key in Identifier iOS column and mark it with name of the file → in this case (InfoPlist)

### Examples

| Location | Identifier iOS | CS |
| --- | --- | --- |
|  | NSFaceIDUsageDescription(InfoPlist) | NSFaceIDUsageDescription CS |
|  | CFBundleDisplayName(InfoPlist) | CFBundleDisplayName CS |

# Code

## Variables

```python
SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
LOCALIZATION_PATH: str = "Resources/Localization"

SPREADSHEET_ID: str = None
RANGE: str = None
PROJECT_NAME: str = None
```

**`SCOPE`**:

- This variable holds the authentication scope required for accessing Google Sheets. It specifies that the script needs read-only access to Google Spreadsheets.

**`TOKEN_FILE`**:

- It stores the name of the file where the authentication token will be stored. This token is used for making authorized requests to the Google Sheets API.

**`CREDENTIALS_FILE`**:

- This variable holds the name of the file containing the client credentials. The script uses these credentials to authenticate with the Google Sheets API.

**`LOCALIZATION_PATH`**:

- Specifies the path where the generated localization files will be stored. It is set to "Resources/Localization" by default.

**`SPREADSHEET_ID`**:

- This variable will hold the unique identifier (ID) of the Google Sheets document from which the script will retrieve localization data. It is initially set to **`None`**.

**`RANGE`**:

- Represents the range of cells within the Google Sheet to be retrieved. It will be in the format "'SheetName'!A1:B10", where 'SheetName' is the name of the sheet, and A1:B10 is the range. Initially set to **`None`**.

**`PROJECT_NAME`**:

- Holds the name of the project for which localization is being generated. It is initially set to **`None`**.

These variables provide the script with the necessary information for authentication, data retrieval, and output location. The **`SPREADSHEET_ID`**, **`RANGE`**, and **`PROJECT_NAME`** are likely to be set during the execution of the script, potentially through command-line arguments or some other input mechanism.

## **Classes**

### **`Translation`**

 Represents a translation with a type and its corresponding value.

```python
class Translation:
    def __init__(self, type, translation):
        self.type = type
        self.translation = translation

    def output(self):
        return """<key>{}</key>
        <string>{}</string>""".format(self.type, self.translation)
```

### **`Variable`**

Represents a variable with a key and a list of translations.

```python
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
```

### **`LocalizedString`**

Represents a localized string with a key, a base string, and a list of variables.

```python
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
```

## Functions

### **`import_google_apis(firstAttempt)`**

This function imports the necessary modules for Google APIs. If an import error occurs, it attempts to install the required libraries using **`pip_install_google_apis`**.

- **Parameters:**
    - **`firstAttempt`** (bool): Indicates whether this is the first attempt to import Google APIs.

```python
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
            print("error: FAILED TO IMPORT GOOGLE APIS ❌")
            sys.exit(1)
```

### **`pip_install_google_apis()`**

This function installs or upgrades the required Google API libraries using **`pip`**.

```python
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
```

### **`authorize_and_get_spreadsheet()`**

This function handles the authentication process for the Google Sheets API and retrieves data from the specified spreadsheet.

- **Returns:**
    - List of lists representing the values from the spreadsheet.

```python
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
            print("error: NO DATA FOUND IN RANGE IN SPREADSHEET ❌")
            exit()

        return values

    except HttpError as error:
        print("error: ", error, "❌")
        exit()
```

### **`get_languages(spreadsheet)`**

This function extracts language headers from the spreadsheet.

- **Parameters:**
    - **`spreadsheet`** (list of lists): The data retrieved from the spreadsheet.
- **Returns:**
    - List of language headers.

```python
def get_languages(spreadsheet):
    headers = spreadsheet[0]
    languages = []
    for header in headers:
        if len(header) == 2:
            languages.append(header)

    return languages
```

### **`generate_strings(spreadsheet, language)`**

Generates localized strings for the specified language based on the spreadsheet data.

- **Parameters:**
    - **`spreadsheet`** (list of lists): The data retrieved from the spreadsheet.
    - **`language`** (str): The language for which to generate localized strings.
- **Returns:**
    - Tuple containing a list of simple localized strings and a list of pluralized localized strings.

```python
def generate_strings(spreadsheet, language):
    ios_column_name = "iOS"
    ios_column_first_match = [header for header in spreadsheet[0] if ios_column_name in header][0]
    ios_column_index = spreadsheet[0].index(ios_column_first_match)

    language_column_index = spreadsheet[0].index(language)

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
```

### **`generate_special_strings(spreadsheet, language)`**

Generates localized strings for the specified language based on the spreadsheet data.

- **Parameters:**
    - **`spreadsheet`** (list of lists): The data retrieved from the spreadsheet.
    - **`language`** (str): The language for which to generate localized strings.
- **Returns:**
    - Dictionary containing a file_name as key and a list of simple localized strings as values

```python
def generate_special_strings(spreadsheet, language):
    ios_column_name = "iOS"
    ios_column_first_match = [header for header in spreadsheet[0] if ios_column_name in header][0]
    ios_column_index = spreadsheet[0].index(ios_column_first_match)

    language_column_index = spreadsheet[0].index(language)

    dict_of_special_strings = dict()

    for row in spreadsheet:
        try:
            if not row[ios_column_index]:
                continue
            else:
                key = row[ios_column_index]
                if "(" in key and "(pluralized)" not in key:
                    file_name = key[key.find("(") + 1:key.find(")")]
                    translation = fix_special_substrings(row[language_column_index])
                    localized_entry = as_special_localized_entry(key, file_name, translation)

                    if file_name in dict_of_special_strings:
                        dict_of_special_strings.get(file_name).append(localized_entry)
                    else:
                        dict_of_special_strings.update({file_name : [localized_entry]})

        except IndexError:
            continue

    return dict_of_special_strings
```

### **`create_pluralized_file(rows, language_index, ios_column_index)`**

Creates localized strings for pluralized entries based on the provided rows.

- **Parameters:**
    - **`rows`** (list of lists): Rows containing pluralized entries.
    - **`language_index`** (int): Index of the language column.
    - **`ios_column_index`** (int): Index of the iOS column.
- **Returns:**
    - List of **`LocalizedString`** objects representing pluralized entries.

```python
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
```

### **`separate_strings(input_string)`**

Splits a string into segments based on specified patterns.

- **Parameters:**
    - **`input_string`** (str): The input string to be split.
- **Returns:**
    - List of string segments.

```python
def separate_strings(input_string):
    # Define a regular expression pattern to capture substrings around '%[0-9]+\$@'
    pattern = r'([^%]*)(%[0-9]*\$*[@dDuUxXoOfeEgGcCsSpaAF][^%]*)'

    # Use re.split to split the input string around the specified pattern
    result = re.split(pattern, input_string)

    # Remove empty strings from the result
    result = [segment for segment in result if segment]

    return result
```

### **`extract_pluralized_translations(input_string)`**

Extracts translations from a pluralized string.

- **Parameters:**
    - **`input_string`** (str): Pluralized input string.
- **Returns:**
    - List of **`Translation`** objects representing pluralized translations.

```python
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
```

### **`fix_special_substrings(string)`**

Handles special substrings and escapes in a string.

- **Parameters:**
    - **`string`** (str): The input string to be processed.
- **Returns:**
    - Processed string.

```python
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

    string = html.unescape(string)

    return string
```

### **`as_localized_entry(key, translation)`**

Formats a localized entry for output.

- **Parameters:**
    - **`key`** (str): The key for the localized entry.
    - **`translation`** (str): The translation for the localized entry.
- **Returns:**
    - Formatted string representing the localized entry.

```python
def as_localized_entry(key, translation):
    return "\"{}\" = \"{}\";".format(key.replace("(pluralized)", ""), translation)
```

### **`as_special_localized_entry(key, file_name, translation)`**

Formats a localized entry for output.

- **Parameters:**
    - **`key`** (str): The key for the localized entry.
    - **`file_name`** (str): The name for the localized file.
    - **`translation`** (str): The translation for the localized entry.
- **Returns:**
    - Formatted string representing the localized entry.

```python
def as_special_localized_entry(key, file_name, translation):
    return "{} = \"{}\";".format(key.replace("({})".format(file_name), ""), translation)
```

### **`save_strings(strings, language)`**

Saves generated strings to a file.

- **Parameters:**
    - **`strings`** (list of str): List of simple localized strings.
    - **`language`** (str): The language for which to save the strings.

```python
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
```

### **`save_pluralized_strings(strings, language)`**

Saves generated pluralized strings to a file.

- **Parameters:**
    - **`strings`** (list of **`LocalizedString`**): List of pluralized localized strings.
    - **`language`** (str): The language for which to save the pluralized strings.

```python
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
```

### **`save_special_strings(strings, language)`**

Saves generated strings to a file.

- **Parameters:**
    - **`strings`** (list of str): Dictionary of files and localized strings.
    - **`language`** (str): The language for which to save the strings.

```python
def save_special_strings(strings, language):
    for file_name in strings: 
        file_path = prepare_path(language, False, file_name)
        if file_path:
            with open(file_path, "w") as output_file:
                output_file.write("/*\n * Generated by Logen v2\n")
                output_file.write(" */\n\n")

                for line in strings.get(file_name):
                    output_file.write(line)
                    output_file.write("\n")

        else:
            print("⚠️ Localization file not found - {} ⚠️".format(language))
```

### **`prepare_path(language, isPluralizedFile)`**

Prepares the path for saving localization files.

- **Parameters:**
    - **`language`** (str): The language for which to prepare the path.
    - **`isPluralizedFile`** (bool): Indicates whether the file is for pluralized strings.
- **Returns:**
    - Path for saving the localization file.

```python
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
```

### **`print_success_message(languages)`**

Prints a success message with the generated languages.

- **Parameters:**
    - **`languages`** (list of str): List of languages for which strings were generated.

```python
def print_success_message(languages):
    print("✅ Generated strings for {} language(s):".format(len(languages)))
    for language in languages:
        print("    - {}".format(language))
```

### **`parse_arguments()`**

Parses command-line arguments using the **`argparse`** module.

```python
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
```
