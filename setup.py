import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
install_reqs = open("requirements.txt", "rb").read().decode("utf-8")

setuptools.setup(
    name="feasible-cat",
    version="0.9",
    author="Cat Chenal",
    author_email="catchenal@gmail.com",
    description="A plotting function of the feasible region of a linear programming problem.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CatChenal/Feasible_Region",
    project_urls={
        "Issue Tracker": "https://github.com/CatChenal/Feasible_Region/issues",
        #"Documentation": "https://feasible.readthedocs.io/en/stable/",
    },
    packages=setuptools.find_packages(),
    install_requires=install_reqs
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Framework :: Matplotlib",
    ],
    python_requires='>=3.7',
)
