from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = []
    for line in f:
        requirements.append(line.rstrip())

setup(
    name='manga109api',
    version='0.2.1',
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
