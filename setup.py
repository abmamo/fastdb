from setuptools import setup, find_packages

# read the contents of README file
from os import path
# get current file directory
this_directory = path.abspath(path.dirname(__file__))
# open README with UTF-8 encoding
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    # read README
    long_description = f.read()

setup(
      name='fastdb',
      version='0.0.1',
      description='python interface to docker databases',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/abmamo/fastdb',
      author='Abenezer Mamo',
      author_email='contact@abmamo.com',
      license='MIT',
      packages=find_packages(exclude=("tests",)),
      include_package_data=True,
      install_requires=[
          "oyaml==1.0"
          ],
      zip_safe=False
)
