from distutils.core import setup

setup(
    name='sjtu-questionnaire',
    version='0.1.0',
    description='A Python binding to SJTU Questionnaire API (https://wj.sjtu.edu.cn/)',
    author='Kunologist',
    author_email='kunologist@foxmail.com',
    url='https://github.com/Gennadiyev/sjtuq',
    packages=['sjtuq'],
    install_requires=['requests'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
