import setuptools

NAME = "ga4gh-rnaget-compliance"
VERSION = "1.0.0"
AUTHOR = "Jeremy Adams"
EMAIL = "jeremy.adams@ga4gh.org"

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

with open("README.md", "r") as fh:
    long_description = fh.read()
install_requires = ['requests', 'click', 'jsonschema', 'PyYAML', "Jinja2", "loompy"]

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description="Reports web service compliance to GA4GH RNAget specification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ga4gh-rnaseq/rnaget-compliance-suite",
    package_data={'': ['web/*/*', 'schemas/*']},
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        rnaget-compliance=compliance_suite.cli:main
    ''',
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ),
)
