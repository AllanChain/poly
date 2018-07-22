import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polygons",
    version="0.0.1",
    author="Allan Chain",
    author_email="txsmlf@gmail.com",
    description="Handle polygons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AllanChain/poly",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
