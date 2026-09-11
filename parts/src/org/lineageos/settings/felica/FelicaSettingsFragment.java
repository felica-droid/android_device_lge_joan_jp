/*
 * Copyright (C) 2026 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package org.lineageos.settings.felica;

import android.os.Bundle;
import android.os.SystemProperties;

import androidx.preference.ListPreference;
import androidx.preference.Preference;
import androidx.preference.PreferenceFragment;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

public class FelicaSettingsFragment extends PreferenceFragment
        implements Preference.OnPreferenceChangeListener {

    private static final String KEY_FELICA_MODEL = "felica_model";

    /* init.felica_model.rc binds /system/etc/felica_<value> over /system/etc/felica. */
    private static final String PROP_FELICA_MODEL = "persist.felica.model";

    private static final File FELICA_DIR = new File("/system/etc");
    private static final String FELICA_PREFIX = "felica_";

    /* The SKU is how the sets are named; this is how the handset is sold. */
    private static final Map<String, String> MODEL_LABELS = Map.of(
            "joan_dcm_jp", "L-01K (docomo)",
            "joan_kddi_jp", "LGV35 (au)");

    @Override
    public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
        addPreferencesFromResource(R.xml.felica_settings);

        final ListPreference pref = findPreference(KEY_FELICA_MODEL);

        /*
         * The sets that ship are whatever the blob list extracted, so read them
         * off the filesystem rather than carrying a SKU table here as well.
         */
        final String[] dirs = FELICA_DIR.list((dir, name) -> name.startsWith(FELICA_PREFIX)
                && new File(dir, name).isDirectory());
        if (dirs == null || dirs.length == 0) {
            pref.setVisible(false);
            return;
        }
        Arrays.sort(dirs);

        final List<String> entries = new ArrayList<>();
        final List<String> values = new ArrayList<>();

        /* An empty value means "leave it to the SKU detection in init.joan.rc". */
        entries.add(getString(R.string.felica_model_automatic));
        values.add("");

        for (String dir : dirs) {
            final String sku = dir.substring(FELICA_PREFIX.length());
            entries.add(MODEL_LABELS.getOrDefault(sku, sku));
            values.add(sku);
        }

        pref.setEntries(entries.toArray(new String[0]));
        pref.setEntryValues(values.toArray(new String[0]));
        pref.setValue(SystemProperties.get(PROP_FELICA_MODEL, ""));
        pref.setSummaryProvider(ListPreference.SimpleSummaryProvider.getInstance());
        pref.setOnPreferenceChangeListener(this);
    }

    @Override
    public boolean onPreferenceChange(Preference preference, Object newValue) {
        if (!KEY_FELICA_MODEL.equals(preference.getKey())) {
            return false;
        }

        /*
         * init picks this up straight away, but a bind mount is invisible to a
         * file descriptor somebody already holds - the FeliCa applications have
         * to be restarted, and a reboot is the honest way to say that.
         */
        SystemProperties.set(PROP_FELICA_MODEL, (String) newValue);
        return true;
    }
}
