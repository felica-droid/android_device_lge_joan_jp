#
# Copyright (C) 2018-2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

DEVICE_PATH := device/lge/l01k

# Inherit common repository
$(call inherit-product, device/lge/joan-common/joan-common.mk)

# NFC
PRODUCT_PACKAGES += \
	libhidlbase_shim

# The HAL service is `disabled` in its own init script and starts on nothing
# but this property, which the bootloader does not hand out - stock carries it
# in /system/build.prop. Without it the CXD224x never comes up, and the only
# symptom is NFC quietly not existing. The two japanese SKUs are the Sony part;
# h930 and the rest are NXP, so this cannot live in joan-common.
PRODUCT_PRODUCT_PROPERTIES += \
	ro.boot.vendor.lge.nfc.vendor=sony

PRODUCT_SOONG_NAMESPACES += \
    $(DEVICE_PATH)

# Inherit proprietary blobs
$(call inherit-product, vendor/lge/l01k/l01k-vendor.mk)
