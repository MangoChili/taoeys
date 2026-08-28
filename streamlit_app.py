import streamlit as st
import random

# charactors
role_db = {
    "goose": [
        {
            "name": "大白鹅",
            "skill": "无特殊技能，依靠做任务、发言投票找出鸭子",
            "task": "完成你的全部任务，开会理性发言，投出所有鸭子",
            "win": "胜利条件：所有鸭子出局"
        },
        {
            "name": "警长",
            "skill": "本局可以找DM出刀；刀鸭子/中立对方出局；刀鹅则你一同出局",
            "task": "暗中观察，谨慎出刀，完成任务",
            "win": "胜利条件：所有鸭子出局"
        },
        {
            "name": "加拿大鹅",
            "skill": "被鸭子击杀时DM立刻公开凶手；被专业杀手击杀不会触发报警",
            "task": "尽量暴露在大家视野，引诱鸭子来杀你",
            "win": "胜利条件：所有鸭子出局"
        },
        {
            "name": "正义使者",
            "skill": "整局仅有1次出刀机会，刀任何人都不会反噬自己，用完变普通鹅",
            "task": "收集信息，关键回合再使用出刀",
            "win": "胜利条件：所有鸭子出局"
        },
        {
            "name": "侦探",
            "skill": "开会阶段可向DM查询一名玩家本回合是否出过刀",
            "task": "多观察行动轨迹，开会向DM获取信息",
            "win": "胜利条件：所有鸭子出局"
        },
        {
            "name": "保镖鹅",
            "skill": "每回合可保护1人，被保护者本回合不会被刀，不可连续保同一人，不能保自己",
            "task": "保护高价值玩家，完成任务",
            "win": "胜利条件：所有鸭子出局"
        },
        {
            "name": "模仿鹅",
            "skill": "鸭子阵营会知道场上存在模仿，但不知道是谁，鸭子视你为同类",
            "task": "混入鸭子圈子获取情报，小心被鸭子误杀",
            "win": "胜利条件：所有鸭子出局"
        }
    ],
    "duck": [
        {
            "name": "普通鸭子",
            "skill": "找DM示意击杀玩家，可以向DM发起破坏（关灯/封锁任务），和鸭队友配合",
            "task": "伪装好人，制造混乱，减少存活鹅数量",
            "win": "胜利条件：鹅存活数 ≤ 鸭子存活数"
        },
        {
            "name": "专业杀手",
            "skill": "击杀加拿大鹅不会触发加拿大鹅报警效果",
            "task": "优先处理关键好人角色，隐藏身份",
            "win": "胜利条件：鹅存活数 ≤ 鸭子存活数"
        },
        {
            "name": "间谍鸭",
            "skill": "开会阶段，可向DM查验一名玩家阵营（好人/坏人/中立）",
            "task": "收集阵营信息，误导投票",
            "win": "胜利条件：鹅存活数 ≤ 鸭子存活数"
        },
        {
            "name": "变形鸭",
            "skill": "向DM登记伪装目标，开会时你可以谎称自己是被伪装的玩家",
            "task": "伪造身份，嫁祸其他玩家",
            "win": "胜利条件：鹅存活数 ≤ 鸭子存活数"
        },
        {
            "name": "刺客鸭",
            "skill": "全局2次刺杀，开会时猜别人身份；猜对对方出局，猜错自己出局",
            "task": "记住场上角色，关键回合发动刺杀",
            "win": "胜利条件：鹅存活数 ≤ 鸭子存活数"
        }
    ],
    "neutral": [
        {
            "name": "呆呆鸟",
            "skill": "被投票投出局即直接获胜，被刀死不能胜利",
            "task": "想方设法让其他人把你投出去",
            "win": "胜利条件：开会投票被放逐出局"
        },
        {
            "name": "鹈鹕",
            "skill": "找DM吞噬玩家，被吞噬直接出局；场上只剩你一人则你胜利",
            "task": "伺机吞噬其他人活到最后",
            "win": "胜利条件：场上仅剩余自己存活"
        },
        {
            "name": "鸽子",
            "skill": "私下接触存活玩家完成感染，全部感染完成立刻胜利",
            "task": "悄悄接触所有人完成感染，不要过早暴露",
            "win": "胜利条件：全部存活玩家被你感染"
        },
        {
            "name": "猎鹰",
            "skill": "可以找DM击杀玩家；当场上剩余3人触发猎鹰时刻，存活即胜利",
            "task": "控制场上人数，等待猎鹰时刻",
            "win": "胜利条件：3人猎鹰时刻存活到最后"
        }
    ]
}


def sample_list(lst, n):
    copy = lst.copy()
    res = []
    for _ in range(min(n, len(copy))):
        item = random.choice(copy)
        copy.remove(item)
        res.append(item)
    return res


# ========= Session状态保存（streamlit无后端，内存存储，刷新全部重置） =========
if "role_list" not in st.session_state:
    st.session_state.role_list = []

st.set_page_config(page_title="涛的鹅鸭杀", page_icon="🦆")
st.title("🪿 欢迎来到涛的鹅鸭杀")
st.title("🦆 请选择你的身份")
st.caption("初版内测，版权及发布页https://github.com/MangoChili/")

tab1, tab2 = st.tabs(["🎮 房主DM生成本局", "👤玩家查看我的身份"])

with tab1:
    st.subheader("本局配置")
    total_player = st.number_input("总玩家人数", min_value=4, max_value=20, value=8)
    duck_count = st.number_input("鸭子数量", min_value=1, max_value=8, value=2)
    neu_count = st.number_input("中立数量", min_value=0, max_value=4, value=2)
    goose_count = total_player - duck_count - neu_count
    st.info(f"自动计算：好人鹅数量 = {goose_count}")

    if goose_count < 1:
        st.error("好人鹅数量不能小于1，请调整参数")
    else:
        if st.button("🎲生成本局角色", type="primary"):
            pick_goose = sample_list(role_db["goose"], goose_count)
            pick_duck = sample_list(role_db["duck"], duck_count)
            pick_neu = sample_list(role_db["neutral"], neu_count)
            all_roles = pick_goose + pick_duck + pick_neu
            random.shuffle(all_roles)
            st.session_state.role_list = all_roles
            st.success(f"✅已生成 {len(all_roles)} 个角色！告诉玩家去【玩家查看】输入1~{total_player}玩家编号")

    if len(st.session_state.role_list) > 0:
        with st.expander("🔒DM后台：查看全部角色（仅主持人看！不要给玩家看）"):
            for idx, r in enumerate(st.session_state.role_list):
                st.text(f"玩家{idx+1}：{r['name']}")

    if st.button("🔄重置本局游戏"):
        st.session_state.role_list = []
        st.rerun()


with tab2:
    st.subheader("输入你的玩家编号查看身份")
    st.warning("⚠️不要偷看别人编号，只输入属于你自己的编号！")
    pid = st.number_input("你的玩家编号", min_value=1, max_value=20, value=1)

    if st.button("📥显示我的身份"):
        roles = st.session_state.role_list
        if len(roles) == 0:
            st.error("还没有生成本局角色，请让房主先生成游戏！")
        else:
            if 1 <= pid <= len(roles):
                my = roles[pid - 1]
                st.divider()
                st.markdown(f"# {my['name']}")
                st.markdown(f"**技能**：{my['skill']}")
                st.markdown(f"**任务**：{my['task']}")
                st.markdown(f"**胜利条件**：{my['win']}")
                st.divider()
                st.info("记住你的身份！关闭页面，不要展示给其他人！")
            else:
                st.error("编号超出本局玩家总数")

st.caption("小涛的提示：请不要刷新/重启，本局数据会全部清空的喔。")
