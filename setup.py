try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ""

setup(
    name='youtube-python',
    version='1.0.4',
    description='Python Youtube Data API v3',
    long_description=long_description,
    url='https://github.com/rohitkhatri/youtube-python',
    author='Rohit Khatri',
    author_email='developer.rohitkhatri@gmail.com',
    license='GPL',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.5',
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords="youtube data api python v3",
    packages=[''],
    install_requires=['requests']
)
