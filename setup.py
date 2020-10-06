from setuptools import setup, find_packages
import re

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = []
    for line in f:
        requirements.append(line.rstrip())

with open('manga109api/__init__.py') as f:
    # Version is written in manga109api/__init__.py
    # This function simply reads it
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='manga109api',
    version=version,
    description='Simple python API to read annotation data of Manga109',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Yusuke Matsui',
    author_email='matsui528@gmail.com',
    url='https://github.com/manga109/manga109api',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
)
