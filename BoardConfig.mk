#
# Copyright (C) 2018-2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

DEVICE_PATH := device/lge/joan_jp

TARGET_OTA_ASSERT_DEVICE := L-01K,LGV35,joan,joan_jp,l01k,lgv35

# inherit from common repository
include device/lge/joan-common/BoardConfigCommon.mk

# Kernel
TARGET_KERNEL_CONFIG := lineageos_joan_jp_defconfig

# SELinux
BOARD_VENDOR_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/vendor

# VINTF
DEVICE_FRAMEWORK_COMPATIBILITY_MATRIX_FILE += \
    $(DEVICE_PATH)/framework_compatibility_matrix.xml
DEVICE_MANIFEST_FILE += $(DEVICE_PATH)/manifest.xml

# inherit from the proprietary version
include vendor/lge/joan_jp/BoardConfigVendor.mk
