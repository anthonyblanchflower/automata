from setuptools import setup

setup(
    name='automata',
    version='0.0.1',
    packages=['automata', 'automata/data'],
    author='anthony blanchflower',
    author_email='anthonyblanchflower@btinternet.com',
    description='Cellular automata simulation',
    long_description=open('README.txt').read(),
    package_data={'data': ['*'], },
    include_package_data=True,
    classifiers=[
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3']
)
