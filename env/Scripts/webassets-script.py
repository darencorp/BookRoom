#!"C:\Users\Nazariy Mandebura\PycharmProjects\BookRoom\env\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'webassets','console_scripts','webassets'
__requires__ = 'webassets'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('webassets', 'console_scripts', 'webassets')()
    )
