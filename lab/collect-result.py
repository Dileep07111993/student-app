import datetime, hashlib, json, os, platform, re, subprocess, sys
from pathlib import Path
root=Path(os.environ['RUNNER_TEMP'])/'devprep-audit'
filesystem=subprocess.check_output(['diskutil','info','/'],text=True)
report={'exitCode':int((root/'exit.txt').read_text().strip()),'stdout':(root/'stdout.log').read_text(encoding='utf8',errors='replace'),'stderr':(root/'stderr.log').read_text(encoding='utf8',errors='replace'),'phase':'execute','host':'macos','platform':sys.platform,'filesystem':'APFS' if re.search(r'File System Personality:.*APFS',filesystem) else 'unverified','osVersion':platform.platform(),'gitVersion':subprocess.check_output(['git','--version'],text=True).strip(),'scriptHash':hashlib.sha256(Path('lab/reviewed.sh').read_bytes()).hexdigest(),'inputCommit':os.environ['GITHUB_SHA'],'actionRunUrl':os.environ['GITHUB_SERVER_URL']+'/'+os.environ['GITHUB_REPOSITORY']+'/actions/runs/'+os.environ['GITHUB_RUN_ID'],'executedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(root/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
