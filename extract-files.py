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
    'vendor/etc/init/vendor.lge.hardware.nfc@1.1-service.rc': blob_fixup()
        .regex_replace(
            "    interface android.hardware.nfc@1.1::INfc default",
            "    interface android.hardware.nfc@1.0::INfc default\n    interface android.hardware.nfc@1.1::INfc default"
        ),
}  # fmt: skip

module = ExtractUtilsModule(
    'joan_jp',
    'lge',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'joan-common', module.vendor)
    utils.run()
