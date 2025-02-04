from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oracle_mcp",
    version="0.1.0",
    author="Aditya Sugandhi",
    author_email="adityasugandhi@hotmail.com",
    description="A Python-based server implementation for building automation systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adityasugandhi/oracle_mcp",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
        "httpx-sse>=0.3.0",
        "python-dotenv>=0.19.0",
        "cryptography>=3.4.7",
        "oracledb>=1.3.0",
        "mcp>=0.1.0",
        "asyncio>=3.4.3",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
            "pytest-cov>=3.0.0",
            "pytest-asyncio>=0.20.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "oracle-mcp=src.server:main",
        ],
    },
)