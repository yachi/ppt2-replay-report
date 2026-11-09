while ! grep -q STAGE2_DONE drive_qh1.out; do pgrep -f drive_qh1.sh >/dev/null || exit 1; sleep 30; done
bash drive_qh2.sh > drive_qh2.out 2>&1
