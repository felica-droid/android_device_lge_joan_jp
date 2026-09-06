#
# Copyright (C) 2018-2023 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

$(call inherit-product, $(SRC_TARGET_DIR)/product/product_launched_with_n_mr1.mk)

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/non_ab_device.mk)

# Inherit from joan_jp device
$(call inherit-product, device/lge/joan_jp/device.mk)

# Device identifiers
PRODUCT_DEVICE := joan_jp
PRODUCT_NAME := lineage_joan_jp
PRODUCT_BRAND := lge
PRODUCT_MODEL := joan_jp
PRODUCT_MANUFACTURER := LGE
PRODUCT_RELEASE_NAME := V30

PRODUCT_GMS_CLIENTID_BASE := android-om-lg

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="joan_dcm_jp-user 9 PKQ1.190414.001 20072184679ed release-keys" \
    BuildFingerprint="lge/joan_global_com/joan:8.0.0/OPR1.170623.026/181381736b4e9:user/release-keys"

PRODUCT_SYSTEM_PROPERTY_BLACKLIST += ro.product.model ro.vendor.product.model ro.product.system.model
