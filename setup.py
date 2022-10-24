from distutils.core import setup

setup(
    name='sjtu-questionnaire',
    version='0.2.0',
    description='A Python binding to SJTU Questionnaire API (https://wj.sjtu.edu.cn/)',
    author='Kunologist',
    author_email='kunologist@foxmail.com',
    url='https://github.com/Gennadiyev/sjtu-questionnaire',
    packages=['sjtuq'],
    install_requires=['requests', 'loguru'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules :: API Bindings',
    ]
)
