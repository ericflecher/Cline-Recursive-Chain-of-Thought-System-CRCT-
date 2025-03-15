from setuptools import setup, find_packages

setup(
    name="gherkin_feature_agent",
    version="0.1.0",
    description="A Python project named gherkin_feature_agent",
    author="ericflecher",
    author_email="ericflecher@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add your dependencies here
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    python_requires=">=3.8",
)
