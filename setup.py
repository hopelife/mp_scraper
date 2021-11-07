from setuptools import setup
import mp_scraper

setup(
    name='mp_scraper',
    version=mp_scraper.__version__,
    description='Moon Package for web Scraper',
    url='https://github.com/hopelife/mp_scraper',
    author='Moon Jung Sam',
    author_email='monblue@snu.ac.kr',
    license='MIT',
    packages=['mp_scraper'],
    # entry_points={'console_scripts': ['mp_scraper = mp_scraper.__main__:main']},
    keywords='scraper',
    # python_requires='>=3.8',  # Python 3.8.6-32 bit
    # install_requires=[ # 패키지 사용을 위해 필요한 추가 설치 패키지
    #     'selenium',
    # ],
    # zip_safe=False
)
