import pandas as pd
import random

EXCEL_FILE = '리눅스 6, 7 DB.xlsx'

def get_category_list(df):
    return sorted(df['category'].unique())

def select_category():
    print("주제 목록:")
    print("1. 주제 1")
    print("2. 주제 2")
    print("3. 주제 3")
    print("4. 주제 4")
    while True:
        choice = input("공부할 주제 번호를 입력하세요 (1~4): ")
        if choice in ['1', '2', '3', '4']:
            return f"주제 {choice}"
        else:
            print("잘못된 입력입니다. 1~4 중에 선택해주세요.")

def generate_problems(df, category):
    filtered = df[df['category'] == category].copy()
    # 객관식과 주관식 분리
    objective = filtered[filtered['type'] == '객관식']
    subjective = filtered[filtered['type'] == '주관식']
    # 랜덤 추출 (중복 방지)
    objective_sample = objective.sample(n=15, replace=False) if len(objective) >= 15 else objective
    subjective_sample = subjective.sample(n=5, replace=False) if len(subjective) >= 5 else subjective
    return objective_sample, subjective_sample

def ask_question(row):
    print("\n문제:")
    print(row['question'])
    user_answer = input("답을 입력하세요: ").strip()
    if str(user_answer).lower() == str(row['answer']).strip().lower():
        print("정답입니다.\n")
    else:
        print(f"오답입니다. 정답: {row['answer']}\n")

def main():
    df = pd.read_excel(EXCEL_FILE)
    category = select_category()
    objective, subjective = generate_problems(df, category)
    
    print(f"\n--- {category} 객관식 15문제 ---")
    for idx, row in objective.iterrows():
        ask_question(row)
    print(f"\n--- {category} 주관식 5문제 ---")
    for idx, row in subjective.iterrows():
        ask_question(row)

if __name__ == '__main__':
    main()
