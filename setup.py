from distutils.core import setup

NAME                = 'wbquery'
MAINTAINER          = "Skipper Seabold"
MAINTAINER_EMAIL    = "js2796a@american.edu"
DESCRIPTION         = "Access World Bank API in Python"
LONG_DESCRIPTION    = None
URL                 = ""
DOWNLOAD_URL        = ""
LICENSE             = 'BSD'
CLASSIFIERS         = None
AUTHOR              = "Skipper Seabold"
AUTHOR_EMAIL        = None
PLATFORMS           = ["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"]
MAJOR               = 0
MINOR               = 0
MICRO               = 0
ISRELEASED          = False
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


def setup_package():
    setup(
        pacakges=['wbquery'],
        version=VERSION,
        name=NAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url=URL,
        download_url=DOWNLOAD_URL,
        license=LICENSE,
        classifiers=CLASSIFIERS,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        platforms='any')

if __name__ == "__main__":
    setup_package()
