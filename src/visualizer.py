import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def plot_data(df):
    """
    Professional interactive dashboard (Power BI style)
    """

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_cols) == 0:
        st.warning("⚠️ No numeric columns available")
        return

    # -----------------------------
    # SELECT IMPORTANT COLUMNS
    # -----------------------------
    cols = numeric_cols[:3]

    # -----------------------------
    # 📈 INTERACTIVE LINE CHART
    # -----------------------------
    st.markdown("### 📈 Sensor Trends (Interactive)")

    fig = go.Figure()

    for col in cols:
        fig.add_trace(go.Scatter(
            y=df[col],
            mode='lines',
            name=col
        ))

    fig.update_layout(
        template="plotly_white",
        title="Sensor Trends Over Time",
        xaxis_title="Time Index",
        yaxis_title="Sensor Value",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # 📊 DISTRIBUTION (HISTOGRAM)
    # -----------------------------
    st.markdown("### 📊 Sensor Distribution")

    col1, col2, col3 = st.columns(3)

    for i, col in enumerate(cols):
        fig_hist = px.histogram(
            df,
            x=col,
            nbins=30,
            title=f"{col} Distribution",
            template="plotly_white"
        )

        if i == 0:
            col1.plotly_chart(fig_hist, use_container_width=True)
        elif i == 1:
            col2.plotly_chart(fig_hist, use_container_width=True)
        else:
            col3.plotly_chart(fig_hist, use_container_width=True)

    # -----------------------------
    # 🔥 CORRELATION HEATMAP
    # -----------------------------
    if len(numeric_cols) > 2:
        st.markdown("### 🔗 Correlation Heatmap")

        corr = df[numeric_cols].corr()

        fig_corr = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Blues",
            title="Feature Correlation",
        )

        st.plotly_chart(fig_corr, use_container_width=True)

    # -----------------------------
    # 🚨 FAILURE ANALYSIS
    # -----------------------------
    if "failure" in df.columns:

        st.markdown("### 🚨 Failure Analysis")

        colA, colB = st.columns(2)

        # Pie chart
        fig_pie = px.pie(
            df,
            names="failure",
            title="Failure vs Normal",
            template="plotly_white"
        )

        # Bar chart
        fig_bar = px.histogram(
            df,
            x="failure",
            title="Failure Count",
            template="plotly_white"
        )

        colA.plotly_chart(fig_pie, use_container_width=True)
        colB.plotly_chart(fig_bar, use_container_width=True)