from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='manga109api',
    version='0.1.0',
    description='Simple python API to read annotation data of Manga109',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Yusuke Matsui',
    author_email='matsui528@gmail.com',
    url='https://github.com/matsui528/manga109api',
    license='MIT',
    packages=find_packages(),
    install_requires=['xmltodict'],
)
