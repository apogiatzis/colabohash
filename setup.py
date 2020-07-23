from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    install_requires=[
        "html5lib==1.1",
        "jinja2==2.11.2",
        "markupsafe==1.1.1",
        "mechanize==0.4.5",
        "selenium==3.141.0",
        "six==1.15.0",
        "urllib3==1.25.9",
        "webencodings==0.5.1",
    ],
    name="colabohash",
    version="0.0.4",
    description="Hashcat with GPU support in Google Colab runtime",
    url="http://github.com/apogiatzis/colabohash",
    author="Antreas Pogiatzis",
    author_email="pogiatzis.c.a@gmail.com",
    license="MIT",
    include_package_data=True,
    package_data={"colabohash":["bin/*"]},
    packages=["colabohash"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ],
)
