import os

TEST = "test"
REFRESH_PROFILES = "refresh_zosmf_profiles"
CREATE_PROFILE = "create_zosmf_profile"
DELETE_PROFILE = "delete_zosmf_profile"
UPDATE_PROFILE = "update_zosmf_profile"
SET_DEFAULT_PROFILE = "set_default_zosmf_profile"
LIST_DATASET = "list_dataset"

Application_Title = "ZOWE Profiles Manager"
Create_Profile_Title = "Create ZOWE {0} Profile"
Edit_Profile_Title = "Edit ZOWE {0} Profile"
Edit_Profiles_Title = "Edit ZOWE {0} Profiles Credentials"
Overwrite_Profile_Template = "Profile \"{0}\" already exist. Do you want to overwrite it?"

About_Rich_Text = "<html><head/><body><p align=\"center\">Zowe profiles manager.</p>" \
                  "<p align=\"center\">Specially for <a href=\"http://www.broadcom.com\">Broadcom</a> " \
                  "<a href=\"http://www.zowe.org\">ZOWE</a> hackaton.</p>" \
                  "<p align=\"center\">Aleksandr Sokolov</p></body></html>"

Whats_Profile_Name = "Specifies the name of the new tso profile" \
                     "\nYou can load this profile by using the name on commands that support " \
                     "the \"--tso-profile\" option"
Whats_Set_Default = "Set a profile the default one after creation"
Whats_Account = "Your z/OS TSO/E accounting information"
Whats_Char_Set = "Character set for address space to convert messages and responses from UTF-8 to EBCDIC" \
                 "\nDefault value: 697"
Whats_Code_Page = "Codepage value for TSO/E address space to convert messages and responses from UTF-8 to EBCDIC" \
                  "\nDefault value: 1047"
Whats_Region_Size = "Region size for the TSO/E address space" \
                    "\nDefault value: 4096"
Whats_Logon_Proc = "The logon procedure to use when creating TSO procedures on your behalf" \
                   "\nDefault value: IZUFPROC"
Whats_Rows = "The number of rows on a screen" \
             "\nDefault value: 24"
Whats_Columns = "The number of columns on a screen" \
                "\nDefault value: 80"

char_set_help_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "help", "char_set_help.html")
with open(char_set_help_file) as fd:
    Whats_Char_Set_Full = fd.read()
