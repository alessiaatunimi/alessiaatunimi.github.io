"""Build or serve Hugo, importing BibTeX first and watching it during preview."""
import subprocess
import sys
import time
from publications import ROOT, SOURCE, generate

if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'build'
    if command not in ('build', 'serve'):
        sys.exit('Usage: python scripts/site.py [build|serve] [Hugo options]')
    generate()
    if command == 'build':
        sys.exit(subprocess.call(['hugo', '--minify', '--cleanDestinationDir', *sys.argv[2:]], cwd=ROOT))
    previous = SOURCE.read_bytes()
    server = subprocess.Popen(['hugo', 'server', '--disableFastRender', *sys.argv[2:]], cwd=ROOT)
    try:
        while server.poll() is None:
            time.sleep(0.5)
            try:
                current = SOURCE.read_bytes()
                if current != previous:
                    previous = current
                    generate()
            except Exception as error:
                print(f'Bibliography update failed; keeping last valid output: {error}', flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        if server.poll() is None:
            server.terminate()
            server.wait(timeout=10)
