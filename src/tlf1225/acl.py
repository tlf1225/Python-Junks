from sys import argv

from win32api import GetLastError
from win32security import ACL_REVISION_DS, CONTAINER_INHERIT_ACE, OBJECT_INHERIT_ACE, SYSTEM_MANDATORY_LABEL_NO_READ_UP, \
    SYSTEM_MANDATORY_LABEL_NO_WRITE_UP, SYSTEM_MANDATORY_LABEL_NO_EXECUTE_UP, SE_FILE_OBJECT, LABEL_SECURITY_INFORMATION, \
    GetNamedSecurityInfo, SetNamedSecurityInfo, CreateWellKnownSid, WinMediumLabelSid, ACL

if __name__ == '__main__':
    target = argv[1] if len(argv) > 1 else None
    if not target:
        exit(1)

    handle = GetNamedSecurityInfo(target, SE_FILE_OBJECT, LABEL_SECURITY_INFORMATION)
    print(GetLastError())
    well = CreateWellKnownSid(WinMediumLabelSid)
    acl = handle.GetSecurityDescriptorSacl()
    if not acl:
        acl = ACL()
        acl.Initialize()

    if acl.GetAceCount():
        acl.DeleteAce(0)

    acl.AddMandatoryAce(ACL_REVISION_DS, OBJECT_INHERIT_ACE | CONTAINER_INHERIT_ACE,
                        SYSTEM_MANDATORY_LABEL_NO_READ_UP | SYSTEM_MANDATORY_LABEL_NO_WRITE_UP | SYSTEM_MANDATORY_LABEL_NO_EXECUTE_UP, well)

    # for a in range(acl.GetAceCount()):
    #     ace = acl.GetAce(a)
    #     for b in range(ace[2].GetSubAuthorityCount()):
    #         sub_a = ace[2].GetSubAuthority(b)
    #         print(f"Limit: {ace[1]} SID:{sub_a}")

    SetNamedSecurityInfo(target, SE_FILE_OBJECT, LABEL_SECURITY_INFORMATION, None, None, None, acl)
    print(GetLastError())

    # sleep(5)
    # acl.DeleteAce(0)
    # SetNamedSecurityInfo(target, SE_FILE_OBJECT, LABEL_SECURITY_INFORMATION, None, None, None, acl)
    # print(GetLastError())
