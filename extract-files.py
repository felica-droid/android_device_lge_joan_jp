#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/lib64/vendor.lge.hardware.nfc@1.0.so',
        'vendor/lib64/vendor.lge.hardware.nfc@1.1.so'
    ): blob_fixup()
        .binary_regex_replace(b'libhidltransport.so', b'libhidlbase_shim.so'),
    # felica_access.xml is the ACL the NFC service checks callers against.
    # extract_utils turns .xml into prebuilt_etc_xml, which runs xmllint, and
    # this file does not survive it: it uses android:signature and android:name
    # while declaring only xmlns:xliff, so the prefix is undefined. Declaring it
    # is enough - the file is data, and nothing reads the namespace back.
    'product/etc/felica_access.xml': blob_fixup()
        .regex_replace(
            r'<resources xmlns:xliff=',
            '<resources xmlns:android="http://schemas.android.com/apk/res/android" xmlns:xliff='),
    # MobileFeliCaClient reports a failure as a bare numeric FelicaException and
    # keeps its reasoning to itself: R8 emptied LogMgr's two sinks to
    # "return-void" before the apk shipped, so the several thousand call sites
    # that mark every branch it takes produce nothing. patches/MobileFeliCaClient
    # fills them back in against android.util.Log under the tag "MfcLog".
    #
    # This costs the apk FeliCa Networks' signature, which is the one
    # felica_access.xml names; it comes back platform-signed instead, and
    # NfceeAccessControl admits that.
    'product/priv-app/MobileFeliCaClient/MobileFeliCaClient.apk': blob_fixup()
        .apktool_patch('patches/MobileFeliCaClient'),
    'vendor/etc/init/vendor.lge.hardware.nfc@1.1-service.rc': blob_fixup()
        .regex_replace(
            "    interface android.hardware.nfc@1.1::INfc default",
            "    interface android.hardware.nfc@1.0::INfc default\n    interface android.hardware.nfc@1.1::INfc default"
        ),
}  # fmt: skip

module = ExtractUtilsModule(
    'l01k',
    'lge',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'joan-common', module.vendor)
    utils.run()
