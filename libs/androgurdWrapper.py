import androguard.core.bytecodes.apk as apk
import androguard.core.bytecodes.dvm as dvm
import logging
logging.getLogger("androguard").setLevel(logging.CRITICAL)


def appinfo(apkfile):
    a = apk.APK(apkfile)
    d = dvm.DalvikVMFormat(a.get_dex())
    return {
        'package': a.get_package(),
        'version': a.get_androidversion_code(),
        'permissions': a.get_permissions(),
        'activities': a.get_activities(),
        'services': a.get_services(),
        'receivers': a.get_receivers(),
        'providers': a.get_providers(),
        'strings': d.get_strings()
    }



