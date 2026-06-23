import streamlit as st
import requests


# 数据获取函数：向 CoinGecko 免费接口请求比特币价格
def get_bitcoin_price():
    try:
        # 获取 Bitcoin 的价格数据（usd 价格 + 24 小时涨跌幅）
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true')
        data = response.json()
        # 从返回的 JSON 里取出当前价格和 24 小时变化
        current_price = data['bitcoin']['usd']
        price_change_percentage = data['bitcoin']['usd_24h_change']

        return current_price, price_change_percentage
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None, None


# 初始化 Streamlit 应用
st.title('实时比特币价格')
st.subheader('获取最新的比特币价格信息及其24小时价格变化趋势')

# 添加刷新按钮
if st.button('刷新价格'):
    # 教程原版用的是 st.experimental_rerun()，该 API 在新版 Streamlit 已被删除，
    # 正确写法是 st.rerun()——重新从头跑一遍脚本，相当于刷新页面。
    st.rerun()

# 显示加载状态（spinner 是转圈圈的“加载中”提示）
with st.spinner('加载中...'):
    current_price, price_change_percentage = get_bitcoin_price()

# 显示数据
if current_price is not None:
    if price_change_percentage is not None:
        # 由涨跌幅反推 24 小时前的价格，再算出涨跌额（USD 绝对值）
        prev_price = current_price / (1 + price_change_percentage / 100)
        change_amount = current_price - prev_price
        # delta 传给 st.metric 后会自动“涨绿跌红”，并同时显示涨跌额和涨跌幅
        st.metric(
            label="当前比特币价格 (USD)",
            value=f"${current_price:,.2f}",
            delta=f"{change_amount:,.2f} USD ({price_change_percentage:.2f}%)",
        )
    else:
        st.metric(label="当前比特币价格 (USD)", value=f"${current_price:,.2f}")
else:
    st.error("无法获取数据，请稍后重试。")
