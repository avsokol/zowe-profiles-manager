import json
import os
from subprocess import Popen, PIPE
import sys
import re
from lib.exceptions.no_zowe_profiles_found_exception import NoZoweProfilesFoundException
from lib.exceptions.unknown_command_exception import UnknownCommandException
from inc.constants import TEST, REFRESH_PROFILES, CREATE_PROFILE, DELETE_PROFILE, SET_DEFAULT_PROFILE, LIST_DATASET, \
    UPDATE_PROFILE
from lib.exceptions.unsupported_platform_exception import UnsupportedPlatformException
from lib.exceptions.zoe_cmd_fail_exception import ZoweCmdFailException

TYPE_ZOSMF = "zosmf"
TYPE_SSH = "ssh"
TYPE_TSO = "tso"
SSH_PORT = 22

ZOWE_COMMAND = {
    TEST: "zowe",
    REFRESH_PROFILES: "zowe\tprofiles\tlist\t{0}",
    CREATE_PROFILE: "zowe\tprofiles\tcreate\t{0}\t{1}\t--host\t{2}\t--port\t{3}"
                    "\t--user\t{4}\t--password\t{5}",
    DELETE_PROFILE: "zowe\tprofiles\tdelete\t{0}\t{1}",
    UPDATE_PROFILE: "zowe\tprofiles\tupdate\t{0}\t{1}",
    SET_DEFAULT_PROFILE: "zowe\tprofiles\tset-default\t{0}\t{1}",
    LIST_DATASET: "zowe\tzos-files\tlist\tdata-set\t{0}\t--zosmf-profile\t{1}",
}

ZOWE_TSO_COMMAND = {
    CREATE_PROFILE: "zowe\tprofiles\tcreate\t{0}\t{1}\t--account\t{2}\t--region-size\t{3}\t--logon-procedure\t{4}"
                    "\t--code-page\t{5}\t--character-set\t{6}\t--rows\t{7}\t--columns\t{8}",
    UPDATE_PROFILE: "zowe\tprofiles\tupdate\t{0}\t{1}"
}

ZOWE_RESPONSES = {
    CREATE_PROFILE: "Profile created successfully!",
    UPDATE_PROFILE: "Profile created successfully!",
    DELETE_PROFILE: "Profile \"{1}\" of type \"{0}\" successfully deleted.",
    SET_DEFAULT_PROFILE: "The default profile for {0} set to {1}"
}

ZOWE_ERROR_RESPONSES = {
    CREATE_PROFILE: "Profile \"{1}\" of type \"{0}\" already exists and overwrite was NOT specified.",
    UPDATE_PROFILE: "Profile \"{1}\" of type \"{0}\" does not exist.",
    DELETE_PROFILE: "Profile \"{1}\" of type \"{0}\" does not exist."
}


def get_login_name(upper=True):
    platform = sys.platform
    if platform in ["windows", "win32"]:
        key = "USERNAME"

    elif platform == "linux":
        key = "LOGNAME"

    else:
        raise UnsupportedPlatformException("Unsupported platform '{0}'".format(platform))

    login = os.environ[key]
    if upper:
        login = login.upper()

    return login


def tune_zowe_cmd_for_platform(cmd):
    platform = sys.platform
    if platform in ["windows", "win32"]:
        cmd[0] = cmd[0] + ".cmd"

    return cmd


def get_zowe_test_cmd():
    cmd = ZOWE_COMMAND[TEST].split("\t")
    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_refresh_profiles_cmd(profile_type, show_contents=None):
    if show_contents is None:
        show_contents = False

    cmd = ZOWE_COMMAND[REFRESH_PROFILES].format(profile_type).split("\t")
    if show_contents:
        cmd.append("--response-format-json")
    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_create_profile(profile_type, profile_name, host, port, username, password,
                            reject_unauthorised=None, overwrite=None):
    if reject_unauthorised is None:
        reject_unauthorised = True

    if overwrite is None:
        overwrite = False

    cmd = ZOWE_COMMAND[CREATE_PROFILE].format(
        profile_type, profile_name, host, port, username, password
    ).split("\t")

    if profile_type == TYPE_ZOSMF:
        reject_unauthorised = str(reject_unauthorised).lower()
        cmd.append("--reject-unauthorized")
        cmd.append(reject_unauthorised)

    if overwrite:
        cmd.append("--overwrite")

    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_delete_profile_cmd(profile_type, profile_name):
    cmd = ZOWE_COMMAND[DELETE_PROFILE].format(profile_type, profile_name).split("\t")
    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_update_profile_cmd(profile_type, profile_name,
                                host=None, port=None, username=None, password=None, reject_unauthorised=None):
    cmd = ZOWE_COMMAND[UPDATE_PROFILE].format(profile_type, profile_name).split("\t")

    if host is not None:
        cmd.append("--host")
        cmd.append(host)

    if profile_type != TYPE_SSH:
        if port is not None:
            cmd.append("--port")
            cmd.append(port)

    if username is not None:
        cmd.append("--user")
        cmd.append(username)

    if password is not None:
        cmd.append("--password")
        cmd.append(password)

    if profile_type != TYPE_SSH:
        if reject_unauthorised is not None:
            reject_unauthorised = str(reject_unauthorised).lower()
            cmd.append("--reject-unauthorized")
            cmd.append(reject_unauthorised)

    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_set_default_profile_cmd(profile_type, profile_name):
    cmd = ZOWE_COMMAND[SET_DEFAULT_PROFILE].format(profile_type, profile_name).split("\t")
    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_list_dataset_cmd(profile_name, dataset):
    cmd = ZOWE_COMMAND[LIST_DATASET].format(dataset, profile_name).split("\t")
    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_default_profile(profile_type):
    result, zowe_profiles = execute_zowe_command(REFRESH_PROFILES, profile_type=profile_type)
    for zowe_profile in zowe_profiles.split("\n"):
        if re.search("^.*\(default\)$", zowe_profile):
            zowe_profile = re.sub(" \(default\)$", "", zowe_profile)
            return zowe_profile

    raise NoZoweProfilesFoundException


def execute_zowe_command(command, **kwargs):
    all_params = [
        "profile_type",
        "profile_name",
        "host",
        "port",
        "username",
        "password",
        "reject_unauthorised",
        "show_contents",
        "overwrite",
        "dataset",
        "account",
        "regionSize",
        "logonProcedure",
        "codePage",
        "characterSet",
        "rows",
        "columns"
    ]

    params = dict()
    for param in all_params:
        params[param] = None
        if param in kwargs:
            params[param] = kwargs[param]

    if command == TEST:
        cmd = get_zowe_test_cmd()

    elif command == REFRESH_PROFILES:
        cmd = get_zowe_refresh_profiles_cmd(params["profile_type"], show_contents=params["show_contents"])

    elif command == CREATE_PROFILE:
        if params["profile_type"] != TYPE_TSO:
            cmd = get_zowe_create_profile(
                params["profile_type"],
                params["profile_name"],
                params["host"],
                params["port"],
                params["username"],
                params["password"],
                params["reject_unauthorised"],
                params["overwrite"]
            )

        else:
            cmd = get_zowe_create_tso_profile(
                params["profile_type"],
                params["profile_name"],
                account=params["account"],
                region_size=params["regionSize"],
                logon_procedure=params["logonProcedure"],
                code_page=params["codePage"],
                character_set=params["characterSet"],
                rows=params["rows"],
                columns=params["columns"],
                overwrite=params["overwrite"]
            )

    elif command == DELETE_PROFILE:
        cmd = get_zowe_delete_profile_cmd(params["profile_type"], params["profile_name"])

    elif command == UPDATE_PROFILE:
        if params["profile_type"] != TYPE_TSO:
            cmd = get_zowe_update_profile_cmd(
                params["profile_type"],
                params["profile_name"],
                host=params["host"],
                port=params["port"],
                username=params["username"],
                password=params["password"],
                reject_unauthorised=params["reject_unauthorised"]
            )

        else:
            cmd = get_zowe_update_tso_profile_cmd(
                params["profile_type"],
                params["profile_name"],
                account=params["account"],
                region_size=params["regionSize"],
                logon_procedure=params["logonProcedure"],
                code_page=params["codePage"],
                character_set=params["characterSet"],
                rows=params["rows"],
                columns=params["columns"],
                overwrite=params["overwrite"]
            )

    elif command == SET_DEFAULT_PROFILE:
        cmd = get_zowe_set_default_profile_cmd(params["profile_type"], params["profile_name"])

    elif command == LIST_DATASET:
        cmd = get_zowe_list_dataset_cmd(params["profile_name"], params["dataset"])

    else:
        raise UnknownCommandException

    # For DEBUG ONLY!
    # print("cmd", cmd)

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)

    return_code = proc.wait()
    if return_code == 0:
        output = proc.stdout.read()
        output = output.strip()
        output = output.decode("UTF-8")

    else:
        output = proc.stdout.read()
        output = output.strip()
        output = output.decode("UTF-8")
        err_output = proc.stderr.read()
        err_output = err_output.strip()
        err_output = err_output.decode("UTF-8")
        raise ZoweCmdFailException("Failure %s:\n'%s'\n'%s'" % (return_code, output, err_output))

    return return_code, output


def get_profiles_from_content(content):
    cnt_profiles = dict()

    json_struct = json.loads(content)
    data = json_struct["data"]

    def_profile = None

    for element in data:

        profile_line = element["message"]

        res = re.match("Profile (\".*\") of type.*$", profile_line)
        profile_name = res.groups()[0].strip('"')

        cnt_profiles[profile_name] = element["profile"]

        if profile_name != element["name"]:
            def_profile = profile_name

    return cnt_profiles, def_profile


def get_zowe_create_tso_profile(profile_type, profile_name,
                                account=None, region_size=None, logon_procedure=None,
                                code_page=None, character_set=None,
                                rows=None, columns=None, overwrite=None):

    if overwrite is None:
        overwrite = False

    cmd = ZOWE_TSO_COMMAND[CREATE_PROFILE].format(
        profile_type,
        profile_name,
        account,
        str(region_size),
        logon_procedure,
        str(code_page),
        str(character_set),
        str(rows),
        str(columns)
    ).split("\t")

    if overwrite:
        cmd.append("--overwrite")

    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def get_zowe_update_tso_profile_cmd(profile_type, profile_name,
                                    account=None, region_size=None, logon_procedure=None,
                                    code_page=None, character_set=None,
                                    rows=None, columns=None, overwrite=None):

    if overwrite is None:
        overwrite = False

    cmd = ZOWE_TSO_COMMAND[UPDATE_PROFILE].format(profile_type, profile_name).split("\t")

    if account is not None:
        cmd.append("--account")
        cmd.append(account)

    if region_size is not None:
        cmd.append("--region-size")
        cmd.append(str(region_size))

    if logon_procedure is not None:
        cmd.append("--logon-procedure")
        cmd.append(logon_procedure)

    if code_page is not None:
        cmd.append("--code-page")
        cmd.append(str(code_page))

    if character_set is not None:
        cmd.append("--character-set")
        cmd.append(str(character_set))

    if rows is not None:
        cmd.append("--rows")
        cmd.append(str(rows))

    if columns is not None:
        cmd.append("--columns")
        cmd.append(str(columns))

    if overwrite:
        cmd.append("--overwrite")

    cmd = tune_zowe_cmd_for_platform(cmd)
    return cmd


def test1():
    return execute_zowe_command(REFRESH_PROFILES, profile_type=TYPE_ZOSMF)


def test2():
    zowe_profile = get_zowe_default_profile(TYPE_ZOSMF)
    login = get_login_name()
    return execute_zowe_command(LIST_DATASET, profile_name=zowe_profile, dataset=login)


def test3():
    res, output = execute_zowe_command(REFRESH_PROFILES, profile_type=TYPE_SSH, show_contents=True)
    return get_profiles_from_content(output)


if __name__ == "__main__":
    code, out = test1()
    print("Result: '{0}'".format(code))
    print("Output: '{0}', '{1}'".format(out, type(out)))

    code, out = test2()
    print("Result: '{0}'".format(code))
    print("Output:\n'{0}'\n\n'{1}'".format(out, type(out)))

    profiles, default_profile = test3()
    print("Found profiles: '{0}'".format(profiles))
    print("Default profile: '{0}'".format(default_profile))
