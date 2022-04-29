from setuptools import setup, find_packages

setup(
    name='draft',
    # packages=['flaskdraft'],,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['flask']
)


"""
# https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
#
from setuptools import setup, find_packages

setup(name='corenet_api', version='1.0', packages=find_packages())
"""
