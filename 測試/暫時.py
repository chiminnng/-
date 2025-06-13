import streamlit as st
import pandas as pd
import os

# 頁面標題
st.title("NBA 球隊正負值分析與勝率預測")

# pandas 格式化
pd.options.display.float_format = '{:.2f}'.format

# 掃描 CSV 檔案
csv_dir = "測試"
csv_files = [f for f in os.listdir(csv_dir) if f.endswith('_plus_minus.csv')]
if not csv_files:
    st.error("找不到 CSV 檔案")
    st.stop()

dfs = [pd.read_csv(os.path.join(csv_dir, f)) for f in csv_files]
df_all = pd.concat(dfs, ignore_index=True)


# 合併 CSV
dfs = [pd.read_csv(f) for f in csv_files]
df_all = pd.concat(dfs, ignore_index=True)

# 列出球隊選單
all_teams = sorted(df_all['球隊'].unique())
team_name1 = st.selectbox("請選擇主場球隊：", all_teams)
team_name2 = st.selectbox("請選擇客場球隊：", all_teams)

# 計算正負值
def get_team_stats(team_name):
    team_df = df_all[df_all['球隊'] == team_name]
    avg_pm = team_df['平均正負值'].mean()
    return team_df, avg_pm

if team_name1 and team_name2:
    team1_df, team1_avg = get_team_stats(team_name1)
    team2_df, team2_avg = get_team_stats(team_name2)

    st.subheader(f"{team_name1} 球員平均正負值")
    st.dataframe(team1_df[['球員', '平均正負值']].set_index('球員'))
    st.write(f"**全隊平均正負值：** `{team1_avg:.2f}`")

    st.subheader(f"{team_name2} 球員平均正負值")
    st.dataframe(team2_df[['球員', '平均正負值']].set_index('球員'))
    st.write(f"**全隊平均正負值：** `{team2_avg:.2f}`")

    # 勝率計算
    def get_adjusted_win_rate(pm1, pm2):
        diff = abs(pm1 - pm2)
        if diff <= 5:
            bonus = 0.10
        elif diff <= 10:
            bonus = 0.20
        else:
            bonus = 0.30

        base_home = 0.6
        base_away = 0.4

        if pm1 > pm2:
            home_final = base_home + bonus
            away_final = base_away - bonus
        elif pm1 < pm2:
            home_final = base_home - bonus
            away_final = base_away + bonus
        else:
            home_final = base_home
            away_final = base_away

        total = home_final + away_final
        return home_final / total, away_final / total

    home_win_rate, away_win_rate = get_adjusted_win_rate(team1_avg, team2_avg)

    # 顯示預測結果
    st.subheader("勝率預測結果")
    st.write(f"**{team_name1}（主場）預測勝率：** `{home_win_rate:.2%}`")
    st.write(f"**{team_name2}（客場）預測勝率：** `{away_win_rate:.2%}`")
