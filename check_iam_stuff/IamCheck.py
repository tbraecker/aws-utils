""""Query AWS IAM to check some stuff like access keys, password etc"""

import lib.CredentialReport as Cr
import lib.PasswordCheck as Pc
import lib.AccessKeyCheck as Ac
import lib.DeadUsersCheck as Dc
import lib.MfaCheck as Mfa
import lib.EmptyGroupsCheck as Eg
import os
import shutil

__author__ = 'Tobias Braecker'
__version__ = '1.0'


class IamChecks:
    def main(self):
        period = 30
        path = os.getcwd() + '/files'

        cred = Cr.CredentialReport(path)
        pass_check = Pc.PasswordCheck(period, path)
        access_key_check = Ac.AccessKeyCheck(period, path)
        dead_users_check = Dc.DeadUsersCheck(path)
        mfa_check = Mfa.MfaCheck(path)
        empty_groups_check = Eg.EmptyGroupsCheck(path)

        if not os.path.exists(path):
            os.makedirs(path)

        cred.generate()
        cred.get()

        pass_list = pass_check.last_used()
        pass_check.out(pass_list)

        access_list = access_key_check.last_used()
        access_key_check.out(access_list)

        dead_list = dead_users_check.find()
        dead_users_check.out(dead_list)

        mfa_list = mfa_check.find_mfa()
        group_list = mfa_check.get_admin(mfa_list)
        mfa_check.out(group_list)

        group_list, user_groups_list = empty_groups_check.get_lists()
        dead_groups_list = \
            empty_groups_check.find(group_list,user_groups_list)
        empty_groups_check.out(dead_groups_list)

        shutil.rmtree(path)


if __name__ == '__main__':
    ic = IamChecks()
    ic.main()
