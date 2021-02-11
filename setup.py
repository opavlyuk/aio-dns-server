from setuptools import setup


setup(
    name="aio-dns-server",
    version="0.0.1",
    author="Oleksandr Pavliuk",
    author_email="pavlyuk.olexandr@gmail.com",
    python_requires=">=3.9",
    install_requires=[
        "dnslib",
        "PyYAML",
        "motor",
    ],
    url="https://github.com/opavlyuk/aio-dns-server.git",
    entry_points={
        "console_scripts": ["aio-dns-server = aio_dns_server.main:main"],
    },
)