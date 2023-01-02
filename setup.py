"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='codebarsticker',  # Required
    version='0.1.0',  # Required
    description='This is a project to generate code bars on a given PDF template in order to print stickers.',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/davidusb-geek/CodeBarSticker',  # Optional
    author='David HERNANDEZ',  # Optional
    author_email='davidusb@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    keywords='codebar, stickers, template',  # Optional
    packages=find_packages(),  # Required
    python_requires='>=3.8, <3.10',
    install_requires=[
        'treepoem==3.18.0',
        'PyMuPDF==1.21.1',
    ],  # Optional
    package_data={'codebarsticker': ['config.json']},
)
