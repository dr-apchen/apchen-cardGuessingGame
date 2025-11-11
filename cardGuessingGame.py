import random

# --- 牌組定義與代碼對應 ---
# 定義所有可能的撲克牌花色 (Suits)
# 使用代碼 (C, D, H, S) 作為鍵，方便使用者輸入
SUIT_MAP = {
    'C': '梅花 (Clubs)',
    'D': '方塊 (Diamonds)',
    'H': '紅心 (Hearts)',
    'S': '黑桃 (Spades)'
}
# 僅用於顯示給使用者的花色列表 (簡稱)
SUIT_CHOICES = list(SUIT_MAP.keys()) 
# 僅用於內部比對的完整花色列表
SUITS = list(SUIT_MAP.values())

# 定義所有可能的撲克牌號碼 (Ranks)
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# 新增：號碼值對應字典，用於比較大小 (J=11, Q=12, K=13, A=14)
# 這樣才能判斷猜測的號碼是更大還是更小
RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

# 設定每局遊戲的最大猜測次數
MAX_ATTEMPTS = 5 # 變更為 5 次

# 設定中途離開的代號
EXIT_CODE = 'EXIT'

def generate_card():
    """
    隨機產生一張撲克牌的花色和號碼。
    回傳值：(花色, 號碼) 的 tuple
    """
    suit = random.choice(SUITS)
    rank = random.choice(RANKS)
    return (suit, rank)

def get_combined_guess():
    """
    獲取使用者合併輸入 (花色代碼 + 號碼)，並進行例外處理和中途離開判斷。
    
    回傳值：
        tuple: (花色, 號碼) 的 tuple，或 (EXIT_CODE, None) 表示中途退出，
               或 (None, None) 表示輸入無效需重試。
    """
    while True:
        # --- 輸入錯誤的例外處理 (Try-Except Block) ---
        try:
            suit_options = [f'{k}({v.split(' ')[0]})' for k, v in SUIT_MAP.items()]
            rank_options = ', '.join(RANKS)
            
            # 提示使用者輸入格式
            print(f"\n請輸入猜測（格式：花色代碼 號碼，例如：H K 或 C 10）")
            print(f"花色代碼：{', '.join(suit_options)}")
            print(f"號碼：{rank_options}")
            user_input = input(f"輸入 '{EXIT_CODE}' 可中途退出本局： ").strip().upper()

            # 3. 檢查中途離開代號
            if user_input == EXIT_CODE:
                return (EXIT_CODE, None)

            # 將輸入分割為花色和號碼
            parts = user_input.split()
            
            # 1. 檢查輸入項目數量
            if len(parts) != 2:
                raise ValueError("輸入格式錯誤。請確保只輸入了 花色代碼 和 號碼 兩項，並以空格隔開。")

            input_suit_code = parts[0]
            input_rank = parts[1]
            
            # 2. 檢查花色代碼是否有效
            if input_suit_code not in SUIT_MAP:
                raise ValueError(f"無效的花色代碼 '{input_suit_code}'。")
            
            # 3. 檢查號碼是否有效
            if input_rank not in RANKS:
                raise ValueError(f"無效的號碼 '{input_rank}'。")

            # 輸入有效，轉換花色代碼為完整名稱
            guessed_suit = SUIT_MAP[input_suit_code]
            guessed_rank = input_rank
            
            return (guessed_suit, guessed_rank)
            
        except ValueError as e:
            print(f"🚫 輸入錯誤: {e}")
            # 傳回 (None, None) 讓 while 迴圈繼續
            # 注意：原程式碼中這裡有 return (None, None) 應該改為 continue 讓 while 迴圈繼續，
            # 但由於原程式碼在外層已有 while 迴圈，因此這裡保留原結構。
            # 但為了健壯性，我們在外部 play_round 進行了處理。
            return (None, None)
        except Exception as e:
            print(f"⚠️ 發生未知錯誤: {e}")
            return (None, None)

def play_round():
    """
    進行一輪單局遊戲的主邏輯，加入了合併輸入、次數限制和即時提示。
    
    回傳值：
        int: 猜對回傳 1，猜錯回傳 0，中途退出回傳 -1。
    """
    print("\n--- 新的一局開始 ---")
    
    # 1. 程式隨機產生一張撲克牌
    correct_suit, correct_rank = generate_card()
    
    # 新增：獲取正確號碼的數值，用於大小比較
    correct_value = RANK_VALUES[correct_rank]
    
    # 初始化剩餘猜測次數
    attempts_left = MAX_ATTEMPTS
    
    while attempts_left > 0:
        print(f"\n您還有 {attempts_left} 次猜測機會。")
        
        # 2. 詢問使用者合併輸入
        guessed_suit, guessed_rank = (None, None)
        
        # 確保使用者輸入是有效的花色代碼和號碼
        # 這裡會重複呼叫 get_combined_guess 直到輸入有效或退出
        while guessed_suit is None and guessed_rank is None:
            guessed_suit, guessed_rank = get_combined_guess()
            
            # 判斷是否中途退出
            if guessed_suit == EXIT_CODE:
                print("\n🔔 您已選擇中途退出本局遊戲。")
                return -1 
        
        # 獲取猜測號碼的數值，用於大小比較
        # 由於 get_combined_guess 已驗證 guessed_rank 在 RANKS 中，這裡取值安全
        guessed_value = RANK_VALUES[guessed_rank]

        # 3. 判斷並顯示結果
        print("\n--- 本次猜測結果 ---")
        print(f"您猜測的牌是: **{guessed_suit}** **{guessed_rank}**")
        
        # 檢查花色和號碼是否都正確
        if guessed_suit == correct_suit and guessed_rank == correct_rank:
            print(f"程式生成的牌是: **{correct_suit}** **{correct_rank}**")
            print("\n🎉 **恭喜您！完全猜對了！** 您真是個高手！")
            return 1 # 猜對，回傳 1
        else:
            # 猜錯，減少剩餘次數
            attempts_left -= 1
            print("😢 **很可惜，這次沒有完全猜對。**")
            
            # --- 即時提示功能修改 ---
            suit_match = (guessed_suit == correct_suit)
            rank_match = (guessed_rank == correct_rank)

            if suit_match:
                # 花色猜對，但號碼錯了，提供新的大小提示
                if guessed_value > correct_value:
                    print("✨ **提示：您猜對了花色！** 數字太大了，請猜更小的號碼！")
                else: # guessed_value < correct_value
                    print("✨ **提示：您猜對了花色！** 數字太小了，請猜更大的號碼！")
            elif rank_match:
                # 號碼猜對，但花色錯了 (保留原有提示)
                print("✨ **提示：您猜對了號碼！** (但花色錯了)")
            # --------------------------
                
            if attempts_left > 0:
                print(f"請再試一次！")
    
    # 4. 如果迴圈結束 (次數用盡) 仍未猜對
    print("\n💔 **猜測次數已用完！**")
    print(f"正確答案是: **{correct_suit}** **{correct_rank}**")
    return 0 # 猜錯，回傳 0

def main():
    """
    遊戲主程式，控制多局遊戲的迴圈。
    """
    print("=== 歡迎來到撲克牌猜謎遊戲 ===")
    print(f"每局您有 **{MAX_ATTEMPTS}** 次猜測機會，請把握機會！")
    
    total_rounds = 0
    wins = 0
    
    # 讓使用者可以連續玩多局
    while True:
        total_rounds += 1
        print(f"\n======== 第 {total_rounds} 局 ========")
        
        # 進行一輪遊戲
        round_result = play_round()
        
        # 根據遊戲結果更新分數
        if round_result == 1:
            wins += 1
        elif round_result == -1:
            # 中途退出，不算輸也不算贏，回合數需減一
            total_rounds -= 1
            if total_rounds < 0: total_rounds = 0 # 避免負數
        
        # 詢問是否繼續遊戲
        while True:
            try:
                # 確保在退出或無效局數時，仍能正確顯示和處理繼續選項
                play_again = input("\n還要再玩一局嗎？ (輸入 y 繼續 / 輸入 n 結束): ").strip().lower()
                
                if play_again == 'n':
                    print("\n--- 遊戲總結 ---")
                    print(f"您總共玩了 {total_rounds} 局，猜對了 {wins} 局。")
                    if total_rounds > 0:
                        print(f"勝率：{wins / total_rounds * 100:.2f}%")
                    else:
                         print("由於您中途退出，沒有完成任何一局遊戲。")
                    print("感謝您的遊玩，再見！")
                    return
                elif play_again == 'y':
                    break
                else:
                    raise ValueError("無效的選擇。")
            except ValueError as e:
                print(f"🚫 輸入錯誤: {e} 請輸入 'y' 或 'n'。")

# 執行遊戲
if __name__ == "__main__":
    main()