import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="太阳能透过谱图分析 - 3M", layout="wide")

if 'current_result' not in st.session_state or 'spectra' not in st.session_state.current_result:
    st.markdown("""
    <div style="text-align: center; margin-top: 20%; color: #6c757d;">
        <h2>暂无谱图数据。</h2>
        <p>请先在主页面上传文件并成功执行“开始计算”，然后再点击“显示谱图”。</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py", label="返回主屏幕", icon="🔙")
    st.stop()

res = st.session_state.current_result
file_ident = st.session_state.get('current_file', '未知文件')
spectra = res["spectra"]

# 页面左上角放一个返回按钮
st.page_link("app.py", label="返回主页", icon="🔙")
st.markdown("<hr>", unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=spectra['wl'], y=spectra['irr'],
    mode='lines',
    name='原始太阳能谱图',
    line=dict(color='#ffc107', width=2.5)
))

fig.add_trace(go.Scatter(
    x=spectra['wl'], y=spectra['direct'],
    mode='lines',
    name='直接透过谱图',
    line=dict(color='#0d6efd', width=2.5)
))

fig.add_trace(go.Scatter(
    x=spectra['wl'], y=spectra['total'],
    mode='lines',
    name='总透过谱图 (含二次传热)',
    line=dict(color='#dc3545', width=2.5)
))

fig.update_layout(
    title=dict(text=f'<b>太阳能光谱分布 (300 - 2500nm) - {file_ident}</b>', font=dict(size=20)),
    xaxis=dict(
        title=dict(text="波长 Wavelength (nm)", font=dict(size=14)),
        dtick=500,
        minor=dict(dtick=100, showgrid=True, gridcolor='#e5e5e5'),
        showgrid=True,
        gridcolor='#cccccc',
        zeroline=False
    ),
    yaxis=dict(
        title=dict(text="辐照度 Irradiance (W/m²)", font=dict(size=14)),
        showgrid=True,
        gridcolor='#cccccc',
        zeroline=True,
        zerolinecolor='#999999'
    ),
    legend=dict(
        x=0.99, y=0.99,
        xanchor='right', yanchor='top',
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#ced4da', borderwidth=1,
        font=dict(size=12)
    ),
    hovermode="x unified",
    margin=dict(l=60, r=40, t=60, b=60),
    plot_bgcolor="white",
    height=700
)

st.plotly_chart(fig, use_container_width=True)
