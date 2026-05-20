import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from calculator import calculate_params

# ========== 页面配置 ==========
st.set_page_config(
    page_title="3M Window Film 计算器 (GB/T 2680)",
    layout="wide"
)

# ========== 自定义 CSS ==========
st.markdown("""
<style>
.hero-card {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    border: 2px solid;
    height: 100%;
}
.border-vlt { border-color: #0d6efd; }
.border-tser { border-color: #0dcaf0; }
.border-uvb { border-color: #ffc107; }
.border-vlr { border-color: #6c757d; }
.hero-label { font-size: 1.1rem; color: #6c757d; font-weight: 500; }
.hero-value { font-size: 2.5rem; font-weight: bold; color: #dc3545; }
.hero-unit { font-size: 1.5rem; color: #6c757d; font-weight: normal; }

/* 顶栏图标布局 */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
.header-title-container {
    max-width: 850px;
}
.header-title {
    font-family: '3M Circular TT Book', '3M Circular', sans-serif;
    font-size: 2.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.header-desc {
    color: #6c757d;
    font-size: 0.9rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ========== 页面头部 ==========
logo_svg = "PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA3My4wMSA0OSI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOnJlZDt9PC9zdHlsZT48L2RlZnM+PHBhdGggY2xhc3M9ImNscy0xIiBkPSJNNTAuMzgsMTIuNTJsLTMuNDUsMTQtMy40Ni0xNGgtMTB2NS4xN0MzMi4yNywxMy4xNiwyNy44MiwxMiwyMy44NSwxMiwxOSwxMS45LDEzLjYyLDE0LDEzLjQ0LDIwLjQxaDYuN2EzLjIsMy4yLDAsMCwxLDMuNDUtM2MyLjA1LDAsMywuODYsMy4wNSwyLjIyLS4wNywxLjE5LS43NywyLTMsMkgyMS4zNXY0LjY1aDJjMS4xNiwwLDIuNzguNjQsMi44NCwyLjI5LjA4LDItMS4yOSwyLjg1LTMsMi44Ni0zLS4xMS0zLjc5LTIuNDMtMy43OS00LjQyaC03YzAsMS4zNCwwLDEwLjA5LDEwLjksMTAsNS4yMy4wNSw5LTIuMTUsMTAuMS01LjE4VjM2LjVoNi43MlYyMS4zN0w0My45MywzNi41aDZsMy43My0xNS4xMVYzNi41Mmg2Ljg1di0yNFptLTE2Ljg3LDE0YTUuMyw1LjMsMCwwLDAtMi43NC0yLjc5LDQuNjMsNC42MywwLDAsMCwyLjc0LTMuMloiLz48L3N2Zz4="

st.markdown(f"""
<div class="header-container">
    <div class="header-title-container">
        <div class="header-title">Window Film 计算器 (GB/T 2680)</div>
        <div class="header-desc">本工具严格遵循国家标准 《<strong>GB/T 2680</strong> 建筑玻璃 可见光透射比、太阳光直接透射比、太阳能总透射比、紫外线透射比及有关窗玻璃参数的测定》，支持直接解析Lambda分光光度计原始光谱数据，将原本耗时、繁琐的 Excel 查表与人工积分转换工作，简化为“一键式”的秒级计算。</div>
    </div>
    <img src="data:image/svg+xml;base64,{logo_svg}" alt="3M Logo" style="height: 85px; width: auto; object-fit: contain;">
</div>
<hr style="margin-top: 0.5rem; margin-bottom: 2rem;">
""", unsafe_allow_html=True)

# ========== 状态初始化 ==========
if 'history_data' not in st.session_state:
    st.session_state.history_data = []

col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown("#### 1. 上传测试数据")
    
    with st.container(border=True):
        trans_csv = st.file_uploader("**透光率 (T%) CSV** :red[*]", type=['csv'])
        refl_csv = st.file_uploader("**外反射率 (R%) CSV** :red[*]", type=['csv'])
        in_refl_csv = st.file_uploader("**内反射率 (R_in%) CSV** (选填)", type=['csv'])
        
        if st.button("开始计算", type="primary", use_container_width=True):
            if trans_csv and refl_csv:
                try:
                    trans_text = trans_csv.getvalue().decode('utf-8', errors='replace')
                    refl_text = refl_csv.getvalue().decode('utf-8', errors='replace')
                    in_refl_text = in_refl_csv.getvalue().decode('utf-8', errors='replace') if in_refl_csv else None
                    
                    res = calculate_params(trans_text, refl_text, in_refl_text)
                    
                    file_ident = trans_csv.name.replace(".csv", "").replace(".样品", "").replace(".原始数据", "").replace("-trans", "").replace("-refl-front", "")
                    
                    # Store original values in history list to match HTML logic
                    res["name"] = file_ident
                    st.session_state.history_data.insert(0, res)
                    
                    if len(st.session_state.history_data) > 30:
                        st.session_state.history_data.pop()
                        
                    st.session_state.current_result = res
                    st.session_state.current_file = file_ident

                except Exception as e:
                    st.error(f"计算出错: {str(e)}")
            else:
                st.error("错误: 必须上传 透光率(T%) 和 室外反射率(R%) CSV 文件。")
                
    st.markdown("#### 📜 计算历史")
    
    with st.container(border=True):
        if not st.session_state.history_data:
            st.markdown("<div style='text-align: center; color: gray; padding: 20px;'>（计算结果将自动保存在这里）</div>", unsafe_allow_html=True)
        else:
            # 渲染历史表格
            history_rows = []
            for i, item in enumerate(st.session_state.history_data):
                vlr_str = f"{item['VLR_I']:.1f}" if item.get('VLR_I') is not None else "-"
                history_rows.append({
                    "文件标识": item['name'],
                    "VLT(%)": round(item['VLT'], 1),
                    "Tser(%)": round(item['TSER'], 1),
                    "UVB(%)": round(item['UVB'], 1),
                    "VLR": vlr_str
                })
            
            history_df = pd.DataFrame(history_rows)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🗑️ 清空历史", use_container_width=True):
                    st.session_state.history_data = []
                    # 也可以在这里清除 current_result
                    if 'current_result' in st.session_state:
                         del st.session_state['current_result']
                         del st.session_state['current_file']
                    st.rerun()
            with col_b2:
                export_data = []
                for item in st.session_state.history_data:
                    vlr_str = f"{item['VLR_I']:.1f}" if item.get('VLR_I') is not None else "N/A"
                    export_data.append([item['name'], round(item['VLT'], 1), round(item['TSER'], 1), round(item['UVB'], 1), vlr_str])
                
                export_csv = "Filename,VLT(%),Tser(%),UV Block(%),VLR(%)\\n"
                for row in export_data:
                    export_csv += f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\\n"
                
                st.download_button(
                    label="↓ 导出 CSV",
                    data=export_csv.encode('utf-8-sig'),
                    file_name="GB2680_history_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

with col_right:
    if 'current_result' in st.session_state:
        res = st.session_state.current_result
        file_ident = st.session_state.current_file
        
        st.markdown("#### 核心指标总览")
        st.markdown("<hr style='margin-top:0.5rem; margin-bottom:1rem;'>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        
        c1.markdown(f'<div class="hero-card border-vlt"><div class="hero-label">可见光透光率 (VLT)</div><div class="hero-value">{res["VLT"]:.1f}<span class="hero-unit">%</span></div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="hero-card border-tser"><div class="hero-label">总隔热率 (Tser)</div><div class="hero-value">{res["TSER"]:.1f}<span class="hero-unit">%</span></div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="hero-card border-uvb"><div class="hero-label">紫外线阻隔率 (UV Block)</div><div class="hero-value">{res["UVB"]:.1f}<span class="hero-unit">%</span></div></div>', unsafe_allow_html=True)
        
        if res.get('VLR_I') is not None:
            c4.markdown(f'<div class="hero-card border-vlr"><div class="hero-label">室内可见光反射率 (VLR)</div><div class="hero-value">{res["VLR_I"]:.1f}<span class="hero-unit">%</span></div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### GB/T 2680 标准指标详情")
        st.markdown("<hr style='margin-top:0.5rem; margin-bottom:1rem;'>", unsafe_allow_html=True)
        
        # Build Markdown Table matching exactly HTML styling contents
        vlr_i_val = f"{res['VLR_I']:.2f} %" if res.get('VLR_I') is not None else "未提供数据"
        vlr_i_color = "" if res.get('VLR_I') is not None else "color: gray;"
        
        table_html = f"""
        <div style="background-color: white; border-radius: 5px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #ebebeb;">
            <table style="width: 100%; text-align: left; border-collapse: collapse;">
                <thead style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                    <tr>
                        <th style="padding: 10px;">指标名称 (中/英)</th>
                        <th style="padding: 10px;">符号</th>
                        <th style="padding: 10px; text-align: right;">计算结果</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #dee2e6;">
                        <td style="padding: 10px;">可见光透射比<br><small style="color: #6c757d;">Visible Light Transmittance (VLT)</small></td>
                        <td style="padding: 10px;">$\\tau_v$</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold;">{res['VLT']:.2f} %</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #dee2e6;">
                        <td style="padding: 10px;">可见光-外反射比<br><small style="color: #6c757d;">Visible Light External Reflectance</small></td>
                        <td style="padding: 10px;">$\\rho_{{v,e}}$</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold;">{res['VLR_E']:.2f} %</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #dee2e6; {vlr_i_color}">
                        <td style="padding: 10px;">可见光-内反射比<br><small style="color: #6c757d;">Visible Light Internal Reflectance</small></td>
                        <td style="padding: 10px;">$\\rho_{{v,i}}$</td>
                        <td style="padding: 10px; text-align: right;">{vlr_i_val}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #dee2e6;">
                        <td style="padding: 10px;">紫外线透射比<br><small style="color: #6c757d;">Ultraviolet Transmittance (UVT)</small></td>
                        <td style="padding: 10px;">$\\tau_{{uv}}$</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold;">{res['UVT']:.2f} %</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #dee2e6;">
                        <td style="padding: 10px;">太阳光直接透射比<br><small style="color: #6c757d;">Direct Solar Transmittance (DET)</small></td>
                        <td style="padding: 10px;">$\\tau_e$</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold;">{res['TE']:.2f} %</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #dee2e6;">
                        <td style="padding: 10px;">太阳光直接反射比<br><small style="color: #6c757d;">Direct Solar Reflectance (DER)</small></td>
                        <td style="padding: 10px;">$\\rho_e$</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold;">{res['RE']:.2f} %</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #dee2e6;">
                        <td style="padding: 10px;">太阳能总透射比<br><small style="color: #6c757d;">Solar Heat Gain Coefficient (SHGC / g-value)</small></td>
                        <td style="padding: 10px;">$g$</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold; color: #dc3545;">{res['G']:.2f} %</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px;">遮阳系数<br><small style="color: #6c757d;">Shading Coefficient (SC)</small></td>
                        <td style="padding: 10px;">$SC$</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold; color: #dc3545;">{res['SC']:.3f}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)
        
        # 光谱图
        if "spectra" in res and res["spectra"]:
            st.markdown("<br>", unsafe_allow_html=True)
            
            spectra = res["spectra"]
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
                plot_bgcolor="white"
            )
            
            # Additional minor ticks setting if Plotly supports it fully, else relying on the minor object setting above
            st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="text-align: center; color: #333333; font-size: 0.9rem; margin-top: 50px; margin-bottom: 20px; font-weight: 500;">
    &copy; 3M 2026. All Rights Reserved. &nbsp;&nbsp; 3M Confidential.
</div>
""", unsafe_allow_html=True)
