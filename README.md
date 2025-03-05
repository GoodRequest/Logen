<a href="https://www.goodrequest.com/">
    <img src="https://global-uploads.webflow.com/5dca73a3dff894e401b4d7c0/5ed9fa51800a236c9261b703_GR_new%20logos-02.svg" alt="" class="gr-logo" align="right">
</a>

# LOGEN (**Lo**calization **Gen**erator)

![Version](https://img.shields.io/badge/latest_version-2.3.0-blueviolet)
[![Python Version](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/downloads/release/python-390/)
![Swift Version](https://img.shields.io/badge/swift-6-yellow)
![SPM](https://img.shields.io/badge/SwiftPM-supported-green)
![Hotel](https://img.shields.io/badge/Hotel%3F-Trivago-orange)

# Logen setup

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
- Give it a name (eg. "Logen")
- and "Finish"

Select the target you just created and switch to "Build Phases" tab.

- Click `+` in the top left corner
- Select "New Run Script Phase"
- (not required) Rename the build phase to something more descriptive

Copy and paste this script. Feel free to modify or add parameters as needed. Refer to the table below.

```
SCRIPT_PATH="${BUILD_DIR%/Build/*}/SourcePackages/checkouts/Logen/logen2.py"
CREDS="${BUILD_DIR%/Build/*}/SourcePackages/checkouts/Logen/credentials.json"
TOKEN="${PROJECT_DIR}/logen2_token.json"

GOOGLE_SHEETS_ID="<SHEET_ID_HERE>"
SHEET="<SHEET_NAME_HERE>"
FIRST_ROW="1"
LAST_COLUMN="E"

if test -f "${SCRIPT_PATH}"; then
    python3 "${SCRIPT_PATH}" \
    --id "${GOOGLE_SHEETS_ID}" \
    --sheet "${SHEET}" \
    --first_row "${FIRST_ROW}" \
    --last_column "${LAST_COLUMN}" \
    --project "${PROJECT_NAME}" \
    --credentials "${CREDS}" \
    --token "${TOKEN}"
else
    echo "warning: Script not found"
fi
```

| Parameters | Required | Description |
| --- | --- | --- |
| --id | yes | Spreadsheet identifier. You can find it inside a link from your browser, when you open google spreadsheets (for example, if your link is https://docs.google.com/spreadsheets/d/ASDFGHJKL/edit#gid=0, the identifier is ASDFGHJKL). |
| --sheet | yes | Name of the sheet in spreadsheet. You can find it in the bottom left. |
| --last_column | yes | Last column in the sheet that contains data. For example if your spreadsheet has 7 columns, the last one is marked G. |
| --project | yes | Name of the project, and the root source files directory. Recommended value is "${PROJECT_NAME}" (Xcode build variable). |
| --token | no | Credentials authorizing the user to use google's API. Recommended value is "${PROJECT_DIR}/logen2_token.json", or anywhere else in the user's computer. This token must not be commited to source control and must be excluded (eg. by an entry in .gitignore file). |
| --credentials | no | Credentials authorizing the app to use google's API. Recommended value is the location of credentials.json in build directory. "${BUILD_DIR%/Build/*}/SourcePackages/checkouts/logen_ios/credentials.json"Default value points to credentials.json file in the same directory where the script is invoked from. |
| --first_row | no | First row of the spreadsheet. This is an optional argument (default value is 1) in case you need to skip the first couple of rows. |
| --localization_path | no | Path inside the project directory, where the final localization files should be exported into. Does not start nor end with a slash. Does not specify the localization language. Default value: Resources/Localization. |
| --filename | no | Filename of the default .strings file. This option doesn't include pluralized strings. This option also only applies to localization entries that have no explicit export path set in their localization key. |

Generate your token file:

- Run the target!
- Your web browser should open. Log in with your google account ending in `@goodrequest.com`. It's best to have your password already saved in the browser/keychain, since the timeout is rather short.
- Give Logen 2 access to spreadsheets API
- In case the browser gets stuck on loading, hit *Cmd+R* to refresh the website (but it shouldn't really happen)
- You should get redirected to a success screen
1. Add the token file to `.gitignore`
2. Enjoy your localizations!

# Spreadsheet setup

There isn't much to set up in the spreadsheets. They should follow this general formatting:

| Description | 1234 iOS ASDF | Android | SK | EN |
| --- | --- | --- | --- | --- |
| Any | Title of this column | This is | Preklad 1 | Translation 1 |
| description | should contain | not really | Preklad 2 | Translation 2 |
| you | the word "iOS" | supported | Preklad 3 | Translation 3 |
| want | somewhere | in this tool | Preklad 4 | ... |

It's important to note that the language column must be exactly 2 letters long and reflect the language code that will be used in the project.

## Parametrized localizations

### Valid parameters

Logen does not transform localization entries. Feel free to complement Logen with SwiftGen
or another similar tool that supports string formats.

Here is a list of format specifiers from Apple's documentation (for reference):
[String Format Specifiers](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Strings/Articles/formatSpecifiers.html)

### Examples

| Identifier iOS | CS |
| --- | --- |
| test.number.threehundred | Tři sta třicet tři |
| test.variable.injections | %s stříbrných stříkaček |
| test.shoot | stříká |
| test.over |  přes |
| test.variable.rooftops | %d stříbrných střech. |

```swift
let injectionCount = L.Test.Number.threehundred
let roofCount = 333
let string1 = L.Test.Variable.injections(injectionCount)
let string2 = L.Test.Variable.rooftops(roofCount)
```

## Pluralized localizations

To inform Logen that this localization should be treated as pluralized you will need to include (pluralized) tag somewhere in localization key - eg. `ios.pluralized_string(pluralized)`.

### Variable naming

Every variable in a pluralized string must be numbered - refer to C-style string formatting:

```
%1$d is string with only one variable.
```

```
%1$d is string with %2$d variables.
```

### Pluralized tags options

Logen generates an entry in .stringsdict file for every plural category, for each variable, defined in the localization entry.

Supported plural categories depend on language of the entry. Please refer to [Unicode CLDR language rules](https://cldr.unicode.org/index/cldr-spec/plural-rules) documentation, where every language is specified.

Apple's documentation: [Localizing strings that contain plurals](https://developer.apple.com/documentation/xcode/localizing-strings-that-contain-plurals)

### Examples

| Identifier iOS | CS |
| --- | --- |
| test.variable.parameter | %s string |
| test.pluralized.pluralString(pluralized) | `%1$d<one> den</one><few> dní</few><other> dnů</other>` |
| test.pluralized.multiplePluralString(pluralized) | `%1$@ GB, %2$@. zóna, zbývá %3$d<one> den</one><few> dní</few><other> dnů</other>` |
| test.pluralized.multipleMorePluralString(pluralized) | `%1$d<one> den</one><few> dní</few><other> dnů</other>, %2$@. zóna, zbývá %3$d<one> den</one><few> dní</few><other> dnů</other>` |
| test.pluralized.multiplePluralTagOnly(pluralized) | `%@ GB, %@. zóna, zbývá %d<one> den</one><few> dní</few><other> dnů</other>` |
| test.pluralized.multiplePluralStringReverseOrder(pluralized) | `%1$@ GB, %2$@. zóna, zbývá %3$d<one> den</one><few> dní</few><other> dnů</other>` |

## Localizing different files

You can use Logen to generate localizations for other files that need to be localized. To generate .strings file with a custom name, include the name it parentheses in the localization key.

### Examples

| Identifier iOS | CS |
| --- | --- |
| NSCameraUsageDescription(InfoPlist) | Dej foťák vole |
| CFBundleDisplayName(InfoPlist) | Moje aplikace |

![Slovak parrot](https://cultofthepartyparrot.com/flags/hd/slovakiaparrot.gif)
![USA parrot](https://cultofthepartyparrot.com/flags/hd/unitedstatesofamericaparrot.gif)
![Deutscher papagei](https://cultofthepartyparrot.com/flags/hd/germanyparrot.gif)
![Spain parrot](https://cultofthepartyparrot.com/flags/hd/spainparrot.gif)