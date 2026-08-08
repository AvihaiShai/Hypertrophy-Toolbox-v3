# win32 baseline dimension delta — every capture, HEAD `001b166` vs regenerated tree

Generated mechanically from PNG IHDR chunks. The pre-regeneration side is read straight out of
the git object store (`git show HEAD:<path>`), not from any working copy. Companion table to
[`EVIDENCE.md`](EVIDENCE.md) §4 — that section states the counts, this one shows the rows they
are counted from.

`Δbytes` is included because byte size is what feeds the `nameAndSizeSha256` manifest digest: a
row with unchanged dimensions but changed bytes still moves that digest.

## `win32/visual.spec.ts-snapshots`

resized **18** · added **4** · retired **2** · same dimensions **38** · byte-identical **6**

| Capture | Before | After | ΔH | Δbytes | Status |
|---|---:|---:|---:|---:|---|
| `backup-desktop-dark.png` | 1440x1642 | 1440x1642 | 0 | -5685 | same dimensions |
| `backup-desktop-light.png` | 1440x1642 | 1440x1642 | 0 | -3713 | same dimensions |
| `backup-mobile-dark.png` | 375x3711 | 375x3707 | -4 | -2580 | resized |
| `backup-mobile-light.png` | 375x3711 | 375x3707 | -4 | -9202 | resized |
| `backup-tablet-dark.png` | 768x2950 | 768x2950 | 0 | -2789 | same dimensions |
| `backup-tablet-light.png` | 768x2950 | 768x2950 | 0 | -545 | same dimensions |
| `body-composition-desktop-dark.png` | 1440x1134 | 1440x1134 | 0 | +14717 | same dimensions |
| `body-composition-desktop-light.png` | 1440x1133 | 1440x1133 | 0 | +34728 | same dimensions |
| `body-composition-mobile-dark.png` | 375x2056 | 375x2816 | +760 | +38753 | resized |
| `body-composition-mobile-light.png` | 375x2054 | 375x2814 | +760 | +56060 | resized |
| `body-composition-tablet-dark.png` | 768x1481 | 768x1641 | +160 | +16382 | resized |
| `body-composition-tablet-light.png` | 768x1479 | 768x1639 | +160 | +32810 | resized |
| `fatigue-desktop-dark.png` | 1440x1538 | 1440x1538 | 0 | -3519 | same dimensions |
| `fatigue-desktop-light.png` | 1440x1538 | 1440x1538 | 0 | -2797 | same dimensions |
| `fatigue-mobile-dark.png` | 375x1723 | 375x1723 | 0 | -684 | same dimensions |
| `fatigue-mobile-light.png` | 375x1723 | 375x1723 | 0 | -477 | same dimensions |
| `fatigue-tablet-dark.png` | 768x1516 | 768x1516 | 0 | -542 | same dimensions |
| `fatigue-tablet-light.png` | 768x1516 | 768x1516 | 0 | -421 | same dimensions |
| `progression-desktop-dark.png` | 1440x900 | 1440x900 | 0 | 0 | **byte-identical** |
| `progression-desktop-light.png` | 1440x900 | 1440x900 | 0 | 0 | **byte-identical** |
| `progression-mobile-dark.png` | 375x2113 | 375x2113 | 0 | 0 | **byte-identical** |
| `progression-mobile-light.png` | 375x2113 | 375x2113 | 0 | 0 | **byte-identical** |
| `progression-tablet-dark.png` | 770x1024 | 770x1024 | 0 | 0 | **byte-identical** |
| `progression-tablet-light.png` | 770x1024 | 770x1024 | 0 | 0 | **byte-identical** |
| `session-summary-desktop-dark.png` | 1440x2696 | 1440x2696 | 0 | -5628 | same dimensions |
| `session-summary-desktop-light.png` | 1440x2696 | 1440x2696 | 0 | -220 | same dimensions |
| `session-summary-mobile-dark.png` | 375x10407 | 375x10401 | -6 | -2109 | resized |
| `session-summary-mobile-light.png` | 375x10407 | 375x10401 | -6 | +3882 | resized |
| `session-summary-tablet-dark.png` | 768x3338 | 768x3338 | 0 | -2250 | same dimensions |
| `session-summary-tablet-light.png` | 768x3338 | 768x3338 | 0 | +2865 | same dimensions |
| `user-profile-desktop-dark.png` | 1440x6160 | 1440x6160 | 0 | +71797 | same dimensions |
| `user-profile-desktop-light.png` | 1440x6150 | 1440x6150 | 0 | +72501 | same dimensions |
| `user-profile-mobile-dark-segment-1.png` | — | 375x10000 | — | — | **added** |
| `user-profile-mobile-dark-segment-2.png` | — | 375x9836 | — | — | **added** |
| `user-profile-mobile-dark.png` | 375x19785 | — | — | — | **retired** |
| `user-profile-mobile-light-segment-1.png` | — | 375x10000 | — | — | **added** |
| `user-profile-mobile-light-segment-2.png` | — | 375x9793 | — | — | **added** |
| `user-profile-mobile-light.png` | 375x19742 | — | — | — | **retired** |
| `user-profile-tablet-dark.png` | 768x9602 | 768x9636 | +34 | +171167 | resized |
| `user-profile-tablet-light.png` | 768x9590 | 768x9624 | +34 | +172233 | resized |
| `volume-splitter-desktop-dark.png` | 1440x1162 | 1440x1162 | 0 | -3309 | same dimensions |
| `volume-splitter-desktop-light.png` | 1440x1162 | 1440x1162 | 0 | -3293 | same dimensions |
| `volume-splitter-mobile-dark.png` | 375x3148 | 375x3144 | -4 | -323 | resized |
| `volume-splitter-mobile-light.png` | 375x3148 | 375x3144 | -4 | -1903 | resized |
| `volume-splitter-tablet-dark.png` | 768x1946 | 768x1946 | 0 | -416 | same dimensions |
| `volume-splitter-tablet-light.png` | 768x1946 | 768x1946 | 0 | -840 | same dimensions |
| `weekly-summary-desktop-dark.png` | 1440x3269 | 1440x3269 | 0 | -3485 | same dimensions |
| `weekly-summary-desktop-light.png` | 1440x3269 | 1440x3269 | 0 | -570 | same dimensions |
| `weekly-summary-mobile-dark.png` | 375x11565 | 375x11559 | -6 | -2642 | resized |
| `weekly-summary-mobile-light.png` | 375x11565 | 375x11559 | -6 | +1598 | resized |
| `weekly-summary-tablet-dark.png` | 768x3732 | 768x3732 | 0 | -2260 | same dimensions |
| `weekly-summary-tablet-light.png` | 768x3732 | 768x3732 | 0 | +2349 | same dimensions |
| `welcome-desktop-dark.png` | 1440x4043 | 1440x4043 | 0 | -4132 | same dimensions |
| `welcome-desktop-light.png` | 1440x4043 | 1440x4043 | 0 | -3267 | same dimensions |
| `welcome-mobile-dark.png` | 375x7864 | 375x7864 | 0 | -2547 | same dimensions |
| `welcome-mobile-light.png` | 375x7864 | 375x7864 | 0 | -1845 | same dimensions |
| `welcome-tablet-dark.png` | 768x6734 | 768x6734 | 0 | -849 | same dimensions |
| `welcome-tablet-light.png` | 768x6734 | 768x6734 | 0 | -962 | same dimensions |
| `workout-log-desktop-dark.png` | 1440x1095 | 1440x1095 | 0 | -2574 | same dimensions |
| `workout-log-desktop-light.png` | 1440x1095 | 1440x1095 | 0 | -3043 | same dimensions |
| `workout-log-mobile-dark.png` | 375x8642 | 375x8640 | -2 | -2833 | resized |
| `workout-log-mobile-light.png` | 375x8642 | 375x8640 | -2 | +4244 | resized |
| `workout-log-tablet-dark.png` | 768x1395 | 768x1395 | 0 | -30 | same dimensions |
| `workout-log-tablet-light.png` | 768x1395 | 768x1395 | 0 | -44 | same dimensions |
| `workout-plan-mobile-dark.png` | 375x9330 | 375x9328 | -2 | +14792 | resized |
| `workout-plan-mobile-light.png` | 375x9330 | 375x9328 | -2 | +15728 | resized |
| `workout-plan-tablet-dark.png` | 835x3095 | 835x3095 | 0 | -954 | same dimensions |
| `workout-plan-tablet-light.png` | 835x3094 | 835x3094 | 0 | +41 | same dimensions |

## `win32/visual-baseline-thumbnails.spec.ts-snapshots`

resized **6** · added **0** · retired **0** · same dimensions **9** · byte-identical **0**

| Capture | Before | After | ΔH | Δbytes | Status |
|---|---:|---:|---:|---:|---|
| `log-desktop-dark.png` | 1406x562 | 1406x562 | 0 | +816 | same dimensions |
| `log-desktop-light.png` | 1406x562 | 1406x562 | 0 | +648 | same dimensions |
| `log-mobile-dark.png` | 341x7957 | 341x7955 | -2 | -4743 | resized |
| `log-mobile-light.png` | 341x7957 | 341x7955 | -2 | +4684 | resized |
| `log-tablet-dark.png` | 734x814 | 734x814 | 0 | +383 | same dimensions |
| `log-tablet-light.png` | 734x814 | 734x814 | 0 | +262 | same dimensions |
| `plan-desktop-light-simple.png` | 1525x576 | 1525x576 | 0 | +3397 | same dimensions |
| `plan-mobile-dark-advanced.png` | 239x3969 | 239x3967 | -2 | +2213 | resized |
| `plan-mobile-dark-simple.png` | 235x5418 | 235x5416 | -2 | -1341 | resized |
| `plan-mobile-light-advanced.png` | 239x3969 | 239x3967 | -2 | +3846 | resized |
| `plan-mobile-light-simple.png` | 235x5418 | 235x5416 | -2 | +406 | resized |
| `plan-tablet-dark-advanced.png` | 632x740 | 632x740 | 0 | +614 | same dimensions |
| `plan-tablet-dark-simple.png` | 765x556 | 765x556 | 0 | -2446 | same dimensions |
| `plan-tablet-light-advanced.png` | 632x739 | 632x739 | 0 | +552 | same dimensions |
| `plan-tablet-light-simple.png` | 765x555 | 765x555 | 0 | -925 | same dimensions |

## Reading the byte-identical rows

The six `progression` captures reproduced exactly, matching #304's control run — `progression` was
the only page passing in all six viewport/theme combinations there.
