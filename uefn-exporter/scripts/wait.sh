#!/bin/bash
# ROOT=/h/drugi/folder ./wait.sh ... kad UE projekti nisu u H:/UnrealToUEFN/UnrealProjects
R=${ROOT:-/h/UnrealToUEFN/UnrealProjects}
# wait.sh ue <Name> | uefnready | uefnloaded | ingame | download <Name>
case "$1" in
 ue) L=$R/$2/Saved/Logs/$2.log; s=$(date +%s); for i in $(seq 1 160); do if [ -f "$L" ] && [ $(stat -c %Y "$L") -ge $((s-5)) ] && grep -a -q "Total Editor Startup Time" "$L"; then echo READY; exit; fi; if [ -f "$L" ] && grep -a -q -E "Critical error|GPU crash" "$L" && [ $(stat -c %Y "$L") -ge $((s-5)) ]; then echo CRASH; exit; fi; sleep 3; done; echo TIMEOUT;;
 uefnready) L="/c/Users/dejan/AppData/Local/UnrealEditorFortnite/Saved/Logs/UnrealEditorFortnite.log"; sleep 12; for i in $(seq 1 160); do T=$(grep -a "Total Editor Startup Time" "$L" 2>/dev/null | tail -1 | cut -c2-20); if [ -n "$T" ] && [ $(stat -c %Y "$L") -gt 0 ] && [ "$(date -d "$(echo $T | sed 's/\./-/;s/\./-/;s/-\([0-9][0-9]\)\.\([0-9][0-9]\)\.\([0-9][0-9]\)/ \1:\2:\3/')Z" +%s 2>/dev/null)" -ge $(( $(date +%s) - 300 )) ]; then echo READY; exit; fi; sleep 3; done; echo TIMEOUT;;
 uefnloaded) L="/c/Users/dejan/AppData/Local/UnrealEditorFortnite/Saved/Logs/UnrealEditorFortnite.log"; n=$(grep -a -c "OpenProject_FinalizeAndLoadMap - Done" "$L" 2>/dev/null); for i in $(seq 1 200); do m=$(grep -a -c "OpenProject_FinalizeAndLoadMap - Done" "$L" 2>/dev/null); if [ "$m" -gt "$n" ] || { [ "$m" -ge 1 ] && [ "$2" = "any" ]; }; then echo LOADED; grep -a "VerseBuild: S\|VerseBuild: F" "$L" | tail -1; exit; fi; sleep 3; done; echo TIMEOUT;;
 download) C=$R/$2/Content; prev=-1; same=0; for i in $(seq 1 300); do n=$(find "$C" -type f 2>/dev/null | wc -l); if [ "$n" -gt 0 ] && [ "$n" -eq "$prev" ]; then same=$((same+1)); else same=0; fi; prev=$n; if [ "$n" -gt 0 ] && [ $same -ge 6 ]; then break; fi; sleep 5; done; echo "files $n"; ls "$C"; for d in "$C"/*/; do echo "== $d"; ls "$d"; ls "$d"Maps "$d"Map "$d"Levels 2>/dev/null; done;;
esac
