from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def get_watcha_reviews(movie_url, max_scroll=5):
    options = Options()
    options.add_argument('--headless')  # 브라우저 창 없이 실행
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    driver.get(movie_url)
    time.sleep(3)

    # 스크롤 반복
    for _ in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    reviews = []
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.css-1yxrjdv')  # 리뷰 블록들

    for el in elements:
        try:
            score_el = el.find_element(By.CSS_SELECTOR, 'div.css-13j3rva')
            review_el = el.find_element(By.CSS_SELECTOR, 'div.css-yws6cn')
            score = len(score_el.find_elements(By.CSS_SELECTOR, 'svg'))  # 별 개수로 점수 추정 (1~5)
            review = review_el.text.strip()
            reviews.append((score, review))
        except:
            continue

    driver.quit()

    df = pd.DataFrame(reviews, columns=["score", "review"])
    return df