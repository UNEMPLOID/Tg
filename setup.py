from setuptools import setup, find_packages

setup(
    name="tg-archive",
    version="1.2.1",  
    description="Tool for exporting Telegram group chats into static websites.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Seu Nome",
    author_email="seu.email@dominio.com",
    url="https://github.com/seu_usuario/tg-archive",
    packages=find_packages(include=['tgarchive', 'tgarchive.*']),  
    install_requires=open('requirements.txt').read().splitlines(),
    include_package_data=True,
    download_url="https://github.com/seu_usuario/tg-archive",
    license="MIT License",
    entry_points={
        'console_scripts': [
            'tg-archive = bantele:main' 
        ],
    },
    classifiers=[
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Documentation"
    ],
)