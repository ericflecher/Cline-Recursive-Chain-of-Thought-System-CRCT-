from setuptools import setup, find_packages

setup(
    name="{{package_name}}",
    version="0.1.0",
    description="{{project_description}}",
    author="{{author}}",
    author_email="{{author_email}}",
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
